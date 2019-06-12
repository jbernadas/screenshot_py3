#! /usr/bin/env python3
"""
    Copyright (C) 2007-2009 Vladimir Toncar
    Copyright (C) 2018-2019 Bernhard Ehlers

    Contributors:
        Redirect handling by Pavel "ShadoW" Dvorak

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

"""

import sys
import getopt
import gzip
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
import xml.sax.saxutils
from reppy.robots import Robots


helpText = """sitemap_gen.py version 1.2.3 (2019-02-12)

This script crawls a web site from a given starting URL and generates
a Sitemap file in the format that is accepted by Google. The crawler
does not follow links to other web sites. It also respects the 'nofollow'
tags and will not crawl into directories disallowed in the robots.txt file.

Command line syntax:

python3 sitemap_gen.py <options> <starting URL>

Available options:
-h         --help                Print this text and exit

-b <ext>   --block <ext>         Exclude URLs with the given extension;
                                 <ext> must be without the leading dot.
                                 The comparison is case insensitive, so
                                 for example DOC and doc are treated
                                 the same. You can use this option several
                                 times to block several extensions.

-c <value> --changefreq <value>  Set the change frequency. The given value
                                 is used in all sitemap entries (maybe a
                                 future version of this script will change
                                 that). The allowed values are: always,
                                 hourly, daily, weekly, monthly, yearly,
                                 never.

-p <prio>  --priority <prio>     Set the priority. The value must be from
                                 the interval between 0.0 and 1.0. The value
                                 will be used in all sitemap entries.

-m <value> --max-urls <value>    Set the maximum number of URLs to be crawled.
                                 The default value is 1000 and the largest
                                 value that you can set is 50000 (the script
                                 generates only a single sitemap file).

-o <file>  --output-file <file>  Set the name of the geneated sitemap file.
                                 The default file name is sitemap.xml.

Usage example:
python3 sitemap_gen.py -b doc -b bmp -o test_sitemap.xml http://www.your-site-name.com/index.html

For more information, visit http://toncar.cz/opensource/sitemap_gen.html

"""

allowedChangefreq = ["always", "hourly", "daily", "weekly", \
                     "monthly", "yearly", "never"]

def getPage(url):
    try:
        f = urllib.request.urlopen(url)
        page = f.read()
        if 'Content-Encoding' in f.headers and \
           f.headers['Content-Encoding'] == 'gzip':
            page = gzip.decompress(page)

        # Get the last modify date
        try:
            if 'Last-Modified' in f.headers:
                date = f.headers['Last-Modified']
            else:
                date = f.headers['Date']
            date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
            date = (date.year, date.month, date.day)
        except (KeyError, ValueError):
            date = (0, 0, 0)
        f.close()
        return (page, date, f.url)
    except urllib.error.URLError as detail:
        print("%s. Skipping..." % (detail))
        return (None, (0, 0, 0), "")
#end def


def joinUrls(baseUrl, newUrl):
    helpUrl, _ = urllib.parse.urldefrag(newUrl)
    return urllib.parse.urljoin(baseUrl, helpUrl)
#end def


def getRobotParser(startUrl):
    robotUrl = urllib.parse.urljoin(startUrl, "/robots.txt")
    page, _, _ = getPage(robotUrl)

    if page is None:
        print("Could not read ROBOTS.TXT at: " + robotUrl)
        return None
    #end if

    rp = Robots.parse(robotUrl, page)
    print("Found ROBOTS.TXT at: " + robotUrl)
    return rp
#end def


class MyHTMLParser(HTMLParser):

    def __init__(self, pageMap, redirects, baseUrl, maxUrls, blockExtensions, robotParser):
        HTMLParser.__init__(self)
        self.pageMap = pageMap
        self.redirects = redirects
        self.baseUrl = baseUrl
        self.server = urllib.parse.urlsplit(baseUrl)[1] # netloc in python 2.5
        self.maxUrls = maxUrls
        self.blockExtensions = tuple(blockExtensions)
        self.robotParser = robotParser
    #end def

    def hasBlockedExtension(self, url):
        p = urllib.parse.urlparse(url)
        path = p[2].upper() # path attribute
        return path.endswith(self.blockExtensions)
    #end def

    def handle_starttag(self, tag, attrs):
        if len(self.pageMap) >= self.maxUrls:
            return

        if tag.upper() == "BASE":
            if attrs[0][0].upper() == "HREF":
                self.baseUrl = joinUrls(self.baseUrl, attrs[0][1])
                print("BASE URL set to " + self.baseUrl)

        if tag.upper() == "A":
            #print("Attrs: " + str(attrs))
            url = ""
            # Let's scan the list of tag's attributes
            for attr in attrs:
                #print("  attr: " + str(attr))
                if (attr[0].upper() == "REL") and (attr[1].upper().find('NOFOLLOW') != -1):
                    # We have discovered a nofollow, so we won't continue
                    return
                elif (attr[0].upper() == "HREF") and (attr[1].upper().find('MAILTO:') == -1):
                    # We have discovered a link that is not a Mailto:
                    url = joinUrls(self.baseUrl, attr[1])
            #end for
            # if the url is empty, there was none in the list of attributes
            if url == "":
                return

            # Check if we want to follow the link
            if urllib.parse.urlsplit(url)[1] != self.server:
                return
            if self.hasBlockedExtension(url) or self.redirects.count(url) > 0:
                return
            if self.robotParser is not None and not self.robotParser.allowed(url, "sitemap_gen"):
                print("URL restricted by ROBOTS.TXT: " + url)
                return
            # It's OK to add url to the map and fetch it later
            if not url in self.pageMap:
                self.pageMap[url] = ()
        #end if

    #end def
#end class

def getUrlToProcess(pageMap):
    for i in pageMap.keys():
        if pageMap[i] == ():
            return i
    return None

def parsePages(startUrl, maxUrls, blockExtensions):
    pageMap = {}
    pageMap[startUrl] = ()
    redirects = []

    robotParser = getRobotParser(startUrl)

    while True:
        url = getUrlToProcess(pageMap)
        if url is None:
            break
        print("  " + url)
        page, date, newUrl = getPage(url)
        if page is None:
            del pageMap[url]
        elif url != newUrl:
            print("Redirect -> " + newUrl)
            del pageMap[url]
            pageMap[newUrl] = ()
            redirects.append(url)
        else:
            pageMap[url] = date
            parser = MyHTMLParser(pageMap, redirects, url, maxUrls, blockExtensions, robotParser)
            try:
                parser.feed(page.decode("utf-8", errors='strict'))
                parser.close()
            except UnicodeError:
                print("Failed decoding %s . Try to check if the page is valid." % (url))
    #end while

    return pageMap
#end def

# This has been changed by JBernadas to output a text file instead of xml file
def generateSitemapFile(pageMap, fileName, changefreq="", priority=0.0):
    fw = open(fileName, "wt")
    for i in sorted(pageMap.keys()):
        fw.write('%s\n' % (xml.sax.saxutils.escape(i)))
    #end for
    fw.close()
#end def



def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],\
                "hb:c:m:p:o:", \
                ["help", "block=", "changefreq=", \
                 "max-urls=", "priority=", "output-file="])
    except getopt.GetoptError:
        sys.stderr.write(helpText)
        return 1

    blockExtensions = []
    changefreq = ""
    priority = 0.0
    fileName = "sitemap.txt"
    maxUrls = 100
    pageMap = {}

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            sys.stderr.write(helpText)
            return 1
        elif opt in ("-b", "--block"):
            blockExtensions.append("." + arg.upper())
        elif opt in ("-c", "--changefreq"):
            if arg in allowedChangefreq:
                changefreq = arg
            else:
                sys.stderr.write("Allowed changefreq values are:\n")
                for i in allowedChangefreq:
                    sys.stderr.write("  {}\n".format(i))
                return 1
        elif opt in ("-m", "--max-urls"):
            maxUrls = int(arg)
            if (maxUrls < 0) or (maxUrls > 50000):
                sys.stderr.write("The maximum number of URLs must be between 1 and 50000\n")
                return 1
        elif opt in ("-p", "--priority"):
            priority = float(arg)
            if (priority < 0.0) or (priority > 1.0):
                sys.stderr.write("Priority must be between 0.0 and 1.0\n")
                return 1
        elif opt in ("-o", "--output-file"):
            fileName = arg
            if fileName in ("", ".", ".."):
                sys.stderr.write("Please provide a sensible file name\n")
                return 1
        #end if

    if not args:
        sys.stderr.write("You must provide the starting URL.\nTry the -h option for help.\n")
        return 1

    # Set user agent string
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'sitemap_gen/1.0'),
                         ('Accept', '*/*'), ('Accept-Encoding', 'gzip')]
    urllib.request.install_opener(opener)

    # Start processing
    print("Crawling the site...")
    pageMap = parsePages(args[0], maxUrls, blockExtensions)
    print("Generating sitemap: %d URLs" % (len(pageMap)))
    generateSitemapFile(pageMap, fileName, changefreq, priority)
    print("Finished.")
    return 0
#end def

if __name__ == '__main__':
    try:
        status_code = main()
    except KeyboardInterrupt:
        status_code = 130
    sys.exit(status_code)
