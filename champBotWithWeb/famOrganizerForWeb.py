import pandas as pd
import numpy as np
#import tkinter as tk
from pyscript import document
from getFamHeads import fams, heads, dict

def csvFile():
        file_path = document.querySelector("#champCSV").files[0] #input("give the filepath to the csv in string format i.e'/folder/folder/name.csv'")
        fam_heads = heads #input("who are the family heads? give response in ['name', 'name', 'name', ...]") #given in [,]
        fam_names = fams #input("what are the names of the families? given in the same format as previous.") #given in [,]
        fam_relations = dict

        #for fam in fam_names:
            #fam_heads_for_fam = input(f"for family {fam}, who are the heads? give in ['name', 'name',..] format") #
            #fam_relations[fam] = fam_heads_for_fam
        tbl = pd.read_csv(file_path) #rxc table

        tbl_names=dict()

        def getPrefs(tbl):
            tbl['Preferences'] = tbl['Prefs'].fillna(tbl['Preferences'])
            for name in fam_heads:
                tbl_name = f"{name}_table"
                tbl_names[tbl_name] = tbl[nameFilter(name)]
            for name in fam_names:
                tbl_name = f"{name}_table"
                tbl_names[tbl_name] = tbl[nameFilter(name)]
            return None

        def nameFilter(name): # checks whther a name is in pref returns array for T and F's rx1 filtered by whether a substring is in
            return tbl['Preferences'].str.count(nameRegexPrep(name))>0

        def nameRegexPrep(name): #takes a name and makes it a regex pattern
            regex = ''
            for letter in name:
                regex += f'[{letter}{letter.swapcase()}]+'
            return regex

        def combineTables(tables, relation): #goes through array of tables and combines based on a dictionary of keys
            joint_dict = dict()
            combined = pd.DataFrame()
            for fam in fam_relations: #heads [,], fam string
                heads = fam_relations[fam]
                fam_tbl = f"{fam}_table"
                head_tbls = [tbl_names[f'{head}_table'] for head in heads]
                #joint_dict[f"{fam}"] = tbl_names[fam_tbl].join(head_tbls)
                combined_head = pd.concat(head_tbls)
                combinedfamtbl = pd.concat([tbl_names[fam_tbl], combined_head])[['Email Address', 'First Name', 'Last Name', 'Discord Tag (ex. Gamer#1337)']]
                combinedfamtbl["fam"] = f"{fam}"
                joint_dict[f"{fam}"] = combinedfamtbl
                combined = pd.concat(objs = [combined, combinedfamtbl], ignore_index = True)
            return joint_dict, combined



        getPrefs(tbl)
        results, csv_results = combineTables(tbl_names, fam_relations)
        print("\n ______ Preliminary fam results in out.zip ______ \n")
        print_q = ""
        while print_q != "y" and print_q != "n" :
            print_q = input('Would you like to see the preview of the results? (y/n)')
            if print_q == "y":
                print(results)
            elif print_q == "n":
                print('ok')
            else:
                print("Please provide a valid input")

        compression_opts = dict(method='zip',
                                archive_name='out.csv')
        csv_results.to_csv('out.zip', index=False,
                  compression=compression_opts)
        return None
