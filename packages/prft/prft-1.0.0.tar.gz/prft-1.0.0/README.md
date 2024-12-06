# Project File Tree (pft)

pft is a Python library designed to easily generate and display the file structure of a project, with support for .gitignore patterns. It allows you to quickly visualize the organization of files and directories within a specified project directory.

## Features
-	Generates a clear and visual representation of your project’s file structure.
-	Supports .gitignore and other ignore files, so you only see files relevant to the project.
-	Allows hiding hidden files (dotfiles) for a cleaner output.
- 

## Installation
Install pft via pip:
```bash
pip install pft
```

## Usage
Use pft in the terminal to display a project’s file structure.

**Basic Command**
```bash
pft path_to_project
```

You can also use . to specify the current directory if you are in the project directory:

```bash
pft .
```

### Options
- **--no-ignore**: Show all files, including those listed in .gitignore.
- **--no-dot**: Include hidden files (dotfiles) in the output.

**Example:**
```bash
pft path_to_project --no-ignore --no-dot
```

### Example Output

Running pft in a sample project directory might produce output like this:
```
project/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── config/
│       └── settings.py
├── .gitignore
├── README.md
└── requirements.txt
```
This output shows a hierarchical view of the files and directories in *path_to_project*, ignoring files specified in .gitignore (unless `--no-ignore` is used).

## License

This project is licensed under the MIT License.

## Author

Created by [trum-ok](https://github.com/Trum-ok) :p
