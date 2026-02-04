********************
Screenshot Generator
********************

A Python 3 tool that takes full-page screenshots of web pages using Selenium and Chrome CDP.

Dependencies
============

Install Selenium via pip::

  pip3 install selenium

You also need Chrome (or Chromium) installed. Selenium 4 manages ChromeDriver automatically via its built-in driver manager.

Usage
=====

Screenshot one or more URLs directly::

  python3 screenshot.py https://example.com https://other.com

Or read URLs from a file (one per line)::

  python3 screenshot.py urls.txt

Options::

  --output-dir DIR   Directory for saved screenshots (default: ./website-screenshots/)
  --width PIXELS     Viewport width in pixels (default: 1440)

Screenshots are saved as ``page1.png``, ``page2.png``, etc. in the output directory.
