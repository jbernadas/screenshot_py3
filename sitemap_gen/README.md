# Sitemap Generator

`sitemap_gen` is a Python program, that crawls a web site and
outputs a XML sitemap.

It has been created by Vladimir Toncar and documented in
<http://toncar.cz/opensource/sitemap_gen.html>.

This version is a port of his fine program to Python 3.


## Requirements

- Python 3.x
- reppy (<https://github.com/seomoz/reppy>, install with `pip3 install reppy`)


## Usage

### Example

`python3 sitemap_gen.py -b doc -b bmp -o test_sitemap.xml http://www.your-site-name.com/index.html`

### Command Line Arguments

```text
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
```
