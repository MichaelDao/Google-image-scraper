from bs4 import BeautifulSoup
import requests
import json
import urllib2
import os
import re

# prompt for input
query = raw_input("Enter the search query for google images: ")
#downLimit = raw_input("Enter the amount of images to download: ")

# replace whitespace with the '+' symbol for google url
cleanQuery = re.sub("\s+", "+", query.strip())

# with the query, create url for google images
url = "https://www.google.com.au/search?q=" + cleanQuery + "%20&hl=en&source=lnms&tbm=isch"

# display url we will download from
print ("\n--- begin download of query: '" + cleanQuery + "' from the url:\n" + url + "\n") 

# header is tailored for each browser
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

# Open the url with beatiful soup and urllib2 
soupURL = urllib2.urlopen(urllib2.Request(url, headers=header))
soup = BeautifulSoup(soupURL, "html.parser")

# array stores image link and its type (e.g. jpg)
imageArray=[]

# loop through all images from query search
for a in soup.find_all("div",{"class":"rg_meta"}):	
	# get image link and image type for the array
	imgLink, imgType = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
	imageArray.append((imgLink, imgType))

# display total elements of images in array
print ("Total of " + str(len(imageArray)) + " images found.")
 
# directory for downloaded images
directory = "Pictures"

# if the directory doesnt exist, create it 
if not os.path.exists(directory):
	os.mkdir(directory)

# create a directory specificly for this query
queryDirectory = os.path.join(directory, query)

# make sure we create this new directory 
if not os.path.exists(queryDirectory):
	os.mkdir(queryDirectory)

# print images
# to set a limit, change to enumerate(imageArray[5]) if you want 5 only!
for i, (imgLink, imgType) in enumerate(imageArray):
	try:
		# get raw image from requested url
		requestURL = urllib2.Request(imgLink, headers=header)
		rawImage = urllib2.urlopen(requestURL).read()

		# display current download
		print "\ndownloading " + imgType + " " + str(i+1)
		print imgLink
	
		# download image and set its name into the directory
    	 	f = open(os.path.join(queryDirectory, query + " (" + str(i+1)) + ")." + imgType, 'wb')
		f.write(rawImage)
		f.close

	# error handling
	except Exception as e:
		print e

# downloading finished
print "\ndone!"
