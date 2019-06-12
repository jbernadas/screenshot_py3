********************
Screenshot Generator
********************

Tested on Mac and Linux. You may encounter issues downloading Reppy on Windows.

This is a Python 3 screenshot generator that takes full-page screenshots of all valid pages in a website. It does this by first crawling a website for related URL links then automatically generates a sitemap.txt file. It then reads the list of URLs in sitemap.txt and takes full-page PNG screenshots of each of the listed URLs there. It creates a full-page screenshot by stitching together different section screenshots into one full-page.

The first part of this screenshot generator uses the sitemap_gen created by Bernhard Ehlers, which is the Python 3 port of code made by Vladimir Toncar and Pavel Dvorak.

It has the following libraries as dependencies: PIL, Selenium, Reppy and ChromeDriver.

To download PIL, Selenium and Reppy, use pip3. 
::
  pip3 install Pillow
  pip3 install selenium
  pip3 install reppy

ChromeDriver is downloaded from: https://sites.google.com/a/chromium.org/chromedriver/downloads. Choose the appropriate Chrome version, save it to your computer, cd into the directory where you downloaded Chromedriver. Unzip the file:
::

  unzip chromedriver_linux64.zip

Mac and Linux
=============
Make chromedriver executable then move it to a directory that is part of your path:
::
  
  chmod +x chromedriver
  sudo mv chromedriver /usr/local/bin/chromedriver

Windows
=======
Place chromedriver into your PATH environment variable.

Fire it up
==========
Now cd into screenshot directory. Fire it up by invoking:
::

  python3 screenshot.py

It will ask you for the target URL. Be careful to check if the target URL has a lot of pages, the script will screenshot most of it (except those that end with PNG, JPG and PDF). The maximum is set at 100 pages, you can change this value in sitemap_gen.py.

Thanks for looking.
