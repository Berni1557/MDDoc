# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
import os.path
import glob
import ntpath
import re
from dict2xml import dict2xml
import os, sys, subprocess
import collections
import webbrowser
import shutil
from subprocess import call
import yaml

class MDDoc:

    graph = nx.Graph()
    MDList = []
    variables = dict()
    xml = dict2xml([])
    MDTemplates = [];
    
    def __init__(self):
        self.graph = nx.Graph()
        self._loadMDTemplates()
        currentpath=os.path.dirname(os.path.abspath(__file__))
        variablespath=currentpath + "\\MDVariables\\MDVariables.xml"
        self.loadVariables(variablespath)

    def loadGraphML(self, filename):
        self.graph=nx.read_graphml(filename)
        
    def saveGraphML(self, filename):
         nx.write_graphml(self.graph, filename)
        
    def drawGraph(self):
        f = plt.figure()
        nx.draw(self.graph, ax=f.add_subplot(111), with_labels=True)
        
    def saveGraphMLPNG(self, filename):
        f = plt.figure()
        nx.draw(self.graph, ax=f.add_subplot(111), with_labels=True)
        f.savefig(filename, format="PNG")
        
    def loadMDs(self, folderpath):
        print("Loading md files")
        self._getsubMDs(folderpath)
        
    def createGraph(self, filename):
        self._extractMDs(filename)
       
    def openMD(self, filenames):       
        for fileMD in filenames:
            print("Opening md file: " + fileMD)
            webbrowser.open(fileMD)
        
        
    def ckeckMDLinks(self):
        print("Checking unreferenced md files:")
        for x in self.MDList:
            found=False
            for y,data in self.graph.nodes(data=True):
                if(x==y):
                    found=True
                    break
            if not found:
               print("Unreferenced document: " + x) 
                            
    def renameGraph(self):
        print("Renaming graph")
        graphmap=nx.get_node_attributes(self.graph, 'label')
        self.graph=nx.relabel_nodes(self.graph,graphmap)
        
    def searchMD(self, filename, show=False):
        print("Searching123")
        print("Searching md file '" + filename + "'")
        for fileMD,data in self.graph.nodes(data=True):
            n=fileMD.find(filename)
            if n > -1:
                print("Found md file '" + filename + "' in '" + fileMD +"'")
                if show:
                    self.openMD([fileMD])

    def searchTags(self, strtag, number=0):
        print("Searching tags in md files")
        strtag=strtag.replace(", ", ",")
        strtag=strtag.replace(" ,", ",")
        tags=strtag.split(',')
        scoreList=[];
        NumDocs=3;
        fileList=[];
        for fileMD,data in self.graph.nodes(data=True):
            fileList.append(fileMD)
            file = open(fileMD, "r")
            text = file.read()
            file.close()
            algo = 1;
            score = self._searchTag(algo,text,tags)
            scoreList.append(score)
        idxAll = [scoreList.index(x) for x in sorted(scoreList)]
        idx=idxAll[len(idxAll)-NumDocs : len(idxAll)]
        docs = [fileList[i] for i in idx]
        docs = docs[::-1]
        sc = [scoreList[i] for i in idx]
        sc = sc[::-1]
        for i in range(0,number):
            print(" Document: " + docs[i] + " Score: "+ str(round(sc[i],5)))
            self.openMD([docs[i]])
        
    def checkDocu(self):
        print("checkDocu")
        
    def exeScript(self):
        print("Executing all md file related python scripts")
        for fileMD,data in self.graph.nodes(data=True):
            folderpath=os.path.dirname(fileMD)
            filename=os.path.basename(fileMD)
            name=os.path.splitext(filename)[0]
            scriptfile=folderpath + "\\" + name + ".py"
            print(scriptfile)
            if os.path.isfile(scriptfile):
                returnValue=subprocess.call("python " + scriptfile)
                if returnValue==0:
                    print("Execution of " + scriptfile + " SUCCEDED")
                else:
                    print("Execution of " + scriptfile + " FAILED with code: " + str(returnValue))

    def createMDTemplate(self, template, filepath, templatespath=None):
        print("Creating md file template") 
        if templatespath is None:
            currentpath=os.path.dirname(os.path.abspath(__file__))
            templatespath=currentpath + '\\MDTemplates'
        src=templatespath + '\\' + template + '.md'
        dst=filepath
        print(src)
        print(dst)
        shutil.copyfile(src, dst)
        file = open(dst, "r+")
        text = file.read()
        for key in self.variables.keys():
            strkey="%" + key + "%"
            text = text.replace(strkey, self.variables[key])
        file.seek(0)
        file.write(text)
        file.close()
        
        
    def createPDFDoc(self, filepath):
        """Create a pdf file
        
        Create bla
        
        Parameters
        ----------
        filepath : string
           Filepath to the pdf file
           
        """
        print("Starting pdf creation")
        strMD=""
        for fileMD,data in self.graph.nodes(data=True):
            if not os.path.isfile(fileMD):
                sys.exit("Error: " + fileMD + " does not exist")
            if not fileMD.endswith("md" or "markdown"):
                 sys.exit(fileMD + " is not a markdown file");
            print("Found file: " + fileMD)
            strMD = strMD + " " + fileMD
        cmd = "pandoc --latex-engine=xelatex -s -o " + filepath + strMD	
        print("Starting file conversion.")
        if subprocess.call(cmd) != 0:
            print("Conversion failed")
        else:
            print("Saving pdf file to: " + filepath)
            print("Conversion successfull")
        
    def checkMultiDef(self):
        print("Checking multiple occurance of md files")       
        fileList=[];
        for fileMD,data in self.graph.nodes(data=True):
            fileList.append(ntpath.basename(fileMD))
        fileList.append('Manual.md')       
        counter=collections.Counter(fileList)
        for key in counter:
            value = counter[key]
            if value > 1:
                print("Multiple occurance found of md file: '" + key + "'")

        
    def createMDStructure(self, rootnode, folderpath):
        print("createMDStructure")
        self._getneighbors(rootnode, folderpath)

    def replaceVariables(self):
        print("replaceVariables")
        for x,data in self.graph.nodes(data=True):
            file = open(x, "r+")
            text = file.read()
            for key in self.variables.keys():
                strkey="%" + key + "%"
                text = text.replace(strkey, self.variables[key])
            file.seek(0)
            file.write(text)
            file.close()

        
    def loadVariables(self, filepath=None):  
        if filepath is None:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            filepath=current_dir + "\\variables.xml"      
        self.xml.load(filepath)
        self.variables = self.xml.Vmap
        
    def initVariables(self):
        print("initVariables")  
        self.variables = {
         'PERSON' : 'Max Mustermann',
         'COMPANY' : 'Muster Institut',
         'EMAIL' : 'max.mustermann@musterinstitut.de'
         }
        self.xml=dict2xml(self.variables)
        
    def saveVariables(self, filepath=None):
        print("saveVariables")   
        if filepath is None:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            filepath=current_dir+"\\variables.xml"     
        self.xml.save(filepath)
        
    def createGit(self, folderpath):
        print("createGit") 
        strgit = "git init " + folderpath
        print(strgit)
        os.system(strgit)
        strgitignore = folderpath + "\.gitignore"
        print(strgitignore) 
        file = open(strgitignore, "w+") 
        text = "\n".join(['*', '!*/', '!*.md', ])
        file.write(text)
        file.close()
        
    def _getneighbors(self, node, nodepath):
        # Create directory
        directory=nodepath + '\\' + node
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create markdown file
        filename=directory + '\\' + node + '.md'
        if not os.path.isfile(filename):
            open(filename, 'x')

         # Iterate over getneighbing nodes
        NodeList=self.graph.neighbors(node)
        for x in NodeList:
            self._getneighbors(x, directory)

    def _getsubMDs(self, folderpath):
        str1 = folderpath + "\\*.md"
        fileList = glob.glob(str1) 
        self.MDList = self.MDList + fileList
        subdirs = [d for d in os.listdir(folderpath) if os.path.isdir(os.path.join(folderpath, d))]
        for x in subdirs:
            fpath = folderpath + "\\" + x
            self._getsubMDs(fpath)
        
    def _extractMDText(self, text):      
        MDLinks=[]
        p1 = re.compile("\.md\)")
        p2 = re.compile("\]\(")
        list1=p1.split(text)
        for x in list1:
            list2=p2.split(x)
            if len(list2)==2:
                path=list2[1]
                MDLinks=MDLinks + [path + ".md"]
        return MDLinks
    
        
    def _extractMDs(self, filename):
        for x in self.MDList:
            ind=x.find(filename)
            if ind>-1:
                self.graph.add_node(x)
                filepath=os.path.dirname(os.path.abspath(x))
                file = open(x)
                text = file.read()
                MDLinks=self._extractMDText(text)            
                MDLinks = [ filepath+"\\"+y for y in MDLinks ]
                for y in MDLinks:
                    self.graph.add_node(y)
                    self.graph.add_edge(x,y) 
                    self._extractMDs(y)
                return MDLinks
            
    def _searchTag(self, algo,text,tags):
        if algo==1:
            occurences = 0
            length = 0
            score = 0
            for tag in tags:
                occurences=occurences + text.count(tag)
                length=length + len(text)
            if(length>0):
                score = occurences / length
            else:
                score = 0
            return score
    def _loadMDTemplates(self):
        currentpath=os.path.dirname(os.path.abspath(__file__))
        strtemplate=currentpath + "\\MDTemplates\\*.md"
        fileList = glob.glob(strtemplate)
        for filepath in fileList:
            filename=os.path.basename(filepath)
            name=os.path.splitext(filename)[0]
            self.MDTemplates.append(name)
        
    def createMKDocs(self, sourceFolder, destinationFolder, YMlFilepath):
        print("createMKDocs")
        
        with open(YMlFilepath) as f:
            list_doc = yaml.load(f)
            for sense in list_doc:
                #sense["site_dir"] = "H:/cloud/cloud_data/Projects/MDDoc/data/doc/REFT/site123"
                print(sense)
                
        
        stream = open(YMlFilepath, 'r')
        data = yaml.load(stream)        
        data['site_dir'] = destinationFolder
        data['docs_dir'] = sourceFolder
        with open(YMlFilepath, 'w') as yaml_file:
            yaml_file.write( yaml.dump(data, default_flow_style=False))
            
        
        config = "--config-file=" + YMlFilepath
        source = "--docs_dir=" + sourceFolder
        site = "--site_dir=" + destinationFolder
        print('config1',config)
        print('sourceFolder1',source)
        print(os.path.isdir(sourceFolder))
        print('destinationFolder1',site)
        print(os.path.isdir(destinationFolder))
        call(["mkdocs", "build", config])
        #mkdocs build --config-file=H:/cloud/cloud_data/Projects/MDDoc/data/doc/REFT/mkdocs.yml
        #call(["mkdocs", "build", "--config-file=H:/cloud/cloud_data/Projects/MDDoc/data/doc/REFT/mkdocs.yml", "--site_dir==H:/cloud/cloud_data/Projects/MDDoc/data/doc/REFT/site2"])




