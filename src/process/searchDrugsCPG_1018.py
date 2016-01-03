## Revised: 09/22/15
## Created: 12/02/14
## Purpose: Code for querying NGC guidelines for drug ingredients from Drug Bank and other ontologies.

## Modified to re-run on 10/18/15 ## Adapted from searchDugsCPG_0922.py
## Files used:
## labels_byLen1018.txt AND labels-rxnormByLen
## NGC-xml-2015_1003.zip
## IncludedGLs_byCUI_byPop.tab

import urllib
import os
import re
import sys
import csv
import json

import zipfile
import xml.dom.minidom
import xml.parsers.expat
import time

## Start timer
start = time.time()

## Set path
path = "C:\\Users\\tileung\\Dropbox\\"

## Initiate file to save results
## fName = path + "Py Stuffs - Drugs in CPGs\\drugsInGuidelines.txt"  ## 12/17/14 for exclusions
fName = "C:\\Users\\tileung\\Documents\\drugsInGuidelines_1018-rxnorm-2.txt"
try:
    os.remove(fName)
    print("old file removed")
except OSError:
    pass

## Defined function for searching a string StrRecom (Mjr Rec) for text strList (Drug Label)
def getCount(strList, strRecom):
    kTotal=0
    strRecomLower = strRecom.lower()   
    labelLower = strList.lower()
    labelLower = re.escape(labelLower)
    label = r'\b' + labelLower + r'\b'   
    p = re.compile(label)
    findLabel = p.findall(strRecomLower)
    kTotal = kTotal + len(findLabel)
    strRecomLower.replace(labelLower,"")
    return kTotal

## Obtain Drug Bank list of drugs
## drugbankList = path + 'Py Stuffs - Drugs in CPGs\\SeptCode\\labels_byLen1018.txt'
drugbankList = path + 'Py Stuffs - Drugs in CPGs\\SeptCode\\labels-rxnormByLen.txt'
    ## tab file contains labels newly obtained 10/17/15. Sorted by longest to shortest. Includes: CHEBI, DrugBank, MESH, ATC, NDF-RT, NCBI (no RxNorm)
    ## all obtained from AberOWL and Bioportal

## Get all guidelines
ngc_zip = "c:/Users/tileung/Documents/NGC-xml-2015_1003.zip"
ngc_list_file = "C:\\Users\\tileung\\Documents\\IncludedGLs_byCUI_byPop-rxnorm-2.txt"

ngc_list = {}
f = open(ngc_list_file, 'r')
reader = csv.reader(f, dialect = csv.excel_tab)
for row in reader:
    ngc_list[ row[0]] = row
    
# iterate over ngc files
z = zipfile.ZipFile(ngc_zip,'r')

for f in z.namelist():
    ngc_id = f[22:-4]
    if ngc_id not in ngc_list:
        continue
    
    f = 'NGC-xml-2015_1003/NGC-' + str(ngc_id) + '.xml'
    print str(ngc_id)
    data = z.read(f)
    try:
        dom = xml.dom.minidom.parseString(data)
    except xml.parsers.expat.ExpatError as e:
        continue

    for field in dom.getElementsByTagName("Field"):
        if field.getAttribute("Name") == "Guideline Title":
            fv = field.getElementsByTagName("FieldValue")
            title = str(fv.item(0).toxml('utf-8'))
            filler1 = '<FieldValue Value='
            filler5 = '&lt;div class=&quot;content_title&quot;&gt;'
            filler2 = '.&lt;/div&gt;'
            filler6 = '/>'
            titleShort2 = title.replace(filler1,"").replace(filler2,"").replace(filler5,"").replace(filler6,"")
            titleShort = titleShort2.encode('string_escape')
            
        if field.getAttribute("Name") != "Major Recommendations":
            continue

        fv = field.getElementsByTagName("FieldValue")
        text = str(fv.item(0).toxml('utf-8'))
        text2 = str.lower(str(fv.item(0).toxml('utf-8')))

        ## Iterate through labels from drug list and find in Recommendations text
        f = open(drugbankList,"r")
        reader = csv.reader(f, dialect = csv.excel_tab)
        next(reader)
        for row in reader:

            lab = row[1]
            labSource = row[0] ##Added: 09/27/15
            labType = row[2] ##Added: 09/27/15

            ## Perform search in text
            
            labDrug = getCount(lab,text2)
            
            if labDrug > 0:            
                res = str(ngc_id) + "\t" + titleShort + "\t" + lab + "\t" + str(labDrug) + "\t" + labSource + "\t" + labType + "\n"
##                print res
##                sys.exit(0)
                
                with open(fName, "a") as myfile:
                    myfile.write(res)

myfile.close()
end = time.time()

elapsed = end - start
print "Time elapsed (in sec)"
print elapsed
sys.exit(0)
