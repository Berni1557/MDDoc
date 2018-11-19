# -*- coding: utf-8 -*-
"""
yaml_class.py

Created on Mon Nov 12 13:23:39 2018

@author: Bernhard Foellmer
"""

import yaml

class YAML:
    
    def __init__(self):
        pass        

    def save(self, dictionary, filepath):
        with open(filepath, 'w') as filepath:
            yaml.dump(dictionary, filepath, default_flow_style=False)

    def load(self, filepath):
        dictionary = None
        with open(filepath, 'r') as stream:
            docs = yaml.load_all(stream)
            #print('docs', docs)
            dictionary = dict()
            for doc in docs:
                if doc:
                    for k,v in doc.items():
                        #print(k, "->", v)
                        dictionary[k]=v
        return dictionary



