""" 
    This is a SCREENSHOT GENERATOR that takes full-page images of web pages. It excludes PNG, JPG and PDF files.

    ------------------------------------

    Copyright (C) 2016-2019 Joseph Bernadas

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
import os
from selenium import webdriver
import unittest
import util
import sitemap_gen

target_url = input('What is the target URL? ')
exclude1 = 'png'
exclude2 = 'jpg'
exclude3 = 'pdf'

# # fire up the sitemap generator with the following parameter/options
# # -b stands for block extensions, to be excluded from crawl, i.e., pdf, doc, excel, etc.
# # please refer to http://toncar.cz/opensource/sitemap_gen.html for additional info on how to use sitemap_gen.py
os.system('python3 ./sitemap_gen/sitemap_gen.py -b %s -b %s -b %s %s' %(exclude1, exclude2, exclude3, target_url))

# Ask user if they want to make changes to the sitemap.txt file before proceeding to take screenshots
itsago = input("You can now edit the generated sitemap.txt file. Type 'go' to proceed. ")
if itsago == "go":
    # Proceed with taking screenshots
    class Test(unittest.TestCase):
        """ Get Chrome to generate fullscreen screenshot """

        def setUp(self):
            self.driver = webdriver.Chrome()

        def tearDown(self):
            self.driver.quit()

        def test_fullpage_screenshot(self):
            ''' Generate document-height screenshot '''
            
            i = 1
            with open("sitemap.txt") as urls:
                for line in urls:
                    self.driver.get(line)
                    self.driver.set_window_size(1440, 2000)
                    util.fullpage_screenshot(self.driver, "./website-screenshots/page" + str(i) + ".png")  
                    i = i + 1
            urls.close()
else:
    print("The required reply was not received, exiting program. Bye!")

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
