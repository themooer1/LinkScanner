# LinkScanner <br><img src="https://img.shields.io/github/downloads/themooer1/LinkScanner/total.svg"> <img src="https://img.shields.io/pypi/dm/LinkScanner.svg">  <a href="/to/themooer1"><img src="https://img.shields.io/badge/Say%20Thanks!-🦉-1EAEDB.svg"></a>
Follow links from website to website.

## Usage
LinkScanner takes input from a text file with newline seperated links, locates the links on those pages and either outputs them to links.txt or locates the links on those pages to a set recursion depth.
#### Import
```python
import LinkScanner
```
Can be used like this
```python
if __name__=='__main__':
    linkscanner=Scanner(iterations=3,maxthreads=20,siteList='pathToInputLinks.txt')
    linkscanner.startScan()
    linkscanner.save()
```
The second line is most important, as it set the options for the scanner and provides input.  Most arguments while not necessary are recommended.

| Options       | Necessary     | Default| Purpose|
| ------------- |:-------------:| ------:|-------------------:|
| iterations    | no |3|How many times the results will be scanned before output.|
| maxthreads    | no |8|The most worker threads allowed to run at once|
| siteList |yes|siteList.txt|The name of the input file in the same directory.|

#### Input
The input `sitelist.txt` must be formatted as follows.
```
https://wikipedia.org
http://msn.com
https://example.com
```
Use `http://` if in doubt.
