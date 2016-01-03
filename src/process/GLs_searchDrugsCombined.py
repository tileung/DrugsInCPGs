## Revised: 10/25/15
## Created: 09/29/15
## Adapted from IncludedGL_byCUI.py and IncludedGLs_byCUI_byTargetPop.pt

## Purpose: final list of included CPGs and their disease categories/GUIs COMBINED WITH Labels found in CPGs

import os
import sys
import csv

## Set path
path = ""

## Initiate file to save results
fName = path + "GLs_SearchedTerms_Combined.txt"
try:
    os.remove(fName)
    print("old file removed")
except OSError:
    pass

results_file = "GLs_SearchedTerms_Combined.tab"
results = open(results_file,"w")

## Identify files for comparison
drugsInGLs_list = path + "drugsInGuidelines_1018-manualValidation (completelist).txt"
GL_list = path + "IncludedGLs_byCUI_byPop.tab"

f = open(drugsInGLs_list, 'r')
freader = csv.reader(f, dialect = csv.excel_tab)

for frow in freader:

    try:
        GL_no = str(frow[0]) ##match to same key in GL_list
        GL_title = frow[1]
        labelMatched = frow[2]
        labelCount = str(frow[3])
        labelSource = frow[4]
        labelType = frow[5]
        labelValid = str(frow[7])
        
        g = open(GL_list, 'r')
        greader = csv.reader(g, dialect = csv.excel_tab)

        for grow in greader:
            GL_iNo = str(grow[0]) ## match to same key in drugsInGLs_list
            GL_cui = str(grow[4])
            GL_cat = grow[6]
        
            if GL_iNo == GL_no:
                line = GL_no + '\t' + GL_title + '\t' + GL_cui + '\t' + GL_cat + '\t' + labelMatched + '\t' + labelCount + '\t' + labelSource + '\t' + labelType + '\t' + labelValid + '\n'
##                print line
                results.write(line)

    except IndexError as e:
        continue
    
results.close()
sys.exit(0)
