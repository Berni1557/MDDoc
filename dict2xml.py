# -*- coding: utf-8 -*-
from xml.dom.minidom import Document
from xml.dom.minidom import parse, parseString


def iterate_children(parent):
    child = parent.firstChild
    while child != None:
        yield child
        child = child.nextSibling
        
class dict2xml(object):
    doc     = Document()
    Vmap = dict()
    def __init__(self, Vmap):
        self.doc = Document()
        self.Vmap = Vmap
        root = self.doc.createElement('VARIABLES')
        self.doc.appendChild(root)
        self.build(root, Vmap)

    def build(self, root, Vmap):
        for key in Vmap:
            node = self.doc.createElement(key)
            text = self.doc.createTextNode(Vmap[key])
            node.appendChild(text)
            root.appendChild(node)

    def display(self):
        print(self.doc.toprettyxml(indent="  "))

    def save(self, filepath):
        f = open(filepath, "w")
        f.write(self.doc.toprettyxml(indent="  "))
        f.close()
       
    def load(self, filepath):
        self.doc = parse(filepath)
        NodeList=self.doc.childNodes
        self.Vmap = dict()
        for n in NodeList:
            NodeList1=n.childNodes 
            for n1 in NodeList1:
                NodeList2=n1.childNodes 
                for n2 in NodeList2:
                    self.Vmap[n1.tagName]=n2.nodeValue
       
       