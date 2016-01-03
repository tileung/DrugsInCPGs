# DrugsInCPGs
Drugs and Diseases in CPGs

1. Processing of Guidelines
 for 15 chronic conditions

ngc_rss_guidelineList.txt - Full list of NGC guidelines (identifier, title, location, UMLS CUI)
icd9_cui.txt - Full mapping of ICD to UMLS CUI
MedicareCDW_ICDcodes.txt - Subset of 15 chronic conditions ( with ICD codes)
MedicareCDW_CUIs.tab - List of 15 chronic conditions with mappings between ICD and UMLS CUIs 

IncludedGLs_byCUI.py - Filters the full list of guidelines to those that refer to the 15 chronic conditions
unique_IncludedGLs_byCUI.txt -> a unique list of guidelines for the 15 chronic conditions

GLTargetPop - exclusions (pregnant, children, wrong dx).xlsx  - Manually excluded list

IncludedGLs_byCUI_byTargetPop.py - Generates the final list of guidelines
IncludedCPGs_popExclusions1018.txt - Final list of 377 guidelines for the 15 chronic conditions


2. Retrieval of drug labels

getlabels.php - gets drug labels from multiple sources (ATC, CHEBI, DrugBANK, MeSH, NCIT, NDFRT, RxNORM)

searchDrugsCPG.py - search the CPGs with the drug labels

