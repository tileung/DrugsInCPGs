## Created: 09/29/15
## Purpose:
## For part 1 see separate file: icd_cui_mapping.py
## (1) To compare MedicareCDW_ICDcodes.txt with icd9_cui.n3 to obtain mapped CUIs

## (2) To retrieve only guideline summaries in ngc_rss_guidelineList.txt that have CUIs from (1)

import os
import sys
import csv

import time

## Start timer
start = time.time()

## Set path
path = "C:\\Users\\tileung\\Dropbox\\Py Stuffs - Drugs in CPGs\\SeptCode\\"

## Initiate file to save results
fName = path + "IncludedGLs_byCUI.txt"
try:
    os.remove(fName)
    print("old file removed")
except OSError:
    pass

results_file = "IncludedGLs_byCUI.tab"
results = open(results_file,"w")

## start counter - how many GLs identified by matching CUIs?
x = 0

## Identify files for comparison
GL_list = path + "ngc_rss_guidelineList.txt"
MedicareCUI = path + "MedicareCDW_CUIs.tab"

f = open(GL_list, 'r')
freader = csv.reader(f, dialect = csv.excel_tab)

for frow in freader:

    try:
        GL_no = str(frow[0])
        GL_cui = str(frow[3]) ##match to MedicareCUIs
        GL_title = frow[1]
        GL_link = frow[2]
        
        g = open(MedicareCUI, 'r')
        greader = csv.reader(g, dialect = csv.excel_tab)

        for grow in greader:
            mappedICD = str(grow[0])
            mappedCUI = str(grow[1]) ##match to GL CUIs
            ICDcond = grow[2]
            ICDlongname = grow[3]
        
            if mappedCUI == GL_cui:
                line = GL_no + '\t' + GL_title + '\t' + GL_link + '\t' + mappedCUI + '\t' + mappedICD + '\t' + ICDcond + '\t' + ICDlongname + '\n'
                results.write(line)
                x = x+1
                print x, GL_no, ICDlongname

    except IndexError as e:
        continue
    
results.close()

end = time.time()
elapsed = end - start
print "Time elapsed (in seconds)"
print elapsed
sys.exit(0)
