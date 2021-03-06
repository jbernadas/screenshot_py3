********************
Screenshot Generator
********************

This is a Python 3 screenshot generator that takes full-page screenshots of all valid pages in a website. It does this by first crawling a website for related URL links then automatically generates a sitemap.txt file. It then reads the list of URLs in sitemap.txt and takes full-page PNG screenshots of each of the listed URLs. It creates a full-page screenshot by stitching together different section screenshots into one full-page.

It has the following libraries as dependencies: Pillow, Selenium, Reppy and ChromeDriver.

To download Pillow, Selenium and Reppy, use pip3. ChromeDriver has to be installed manually. 
::
  pip3 install Pillow
  pip3 install selenium
  pip3 install reppy

On Windows, you may encounter some errors installing Reppy, you may need to install Visual Studio with Microsoft Visual Studio C++ first.

The last dependecy you'll need is ChromeDriver which is downloaded from: https://sites.google.com/a/chromium.org/chromedriver/downloads. Choose the appropriate Chrome version, save it to your computer, cd into the directory where you downloaded Chromedriver. Unzip the file:
::
  unzip chromedriver_<your_os_platform>.zip

Mac and Linux
=============
Make chromedriver executable then move it to a directory that is part of your path:
::  
  chmod +x chromedriver
  sudo mv chromedriver /usr/local/bin/chromedriver

Note: On Mac, you may need to give permission to allow Chromedriver to be opened by clicking the question mark on the pop-up window and following the prompts.

Windows
=======
Place chromedriver into your PATH environment variable.

Fire it up
==========
Now cd into the screenshot directory. Fire it up by invoking:
::

  python3 screenshot.py

It will ask you for the target URL. Be careful to check if the target URL has a lot of pages, the script will screenshot most of it (except those that end with PNG, JPG and PDF). The maximum is set at 100 pages, you can change this value in sitemap_gen/sitemap_gen.py.

Thanks for looking.
