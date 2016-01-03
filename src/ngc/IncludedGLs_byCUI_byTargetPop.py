## Created: 09/29/15
## Adapted from IncludedGL_byCUI.pt

## Purpose: final list of included CPGs and their disease categories/GUIs

import os
import sys
import csv

## Set path
path = "C:\\Users\\tileung\\Dropbox\\Py Stuffs - Drugs in CPGs\\SeptCode\\"

## Initiate file to save results
fName = path + "IncludedGLs_byCUI_byPop.txt"
try:
    os.remove(fName)
    print("old file removed")
except OSError:
    pass

results_file = "IncludedGLs_byCUI_byPop.tab"
results = open(results_file,"w")

## Identify files for comparison
byCUI_list = path + "unique_IncludedGLs_byCUI.txt"
byPop_list = path + "IncludedCPGs_popExclusions1018.txt"

f = open(byCUI_list, 'r')
freader = csv.reader(f, dialect = csv.excel_tab)

for frow in freader:

    try:
        GL_no = str(frow[0]) ##match to same key in byPop_list
        GL_cui = str(frow[3]) 
        GL_title = frow[1]
        GL_link = frow[2]
        GL_icd = str(frow[4])
        GL_cat = frow[5]
        GL_icdlong = frow[6]
        
        g = open(byPop_list, 'r')
        greader = csv.reader(g, dialect = csv.excel_tab)

        for grow in greader:
            GL_iNo = str(grow[0]) ## match to same key in byCUI_list
            GL_iTitle = grow[1]
##            GL_iPop = grow[2]
        
            if GL_iNo == GL_no:
                line = GL_no + '\t' + GL_title + '\t' + GL_iTitle + '\t' + GL_link + '\t' + GL_cui + '\t' + GL_icd + '\t' + GL_cat + '\t' + GL_icdlong + '\n'
##                print line
##                sys.exit(0)
                print GL_no
                results.write(line)

    except IndexError as e:
        continue
    
results.close()
sys.exit(0)
