from os import walk, listdir
from os.path import getctime, getsize, isfile, join, split, splitext
import pandas as pd
from PIL import Image
import PyPDF2
import time

"""
Simple script to recursively iterate through a given directory looking for TIF
or PDF files, which are then logged to a CSV along with their page
counts. Files with bad or unreadable data are still listed but with 0 pages.

User needs to update rootpath and outpath to specify the folder to search and
the name and destination for the resulting data.
"""

__author__ = "Richard Parker"
__version__ = "1.0"
__last_modified__ = "2024-03-26"

def GetPdfPageCount(file):
    with open(file, "rb") as currentPdf:
        pdfreader = PyPDF2.PdfReader(currentPdf)
        print(len(pdfreader.pages))
        return (len(pdfreader.pages))
    
def GetTiffPageCount(image):
    img = Image.open(image)
    print(str(img.n_frames))
    return img.n_frames

def GetCreateTimeIso(filepath):
    time_object = time.strptime(time.ctime(getctime(filepath)))
    return time.strftime("%Y-%m-%d %H:%M:%S", time_object)

rootpath = "C:\\"
outpath = join("C:\\", "TEST OUTPUT.csv")
filepaths = [join(dirpath,f) for (dirpath, dirnames, filenames) in walk(rootpath) for f in filenames]

documentcount = 0
zeropagecount = 0
errorcount = 0
totalpages = 0

#extensionslist = [".pdf", ".tif"]
filelist = []
for fp in filepaths:
    pagecount = 0
    splitpath = splitext(fp)
    ext = splitpath[1]
    try:
        match ext:
            case ".pdf":
                pagecount = GetPdfPageCount(fp)
            case ".tif":
                pagecount = GetTiffPageCount(fp)
            case default:
                pagecount = 0
                zeropagecount += 1
    except UserWarning:
        print("Unable to read file at: " + fp)
        pagecount = 0
        errorcount += 1
    except:
        print("Unknown exception with file at: " + fp)
        pagecount = 0
        errorcount += 1
    try:
        filelist.append((fp, pagecount, GetCreateTimeIso(fp), getsize(fp)))
    except OSError:
        pass

    documentcount += 1
    totalpages += pagecount

files_df = pd.DataFrame(filelist).rename(columns = {0: "Filepath", 1: "Pagecount", 2: "CreateTime", 3: "Bytes"})
files_df.to_csv(outpath, index = False)

print("Documents scanned:     " + str(documentcount))
print("Zero page documents:   " + str(zeropagecount))
print("Errored documents:     " + str(errorcount))
print("Total pages:           " + str(totalpages))