# Python-Tools
Simple scripts

## GetTiffPageCounts.py
This script was written to look for any TIFF files in a directory (recursively) to get the page counts using the n_frames attribute of the document using the PIL library. Output file is a CSV listing the full path to the document and the number of pages. Files that are unable to be read will show 0 pages.

## HandleRangedDocuments.py
Purpose built script to generate a number of copies of a document that meets certain naming conventions. Regex patterns are used to identify qualifying document names.
