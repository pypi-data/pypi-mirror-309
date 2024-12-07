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
    return f"SUCESSFULLY WROTE {content} TO {fileDir}"