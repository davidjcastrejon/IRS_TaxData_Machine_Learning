# Importing necessary modules lxml, urllib.request, and ssl
import lxml.html
import urllib.request
import ssl

# Parse the HTML page
ssl._create_default_https_context = ssl._create_unverified_context

# Setting the variable url to the path of the directory containing the zip files
url = "https://www.irs.gov/charities-non-profits/form-990-series-downloads"

# Parsing the HTML of url to get the root element
tree = lxml.html.parse(url).getroot()

# Get all zip files from url using an XPath expression to find all downloadable zip files under the 'a' nodes.
for link in tree.xpath("//a[contains(@href,'.zip')]"):
    # Extract the filename from the URL using split and the delimiter '/'
    fname = link.attrib['href'].split('/')[-1]
    # Download the file found in iteration of the for each loop and saves to working directory
    urllib.request.urlretrieve(link.attrib['href'], fname)
    
