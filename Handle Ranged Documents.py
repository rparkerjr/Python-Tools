from genericpath import isfile
import re
import os
import shutil
"""
.Description
Scans folder for documents using a specific naming convention. For
those documents meeting the condition, the name is parsed and multiple
copies are made in the same folder.

Two diferent regex patterns are used to flag documents, with the key info
being the double-dashes: "--" and the numbers on either side of them.
     \d\d-\d\d\d\d-\d\d\d--\d\d\d
     \d\d-\d\d\d\d--\d\d\d\d

.Usage
Update the range of folders to reflect the current folders being scanned
and then execute the code. (Future version will allow recursion.)
.Author
Richard Parker
.Version
    1.0     2023-11-08
    1.1     2023-11-22
"""

watchFolder = "Z:"

def LPad(num, width = 3):
    outString = (("0" * width) + str(num))[-width:]
    return outString

def MakeCopies(original, fileList):
    #[shutil.copyfile(original, file) for file in fileList]
    for file in fileList:
        # check for existence first
        if os.path.isfile(file):
            #shutil.copyfile(original, file + " from code")
            print("Filename already existed: " + file)
            print("Created new file: " + file + " from code")
        else:
            #shutil.copyfile(original, file)
            print("Created file: " + file)
    
def Parse3(folder, filename):
    original = os.path.join(folder, filename)
    root = filename[:8]
    firstNumber = int(filename[8:11])
    lastNumber = int(filename[13:16])
    fileRange = range(firstNumber, lastNumber + 1)

    outputNames = [root + LPad(i, 3) for i in fileRange]
    # Land Use tag
    if re.search("Land", filename) != None:
        outputNames = [name + " Land Use" for name in outputNames]
    # Full path and extension, change to .tif as needed
    outputNames = [os.path.join(folder, name) + ".tif" for name in outputNames]
    print(outputNames)
    MakeCopies(original, outputNames)

def Parse4(folder, filename):
    original = os.path.join(folder, filename)
    root = filename[:3]
    tail = "-000"
    firstNumber = int(filename[3:7])
    lastNumber = int(filename[9:13])
    fileRange = range(firstNumber, lastNumber + 1)

    outputNames = [root + LPad(i, 4) + tail for i in fileRange]
    # Land Use tag
    if re.search("Land", filename) != None:
        outputNames = [name + " Land Use" for name in outputNames]
    # Full path and extension, change to .tif as needed
    outputNames = [os.path.join(folder, name) + ".tif" for name in outputNames]
    print(outputNames)
    MakeCopies(original, outputNames)

## Main body begins here
rootPath = "Z:"
folders = range(230411, 230453)
for f in folders:
    folderpath = os.path.join(rootPath, str(f))
    filenames = os.listdir(folderpath)
    #[print(f) for f in filenames]

    pattern3 = "\d\d-\d\d\d\d-\d\d\d--\d\d\d"
    pattern4 = "\d\d-\d\d\d\d--\d\d\d\d"
    for file in filenames:
        match3 = re.search(pattern3, file)
        match4 = re.search(pattern4, file)
        fullpath = os.path.join(folderpath, file)
        if match3 != None:
            Parse3(folderpath, file)
        elif match4 != None:
            Parse4(folderpath, file)
