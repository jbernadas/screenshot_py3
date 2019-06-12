====================
Screenshot Generator
====================

This is a Python 3 screenshot generator that takes a URL address and crawls through it to generate a list of inner URLs writing it in a sitemap.txt file. It then reads the list of URLs in sitemap.txt file and goes through the list one by one to create a full-page PNG screenshot of the web page. 

This screenshot generator uses the Sitemap Generator created by Bernhard Ehlers, which is in-turn also based on the work by Vladimir Toncar and Pavel Dvorak.

It has the following libraries as dependencies: Util, PIL, Selenium, ChromeDriver.

To download Util, PIL and Selenium, you can use pip. 
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

It will ask you for the target URL. Be careful to check if the target URL has a lot of pages, the script will screenshot most of it (except those that end with PNG, JPG and PDF). The maximum is set at 4999 pages, which might be too much. You might want to change this in sitemap_gen.py.

Thanks for looking.
