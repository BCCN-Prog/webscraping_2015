''' This file gets the cities from the Deutscher Wetterdienst
    website file (a file of the name
    'TU_Stundenwerte_Beschreibung_Stationen.txt must already be in the
    current folder) and saves it into the file 'current_cityfile.dump'.'''

import pickle
import re # regular expressions package
import csv


#### FUNCTION DEFINITIONS #####################################################


def get_cities(filename):
    ''' Reads cities and ids from textfile '''
    
    print('Reading Deutscher Wetterdienst - File and extract cities...')
    citylist = []
    
    # Attention! The textfile given by the DWD is encoded in Latin-1.
    # Python3 uses utf-8 by default, so we have to specify it here.
    # In Python2 none of this will work, the open() function doesn't
    # even accept encode= as a parameter.
    with open(filename, 'rt', encoding='Latin-1') as text_file:
        
        # Read the first two lines, which we don't need.        
        text_file.readline()
        text_file.readline()

        lines = text_file.readlines()
        
        for idx, textline in enumerate(lines):
            
            wordlist = re.sub("[^\w]", " ",  textline).split()
            # The city is the 8th. word in each line
            try:
                citylist.append([wordlist[0], wordlist[8], wordlist[9]])
            except IndexError:
                # check if this IndexError was raised in the last line:
                if len(lines) == idx+1:
                    print("Checking exited cleanly at the end of the file.")
                else:
                    print('There was an indexerror while reading from' \
                           'the DW text file in line ' + str(idx))
                           
    list_sorted = sorted(citylist, key= lambda line:line[1])
    return list_sorted, text_file
    
    
def delete_multiples(citylist):
    ''' Removes duplicate items from a list. A duplicate is if
        there are several weather stations in the same city'''
    
    print('Deleting cities that occur multiple times in the city list ' + \
          'because the DW has several stations within one city...')
    duplicates   = 0
    new_citylist = []
    citiesonly   = [] # this list is used to temporarilty store
                      # the cities and check whether it occured already
    
    for element in citylist:
        # element is of the form ['ID', 'city', 'part_of_city']

        if element[1] not in citiesonly:
            new_citylist.append(element)
            citiesonly.append(element[1])
        else:
            duplicates+=1
    print("Deleted " + str(duplicates) + " duplicates.")

    return new_citylist



#### IMPLEMENTATION ###########################################################

citylist, text_file = get_cities('TU_Stundenwerte_Beschreibung_Stationen.txt')
citylist            = delete_multiples(citylist)

with open('citylist.txt', 'w', encoding='utf-8') as myfile:
        myfile.writelines(["%s\n" % item1  for item in citylist for item1 in item]) 

pickle.dump(citylist, open('current_cityfile.dump','wb'))