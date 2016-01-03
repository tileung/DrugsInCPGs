## Created: 09/29/15
## Purpose:
## (1) To compare MedicareCDW_ICDcodes.txt with icd9_cui.n3 to obtain mapped CUIs

## For part 2 see separate file: IncludedGLc_byCUI.py
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
fName = path + "MedicareCDW_CUIs.txt"
try:
    os.remove(fName)
    print("old file removed")
except OSError:
    pass

results_file = "MedicareCDW_CUIs.tab"
results = open(results_file,"w")
##results.write("GL no" + "\t" + "GL title" + "\t" + "Drug label (in GL)" + "\t" + "Drug label count in GL" + "\t" + "Drug label source" + "\t" + "Drug label (orig)" + "\t" + "Label type" + "\n")

## Identify files for comparison
MedicareICD = path + "MedicareCDW_ICDcodes.txt"
MedicareCUI = path + "icd9_cui.txt"

f = open(MedicareICD, 'r')
freader = csv.reader(f, dialect = csv.excel_tab)

for frow in freader:
    
    ICDcode = str(frow[1])
    ICDdisease = frow[0]
    ICDcond = frow[2]
    ICDlongname = frow[3]
    
    g = open(MedicareCUI, 'r')
    greader = csv.reader(g, dialect = csv.excel_tab)

    for grow in greader:
        mappedICD = str(grow[0])
        mappedCUI = str(grow[1])

        if mappedICD == ICDcode:
            line = ICDcode + '\t' + mappedCUI + '\t' + ICDdisease + '\t' + ICDlongname + '\n'          
            results.write(line)

results.close()

end = time.time()
elapsed = end - start
print "Time elapsed (in seconds)"
print elapsed
sys.exit(0)

##GL_list = path + "ngc_rss_guidelineList.txt"
