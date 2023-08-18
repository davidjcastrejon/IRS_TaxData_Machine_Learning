import zipfile
from multiprocessing import Pool
import glob
import matplotlib.pyplot as plt

from lxml import etree

# Start with an empty function

def extract1(fname, zf):
    """
    Extract elements of interest
    fname: IRS 990 XML file
    zf: ZipFile where fname is stored
    """
    # print("file opened correctly")
    f = zf.open(fname)
    tree = etree.parse(f)
    ns = {'irs':'http://www.irs.gov/efile'}

    # Holds everything we're interested in.
    result = {}

    #result["description"] = tree.xpath('//irs:DescriptionProgramSrvcAccomTxt/text()', namespaces = ns)


    result["BusinessName"] = tree.xpath('//irs:Filer/irs:BusinessName/irs:BusinessNameLine1Txt/text()', namespaces = ns)[0]

    result["Year"] = int(tree.xpath('//irs:TaxYr/text()', namespaces = ns)[0])

    # XML query to find the total amount spent by the nonprofit within the XML file f
    try:
        total_spent = float(tree.xpath('//irs:TotalFunctionalExpensesGrp/irs:TotalAmt/text()', namespaces = ns)[0])
        result["TotalSpent"] = total_spent
    except:
        pass

    # XML query to find the total amount received by the nonprofit within the XML file f
    try:
        total_received = float(tree.xpath('//irs:TotalRevenueGrp/irs:TotalAmt/text()', namespaces = ns)[0])
        result["TotalReceived"] = total_received
    except:
        pass

    return result


# We use this on ONE zip file
def extract(zname):
    """
    Extract elements of interest
    zname: zipfile
    """
    zf = zipfile.ZipFile(zname)
    f = lambda x: extract1(x, zf)
    # Map a function over every file in the ZipFile
    result = map(f, zf.namelist())
    return list(result)

# List of zip files to process
allzipfiles = glob.glob("/stat129/*.zip")

# List of five nonprofit organizations
nonprofits = ["American Association for the Advancement of Science", 
              "American Chemical Society", "American Physical Society", 
              "American Mathematical Society", 
              "Society for Industrial and Applied Mathematics"]

# Function to filter the results based on the nonprofit name
def filter_results(results):
    filtered_results = []
    for result in results:
        if result["BusinessName"] in nonprofits:
            filtered_results.append(result)
    return filtered_results

# Use 4 parallel processes to extract data from the zip files
with Pool(8) as p:
    # Extract the data from the zip files in parallel
    all_results = p.map(extract, allzipfiles)
    # Flatten the list of results
    flat_results = [item for sublist in all_results for item in sublist]
    # Filter the results for the nonprofit organizations
    filtered_results = filter_results(flat_results)


# Assuming data is a list of dictionaries with each dictionary containing the data for one nonprofit
# The keys in each dictionary should be "BusinessName", "Year", "AmountSpent", and "AmountReceived"

# Create a figure and axis object
fig, ax = plt.subplots()

# Loop through each nonprofit's data and plot the amount spent and amount received over time
colors = ['blue', 'orange', 'green', 'red', 'purple']
legends = []
for i, non_profit in enumerate(filtered_results):
    x = non_profit["Year"]
    y1 = non_profit["TotalSpent"]
    y2 = non_profit["TotalReceived"]
    ax.plot(x, y1, color=colors[i], label=non_profit["BusinessName"]+" Spent")
    ax.plot(x, y2, color=colors[i], linestyle='dashed', label=non_profit["BusinessName"]+" Received")
    legends.append(non_profit["BusinessName"]+" Spent")
    legends.append(non_profit["BusinessName"]+" Received")

# Add legend and axis labels
ax.legend(legends, loc='upper left')
ax.set_xlabel('Year')
ax.set_ylabel('Amount ($)')

# Save the plot as a PNG file
plt.savefig('nonprofits_plot.png')


"""
# Moving on to the whole data set:
allzipfiles = glob.glob("/stat129/*.zip")


with Pool(8) as p:
    result = p.map(extract, allzipfiles)
"""


