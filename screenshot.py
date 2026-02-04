"""Full-page screenshot generator using Selenium 4 and Chrome CDP."""

import argparse
import base64
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def take_screenshot(driver, url, output_path, width):
    """Take a full-page screenshot of a URL using Chrome CDP."""
    driver.get(url)

    # Get full page dimensions
    page_height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, "
        "document.body.offsetHeight, "
        "document.documentElement.clientHeight, "
        "document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);"
    )

    # Set viewport to full page height
    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": width,
        "height": page_height,
        "deviceScaleFactor": 1,
        "mobile": False,
    })

    # Capture full-page screenshot via CDP
    result = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "format": "png",
        "captureBeyondViewport": True,
    })

    output_path.write_bytes(base64.b64decode(result["data"]))
    print(f"  Saved: {output_path}")


def parse_urls(args):
    """Return a list of URLs from either a file or direct arguments."""
    urls = []
    for item in args:
        path = Path(item)
        if path.is_file():
            urls.extend(
                line.strip()
                for line in path.read_text().splitlines()
                if line.strip()
            )
        else:
            urls.append(item)
    return urls


def main():
    parser = argparse.ArgumentParser(
        description="Take full-page screenshots of web pages."
    )
    parser.add_argument(
        "urls",
        nargs="+",
        help="URLs to screenshot, or a file containing one URL per line",
    )
    parser.add_argument(
        "--output-dir",
        default="./website-screenshots",
        help="directory for saved screenshots (default: ./website-screenshots/)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1440,
        help="viewport width in pixels (default: 1440)",
    )
    args = parser.parse_args()

    urls = parse_urls(args.urls)
    if not urls:
        print("No URLs provided.", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    options = Options()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    try:
        for i, url in enumerate(urls, start=1):
            print(f"[{i}/{len(urls)}] {url}")
            try:
                output_path = output_dir / f"page{i}.png"
                take_screenshot(driver, url, output_path, args.width)
            except Exception as exc:
                print(f"  FAILED: {exc}", file=sys.stderr)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
