import os

def NewFile(filename: str, dir: str, filetype: str="txt"):
    fullFileName = filename + "." + filetype
    fileDir = os.path.join(dir, fullFileName)
    with open(fileDir, "x") as f:
        pass

NewFile("hello", "", "json")