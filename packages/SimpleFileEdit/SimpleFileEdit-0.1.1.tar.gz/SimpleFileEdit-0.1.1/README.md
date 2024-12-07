
# SimpleFileEdit

**SimpleFileEdit** is a Python package designed to simplify file and folder operations. With this package, you can create, edit, and rename files and folders effortlessly.

## Installation

To install the package (once published), use pip:

    pip install SimpleFileEdit


---

## Features

### 1. NewFile
Create a new file with a specified name, type, and location.

Arguments:
- `filename` (str): The name of the file (without extension).
- `path` (str, optional): The directory path to create the file in. Defaults to the current working directory.
- `filetype` (str, optional): The file extension/type. Defaults to "txt".

Example:

    from SimpleFileEdit import NewFile
    NewFile("hello world", filetype="json")

# Creates "hello world.json" in the current working directory.

---

### 2. EditFile
Edit an existing file by adding new content or overwriting it.

Arguments:
- `filename` (str): The name of the file to edit (without extension).
- `content` (str, optional): The content to write to the file. Defaults to a template message.
- `filetype` (str, optional): The file extension/type. Defaults to "txt".
- `path` (str, optional): The directory path of the file. Defaults to the current working directory.
- `mode` (str, optional): The editing mode. Options are "add-to-end" or "overwrite". Defaults to "add-to-end".

Example:

    from SimpleFileEdit import EditFile
    EditFile("hello world", "Hello, World!", filetype="txt", path="/helloWorldFolder", mode="overwrite")
    # Overwrites the content of "hello world.txt" in "/helloWorldFolder" with "Hello, World!".

---

### 3. EditFileName
Rename a file and optionally change its file type.

Arguments:
- `filename` (str): The current name of the file (without extension).
- `filetype` (str, optional): The current file type. Defaults to "txt".
- `newname` (str): The new name for the file (without extension).
- `newfiletype` (str, optional): The new file type. Defaults to the current file type.
- `path` (str, optional): The directory path of the file. Defaults to the current working directory.

Example:

    from SimpleFileEdit import EditFileName
    EditFileName("hello world", "txt", "HELLO-WORLD", newfiletype="md", path="/helloWorldFolder")
    # Renames "hello world.txt" to "HELLO-WORLD.md" in "/helloWorldFolder".

---

### 4. NewFolder
Create a new folder in the specified location.

Arguments:
- `foldername` (str): The name of the folder to create.
- `path` (str, optional): The directory path to create the folder in. Defaults to the current working directory.

Example:

    from SimpleFileEdit import NewFolder
    NewFolder("helloWorldFolder")
    # Creates a folder named "helloWorldFolder" in the current working directory.

---

### 5. EditFolder
Rename an existing folder.

Arguments:
- `foldername` (str): The current name of the folder.
- `newfoldername` (str): The new name for the folder.
- `path` (str, optional): The directory path of the folder. Defaults to the current working directory.

Example:

    from SimpleFileEdit import EditFolder
    EditFolder("helloWorldFolder", "helloworldFOLDER")
    # Renames "helloWorldFolder" to "helloworldFOLDER" in the current working directory.

---

## Example Usage

Here’s a complete example of how to use SimpleFileEdit:

    from SimpleFileEdit import NewFile, EditFile, EditFileName, NewFolder, EditFolder
    
    # Create a new folder
    NewFolder("exampleFolder")
    
    # Create a new file in the folder
    NewFile("example", path="./exampleFolder", filetype="txt")
    
    # Edit the file's content
    EditFile("example", "This is new content.", filetype="txt", path="./exampleFolder", mode="overwrite")
    
    # Rename the file
    EditFileName("example", "txt", "new_example", path="./exampleFolder")
    
    # Rename the folder
    EditFolder("exampleFolder", "newExampleFolder")

---

## Future Features (Planned)
- File deletion functionality.
- Folder deletion functionality.
- Copying files and folders.
- Enhanced error handling and logging.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new branch (e.g., `feature-new-functionality`).
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License.

---

## Author

Developed by BravestCheetah. For questions, feedback, or feature requests, feel free to reach out.
