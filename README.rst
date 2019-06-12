====================
Screenshot Generator
====================

This is a Python 3 full-page screenshot generator that takes full-page screenshots of all pages in a website. It does this by first crawling a website for related links then automatically generates a sitemap.txt file. It then reads the list of URLs in sitemap.txt file and takes full-page PNG screenshots of each of the page listed there. It creates a full-page screenshot by stitching together different section screenshots into one full-page.

The first part of this screenshot generator uses the sitemap_gen created by Bernhard Ehlers, which is in-turn also based on the work by Vladimir Toncar and Pavel Dvorak. This is used for generating the sitemap.txt.

The util.py file is copied from

It has the following libraries as dependencies: Util, PIL, Selenium, ChromeDriver.

To download PIL and Selenium, you can use pip. 
::
  pip3 install Pillow
  pip3 install selenium

ChromeDriver is downloaded from: https://sites.google.com/a/chromium.org/chromedriver/downloads. Choose the appropriate Chrome version, save it to your computer, cd into the directory where you downloaded Chromedriver. Unzip the file:
::

  unzip chromedriver_linux64.zip

Make chromedriver executable then move it to a directory that is part of your path:
::
  
  chmod +x chromedriver
  sudo mv chromedriver /usr/local/bin/chromedriver

Now cd into screenshot directory. Fire up the multi.py file:
::

  python multi.py

It will ask you for the target URL. Be careful to check if the target URL has a lot of pages, the script will screenshot most of it (except those that end with PNG, JPG and PDF). The maximum is set at 100 pages, you can change this. You might want to change this in sitemap_gen.py.

Thanks for looking.