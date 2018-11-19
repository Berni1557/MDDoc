# MDDoc
Markdown documentation tool

## Installation with conda
- conda create -n env_MDDoc python=3.6
- activate env_MDDoc
- conda install -c conda-forge mkdocs 
- pip install mkdocs-htmlproofer-plugin
- pip install beautifulsoup4
- conda install -c anaconda networkx
- conda install -c anaconda networkx 
- conda install -c anaconda pyqt
- conda install -c conda-forge matplotlib
- conda install -c anaconda pyqt
- conda install -c conda-forge pyinstaller 
- pip install pyqt5

conda update anaconda

## Start doc tool

## Start server
- python -m http.server 8000

## Create executable
pyinstaller --clear MDDocGUI.px

-> Creats a dist folder with all dependencies

- Copy init folder to dist\MDDocGUI
- Copy MDVariables folder to dist\MDDocGUI

