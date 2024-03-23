from os import walk, listdir
from os.path import isfile, join, split
import pandas as pd
from PIL import Image
"""
Simple script to recursively iterate through a given directory looking
specifically for TIF files, which are then logged to a CSV along with their page
counts. Files with bad EXIF information are still listed but with 0 pages.

User needs to update rootpath and outpath to specify the folder to search and
the name and destination for the resulting data.
"""
__author__ = "Richard Parker"
__version__ = "1.0"
__last_modified__ = "2024-03-23"

def GetTiffPageCount(image):
    img = Image.open(image)
    return img.n_frames

rootpath = "C:where\\to\\look\\for\\TIFs"
outpath = join("C:where\\to\\store\\output", "Output Filename.csv")
filepaths = [join(dirpath,f) for (dirpath, dirnames, filenames) in walk(rootpath) for f in filenames]

tiffs = []
for f in filepaths:
    pagecount = 0
    if f.endswith(".tif"):
        try:
            pages = GetTiffPageCount(f)
        except UserWarning:
            print("Unable to read file at: " + f)
            pages = 0
        except:
            print("Unknown exception with file at: " + f)
            pages = 0
        tiffs.append((f, split(f)[1], pages))
        #print(f, pages)

tiffs_df = pd.DataFrame(tiffs).rename(columns = {0: "Filepath", 1: "Filename", 2: "Pages"})
tiffs_df.to_csv(outpath, index = False)
