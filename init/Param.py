# -*- coding: utf-8 -*-
from xml.dom import minidom

class Param:

    doc = None
    xmlpath = None
    params = dict()
    
    def __init__(self, xmlpath):
        self.xmlpath = xmlpath
        self.params['AnacondaPath01']=None
        self.params['AnacondaPath02']=None
        self.params['UIPath']=None        
        self.params['YMLPath']=None
        
    def init(self, xmlpath):
        self.xmlpath = xmlpath
        
    def read(self):
        self.doc = minidom.parse(self.xmlpath)
        
        # Read parameters
        self.params['AnacondaPath01']=self.doc.getElementsByTagName('AnacondaPath01')[0].childNodes[0].data
        self.params['AnacondaPath02']=self.doc.getElementsByTagName('AnacondaPath02')[0].childNodes[0].data
        self.params['UIPath']=self.doc.getElementsByTagName('UIPath')[0].childNodes[0].data
        self.params['YMLPath']=self.doc.getElementsByTagName('YMLPath')[0].childNodes[0].data
        
    def printParams(self):
        # Print parameters
        print('Params:')
        print(self.params)

        
    def create(self):

        self.doc = minidom.Document()
        
        # Create reft node
        reft = self.doc.createElement('MDDoc')
        self.doc.appendChild(reft)
        
        # Create parameter AnacondaPath01
        AnacondaPath01 = self.doc.createElement('AnacondaPath01')
        reft.appendChild(AnacondaPath01)
        AnacondaPath01.appendChild(self.doc.createTextNode('H:/ProgramFiles/Anaconda2/envs/env_test01/Library/bin'))
        self.params['AnacondaPath01']=AnacondaPath01.childNodes[0].data
        
        # Create parameter AnacondaPath01
        AnacondaPath02 = self.doc.createElement('AnacondaPath02')
        reft.appendChild(AnacondaPath02)
        AnacondaPath02.appendChild(self.doc.createTextNode('H:/ProgramFiles/Anaconda2/envs/env_test01/Library'))
        self.params['AnacondaPath02']=AnacondaPath02.childNodes[0].data
        
        # Create parameter UIPath
        UIPath = self.doc.createElement('UIPath')
        reft.appendChild(UIPath)
        UIPath.appendChild(self.doc.createTextNode('H:/cloud/cloud_data/Projects/MDDoc/qt/MDDoc_V04.ui'))
        self.params['UIPath']=UIPath.childNodes[0].data   
        
        # Create parameter YMLPath
        YMLPathPath = self.doc.createElement('YMLPath')
        reft.appendChild(YMLPathPath)
        YMLPathPath.appendChild(self.doc.createTextNode('H:/cloud/cloud_data/Projects/MDDoc/data/doc/REFT/mkdocs.yml'))
        self.params['YMLPath']=YMLPathPath.childNodes[0].data

    def write(self):
        # Write params to xml file
        f =  open(self.xmlpath, "w")
        f.write(self.doc.toprettyxml(indent = '   '))
        f.close()

param = Param('H:/cloud/cloud_data/Projects/MDDoc/init/init.xml')
