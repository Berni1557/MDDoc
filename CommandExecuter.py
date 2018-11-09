# -*- coding: utf-8 -*-
from MDDoc import MDDoc
import os
import optparse

class CommandExecuter:
    
    parser = optparse.OptionParser()
    MD = MDDoc()
    opts = {}
    args = 0
    
    def __init__(self):

        strCommand=" \
        GRAPHML - Create .graphml file, \
        DOCU - Create pdf documentaion, \
        TEMPLATE - Create md file template, \
        TAG - Search md file by tags, \
        SEARCH - Search md file by name \
        SCRIPT - Execute md file related python script, \
        MDSTRUCT - Create folder structure out of a .graphml file, \
        "              
        parser = optparse.OptionParser(version='1.0.1', usage='MDDoc is a markdown based documentation tool')
        parser.add_option('-c', '--command', help='Command that is executed ' + strCommand, dest='command')
        parser.add_option('-i', '--inputfile', help='Filepath to root md file', dest='inputfile')
        parser.add_option('-o', '--outputfile', help='Filepath output', dest='outputfile')
        parser.add_option('-p', '--parameter', help='Command paramter', dest='parameter')
        (opts, args) = parser.parse_args()
        self.opts=opts;
        self.args=args;
        
    def execute(self):
        opts = self.opts     
        if opts.command == 'GRAPHML':
            print ("Creating .graphml file")
            # Check option existance
            if opts.inputfile is None or opts.outputfile is None:
                print ("An option is missing\n")
                exit(-1)        
            if not os.path.isfile(opts.inputfile):
                print ("Inputfile " + opts.inputfile + " does not exist.")
            folderpath=os.path.dirname(opts.outputfile)
            if not os.path.isdir(folderpath):
                print ("Outputfolder " + opts.outputfile + " for .graphml file does not exist.")   
            print ("Filepath to the root md file: " + opts.inputfile)
            print ("Folderpath of the .graphml file: " + opts.outputfile)
            self.docu(opts.inputfile, folderpath)
            
        elif opts.command == 'DOCU':
            print ("Creating pdf docu")
            # Check option existance
            if opts.inputfile is None or opts.outputfile is None:
                print ("An option is missing\n")
                exit(-1)        
            if not os.path.isfile(opts.inputfile):
                print ("Inputfile " + opts.inputfile + " does not exist.")
            folderpath=os.path.dirname(opts.inputfile)
            if not os.path.isdir(folderpath):
                print ("Outputfolder " + opts.outputfile + " for .pdf file does not exist.")   
            print ("Filepath to the root md file: " + opts.inputfile)
            print ("Folderpath of the .pdf file: " + opts.outputfile)
            self.docu(opts.inputfile, folderpath)
            
        elif opts.command == 'TEMPLATE':
            MDTemp=MDDoc()
            print ("Creating md file template")
            # Check option existance
            if opts.parameter is None or opts.outputfile is None:
                print ("An option is missing\n")
                exit(-1)        
            if not opts.parameter in MDTemp.MDTemplates:
                print ("Template " + opts.parameter + " not found in MDTemplates folder.")
            folderpath=os.path.dirname(opts.outputfile)
            if not os.path.isdir(folderpath):
                print ("Outputfolder " + opts.outputfile + " for .md file does not exist.")   
            print ("Template of the md file: " + opts.parameter)
            print ("Folderpath of the created .md file: " + opts.outputfile)
            self.template(opts.parameter, opts.outputfile)
         
        elif opts.command == 'TAG':
            print ("Searching md file by tags")
            # Check option existance
            if opts.inputfile is None or opts.parameter is None or opts.outputfile is None:
                print ("An option is missing\n")
                exit(-1)        
            if not os.path.isfile(opts.inputfile):
                print ("Inputfile " + opts.inputfile + " does not exist.")
            inputfile=opts.inputfile
            tagsstr=opts.parameter
            number=int(opts.outputfile)
            self.tag(inputfile, tagsstr, number)
         
        elif opts.command == 'SEARCH':
            print ("Searching md file by name")
            # Check option existance
            if opts.inputfile is None or opts.parameter is None or opts.outputfile is None:
                print ("An option is missing\n")
                exit(-1)        
            if not os.path.isfile(opts.inputfile):
                print ("Inputfile " + opts.inputfile + " does not exist.")
            inputfile=opts.inputfile
            name=opts.parameter
            show=opts.outputfile in ['True', 'true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
            self.search(inputfile, name, show)
        
        elif opts.command == 'SCRIPT':
            print ("Searching md file by name")
            # Check option existance
            if opts.inputfile is None:
                print ("An option is missing1\n")
                exit(-1)        
            if not os.path.isfile(opts.inputfile):
                print ("Inputfile " + opts.inputfile + " does not exist.")
            inputfile=opts.inputfile
            self.script(inputfile)
        elif opts.command == 'MDSTRUCT':
            print ("Creeating folder structure from .graphml file")
            # Check option existance
            if opts.inputfile is None or opts.parameter is None or opts.outputfile is None:
                print ("An option is missing1\n")
                exit(-1)        
            if not os.path.isfile(opts.inputfile):
                print ("Inputfile " + opts.inputfile + " does not exist.")
            folderpath=opts.outputfile
            if not os.path.isdir(folderpath):
                print ("Outputfolder " + opts.outputfile + " for folder structure does not exist.")   
            inputfile=opts.inputfile
            mdrootfilename=opts.parameter
            self.mdstruct(mdrootfilename, inputfile, folderpath)
        else:
           print ("Got a false command" +  opts.command)
           print( opts.command)
    
    def graphml(self, inputfile, folderpath): 
        folderpathmd=os.path.dirname(inputfile)
        filename=os.path.basename(inputfile)
        name=os.path.splitext(filename)[0]
        self.MD=MDDoc()
        self.MD.loadMDs(folderpathmd)
        self.MD.createGraph(filename)   
        self.MD.saveGraphML(folderpath + "\\" + name + ".graphml")
        self.MD.saveGraphMLPNG(folderpath + "\\" + name + ".png")
        
    def docu(self, inputfile, folderpath): 
        folderpathmd=os.path.dirname(inputfile)
        filename=os.path.basename(inputfile)
        name=os.path.splitext(filename)[0]
        self.MD=MDDoc()
        self.MD.loadMDs(folderpathmd)
        self.MD.createGraph(filename)
        self.MD.createPDFDoc(folderpath + "\\" + name + ".pdf")
    
    def template(self, parameter, filepath): 
        self.MD=MDDoc()
        self.MD.createMDTemplate(parameter, filepath)
    
    def tag(self, inputfile, tagsstr, number):
        folderpathmd=os.path.dirname(inputfile)
        filename=os.path.basename(inputfile)
        self.MD=MDDoc()
        self.MD.loadMDs(folderpathmd)
        self.MD.createGraph(filename)
        self.MD.searchTags(tagsstr, number)
     
    def search(self, inputfile, name, show):
        folderpathmd=os.path.dirname(inputfile)
        filename=os.path.basename(inputfile)
        self.MD=MDDoc()
        self.MD.loadMDs(folderpathmd)
        self.MD.createGraph(filename)
        self.MD.searchMD(name, show)
    
    def script(self, inputfile):
        folderpathmd=os.path.dirname(inputfile)
        filename=os.path.basename(inputfile)
        self.MD=MDDoc()
        self.MD.loadMDs(folderpathmd)
        self.MD.createGraph(filename)
        self.MD.exeScript()    
        
    def mdstruct(self, mdrootfilename, inputfile, folderpath):
        MD = MDDoc()
        MD.loadGraphML(inputfile)
        MD.renameGraph()
        MD.createMDStructure(mdrootfilename, folderpath)