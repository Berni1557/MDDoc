# -*- coding: utf-8 -*-
from CommandExecuter import CommandExecuter


welcomestr=" \
MDDoc is a markdown based documentation tool. \n \
Example of usage: \n \
python main.py -c GRAPHML -i D:\Entwicklerrunde\MDDoc\Graph\A5-Docu\A5-Docu.md -o D:\Entwicklerrunde\MDDoc\Graph\A5-Docu\grapp123.graphml \n \
python main.py -c DOCU -i D:\Entwicklerrunde\MDDoc\Graph\A5-Docu\A5-Docu.md -o D:\Entwicklerrunde\MDDoc\Graph\A5-Docu\Docu.pdf \n \
python main.py -c TEMPLATE -p REPOSITORY -o D:\Entwicklerrunde\MDDoc\Graph\A5-Docu\MyRepo.md \n \
python main.py -c TAG -i D:\Entwicklerrunde\MDDoc\Graph\A5-Docu\A5-Docu.md -p \"Installation, Windows\" -o 2 \n \
python main.py -c SEARCH -i D:\Entwicklerrunde\MDDoc\Graph\A5-Docu\A5-Docu.md -p Installation -o True \n \
python main.py -c SCRIPT -i D:\Entwicklerrunde\MDDoc\Graph\A5-Docu\A5-Docu.md \n \
python main.py -c MDSTRUCT -i D:\Entwicklerrunde\MDDoc\MDGraph01.graphml -p A5-Docu -o D:\Entwicklerrunde\MDDoc\test \n \
Using Environmental variables: \n \
python %MD% -c TEMPLATE -p CAD -o C:\temp\A5-CAD.md \n \
"
print(welcomestr)
CE=CommandExecuter()
CE.execute()


#from MDDoc import MDDoc
#MD = MDDoc()
#MD.createGit("Q:\\OE400_Gruppenplatte\\oe410\\01_Projekte\\144452_BeMobil\\TPB-A5_VR-Spiegeltherapie docu")
