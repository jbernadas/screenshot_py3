********************
Screenshot Generator
********************

This is the Python 3 version of an old screenshot generator I made 2 years ago. This screenshot generator takes full-page screenshots of all valid pages in a website. It does this by first crawling a website for related URL links then automatically generates a sitemap.txt file. It then reads the list of URLs in sitemap.txt and takes full-page PNG screenshots of each of the listed URLs there. It creates a full-page screenshot by stitching together different section screenshots into one full-page.

The first part of this screenshot generator uses the sitemap_gen created by Bernhard Ehlers, which is the Python 3 port of code made by Vladimir Toncar and Pavel Dvorak.

It has the following libraries as dependencies: Util, PIL, Selenium, ChromeDriver.

To download PIL and Selenium, you can use pip. 
::
  pip3 install Pillow
  pip3 install selenium
  pip3 install requests

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
