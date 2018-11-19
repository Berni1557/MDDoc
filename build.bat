rem ----------- Install MDDocGUI and create desktop shortcut -----------

pyinstaller --clean MDDocGUI.py
robocopy init dist/MDDocGUI/init /s /e
robocopy MDVariables dist/MDDocGUI/MDVariables /s /e
robocopy MDTemplates dist/MDDocGUI/MDTemplates /s /e
rem mklink /d "C:/Users/bernifoellmer/Desktop/Temp" "H:/cloud/cloud_data/Projects/MDDoc/dist/MDDocGUI/MDDocGUI.exe"