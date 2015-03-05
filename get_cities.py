# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 19:48:49 2015

@author: maltimore
"""

import pickle
import re


def get_cities(filename):
    ''' Reads cities and ids from textfile '''
    
    citylist = []
    
    # Attention! The textfile given by the DWD is encoded in Latin-1.
    # Python3 uses utf-8 by default, so we have to specify it here.
    # In Python2 none of this will work, the open() function doesn't
    # even accept encode= as a parameter.
    with open(filename, 'rt', encoding='Latin-1') as text_file:
        
        # Read the first two lines, which we don't need.        
        text_file.readline()
        text_file.readline()
        
        for textline in iter(text_file):
            wordlist = re.sub("[^\w]", " ",  textline).split()
            
            # The city is the 8th. word in each line
            try:
                citylist.append([wordlist[0], wordlist[8], wordlist[9]])
            except IndexError:
                print('There was an indexerror, if this happened in ' + \
                      'the last line, this was expected')
    list_sorted = sorted(citylist, key= lambda line:line[1])
    return list_sorted
    
    
def delete_multiples(citylist):
    ''' Removes duplicate items from a list '''
    new_citylist = []
    citiesonly   = [] # this list is used to temporarilty store
                      # the cities and check whether it occured already
    
    for element in citylist:
        if element[1] not in citiesonly:
            new_citylist.append(element)
            citiesonly.append(element[1])

    return new_citylist


citylist           = get_cities('TU_Stundenwerte_Beschreibung_Stationen.txt')
citylist           = delete_multiples(citylist)

pickle.dump(citylist, open('current_cityfile.dump','wb'))