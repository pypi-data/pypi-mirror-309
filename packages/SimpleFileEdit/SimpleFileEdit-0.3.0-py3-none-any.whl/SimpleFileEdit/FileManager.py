import os

def NewFile(filename: str, path: str, filetype: str="txt"):

    fullFileName = filename + "." + filetype
    fileDir = os.path.join(path, fullFileName)

    with open(fileDir, "x") as f:
        pass



def EditFile(filename, content="This is the template content for SimpleFileEdit", filetype="txt",path=os.getcwd(), mode="add-to-end"):

    fullFileName = filename + "." + filetype
    fileDir = os.path.join(path, fullFileName)

    if os.path.isfile(fileDir):
        if mode == "add-to-end" or mode == "a":
            with open(fileDir, "a") as f:
                f.write(content)
        
        elif mode =="replace" or "r":
            with open(fileDir, "w") as f:
                f.write(content)
    else:
        return f"ERROR --- FILE {fileDir} DOES NOT EXIST"



def EditFileName(filename, newname, path=os.getcwd(), filetype="txt", newfiletype="OLD_FILE_TYPE_TEMP"):

    if newfiletype == "OLD_FILE_TYPE_TEMP":
        newfiletypeUpdated = filetype
    else:
        newfiletypeUpdated = newfiletype

    fullFileName = filename + "." + filetype
    fileDir = os.path.join(path, fullFileName)
    fullNewFileName = newname + "." + newfiletypeUpdated
    newFileDir = os.path.join(path, fullNewFileName)

    os.rename(fileDir, newFileDir)

