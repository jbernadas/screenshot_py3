# -*- coding: utf-8 -*-

'''
Various utility functions used throughout this mini-framework.
'''

import datetime
import os
import platform
import time
from time import strftime

from PIL import Image
import requests


def get_nice_time_and_date():
    '''Returns a readable time and date, eg: SUN130915_165434'''
    nice_time_and_date = datetime.datetime.now().strftime("%a%d%b%Y" + "_" + "%X").upper()
    nice_time_and_date = nice_time_and_date.replace(":", "")
    return nice_time_and_date

def create_screens_dir(mobile=None):
    '''Check for screenshots directory; create it if it doesn't exist'''
    current_date = strftime("%d%m%y")
    cwd = os.getcwd()
    screenshots_today = current_date
    if mobile is True:
        screenshots_location = "/screenshots/mobile/"
    else:
        screenshots_location = "/screenshots/desktop/"
    main_screenshots_dir = cwd+screenshots_location
    if not os.path.exists(main_screenshots_dir):
        os.makedirs(main_screenshots_dir)
        print("'{0}' directory created".format(screenshots_location))
    else:
        print ("The 'screenshots' directory already exists")
        os.chdir(main_screenshots_dir)
    if not os.path.exists(screenshots_today):
        os.makedirs(screenshots_today)
        print ("'{0}{1}/' directory created".format(screenshots_location, current_date))
    else:
        print ("The '{0}{1}/' dir already exists".format(screenshots_location, current_date))
    os.chdir(cwd)

def desktop_screenshot(driver, filename):
    '''Create desktop screenshot'''
    current_date = strftime("%d%m%y")
    filename = filename+"_"
    platform_info = platform.system()+"_"+platform.release()+"_"
    browser_info = driver.capabilities['browserName']+"_"+driver.capabilities['version']+"_"
    screenshot_filename = filename+platform_info+browser_info+get_nice_time_and_date()+".png"
    path = os.getcwd()+"/screenshots/desktop/{0}/{1}".format(current_date, screenshot_filename)
    driver.get_screenshot_as_file(path)

def browserstack_screenshot(driver, filename, mobile=None):
    '''Create browserstack screenshot'''
    current_date = strftime("%d%m%y")
    screenshot_filename = filename+get_nice_time_and_date()+".png"
    if mobile is True:
        screenshots_location = "/screenshots/mobile/"
    else:
        screenshots_location = "/screenshots/desktop/"
    path = os.getcwd()+screenshots_location+"{0}/{1}".format(current_date, screenshot_filename)
    driver.get_screenshot_as_file(path)

def get_page_status(url):
    '''Get page status'''
    req = requests.get(url)
    status = req.status_code
    print ("Status code for URL {0}: {1}".format(url, status))
    return status

def take_desktop_screenshot(driver, filename):
    '''Create desktop screenshot'''
    current_date = strftime("%d%m%y")
    filename = filename+"_"
    platform_info = platform.system()+"_"+platform.release()+"_"
    browser_info = driver.capabilities['browserName']+"_"+driver.capabilities['version']+"_"
    screenshot_filename = filename+platform_info+browser_info+get_nice_time_and_date()+".png"
    path = os.getcwd()+"/screenshots/desktop/{0}/{1}".format(current_date, screenshot_filename)
    driver.get_screenshot_as_file(path)

def mobile_screenshot_old_version(driver, filename):
    '''Create desktop screenshot'''
    current_date = strftime("%d%m%y")
    filename = filename+"_"
    platform_info = platform.system()+"_"+platform.release()+"_"
    platform_info = ""
    browser_info = driver.capabilities['browserName']+"_"+driver.capabilities['version']+"_"
    browser_info = ""
    screenshot_filename = filename+platform_info+browser_info+get_nice_time_and_date()+".png"
    path = os.getcwd()+"/screenshots/mobile/{0}/{1}".format(current_date, screenshot_filename)
    driver.get_screenshot_as_file(path)

def mobile_screenshot(driver, filename):
    '''Create mobile screenshot. This method is used by:
       AVD.py, selendroid.py, CDME.py, appium.py, chromedriver.py
    '''
    current_date = strftime("%d%m%y")
    screenshot_filename = filename+get_nice_time_and_date()+".png"
    path = os.getcwd()+"/screenshots/mobile/{0}/{1}".format(current_date, screenshot_filename)
    driver.get_screenshot_as_file(path)

def fullpage_screenshot(driver, file):
    """
    This function is a slightly modified version of the one here:
    https://snipt.net/restrada/python-selenium-workaround-for-full-page-screenshot-using-chromedriver-2x/
    It contains the *crucial* correction added in the comments by Jason Coutu. 
    This function is not called within this framework but is included here for reference.
    """
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    rectangles = []

    i = 0
    while i < total_height:
        j = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while j < total_width:
            top_width = j + viewport_width

            if top_width > total_width:
                top_width = total_width

            rectangles.append((j, i, top_width, top_height))

            j = j + viewport_width

        i = i + viewport_height

    stitched_image = Image.new('RGB', (total_width, total_height))
    previous = None
    part = 0

    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.2)

        file_name = "part_{0}.png".format(part)
        print ("Capturing {0} ...".format(file_name))

        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(file_name)
        part = part + 1
        previous = rectangle

    stitched_image.save(file)
    return True
