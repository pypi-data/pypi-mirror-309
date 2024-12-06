import os
import argparse
from pathspec import PathSpec


def load_gitignore_patterns(root_path):
    gitignore_path = os.path.join(root_path, ".gitignore")
    try:
        with open(gitignore_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return PathSpec.from_lines("gitwildmatch", [])
    
    patterns = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    return PathSpec.from_lines("gitwildmatch", patterns)


def generate_tree(root_path, prefix=" ", ignore_dot=True, ignore=True, gitignore_spec=None):
    tree = ""
    items = os.listdir(root_path)
    
    directories = sorted([name for name in items if os.path.isdir(os.path.join(root_path, name))])
    files = sorted([name for name in items if os.path.isfile(os.path.join(root_path, name))])
    
    items: list[str] = directories + files

    for index, name in enumerate(items):
        if ignore_dot and name.startswith(".") and name not in ['.gitignore', '.dockerignore', '.env']:
            continue
        
        path = os.path.join(root_path, name)

        if ignore and gitignore_spec and gitignore_spec.match_file(os.path.relpath(path, root_path)):
            continue

        is_last = index == len(items) - 1
        connector = "└── " if is_last else "├── "
        
        tree += f"{prefix}{connector}{name}\n"
        
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            tree += generate_tree(path, prefix + extension, ignore_dot, ignore, gitignore_spec)
    
    return tree


def main():
    parser = argparse.ArgumentParser(description="Generate a file tree structure of a project.")
    parser.add_argument("root_path", nargs="?", default=".", help="Root directory of the project (default: current directory)")
    parser.add_argument("--no-ignore", action="store_false", help="Do not ignore files from .gitignore")
    parser.add_argument("--no-dot", action="store_false", help="Do not ignore dotfiles (hidden files)")
    parser.add_argument("--prefix", default=" ", help="Prefix for tree structure lines (default: space)")

    args = parser.parse_args()

    root_path = os.path.abspath(args.root_path)
    gitignore_spec = load_gitignore_patterns(root_path) if args.no_ignore else None

    tree = generate_tree(root_path, prefix=args.prefix, ignore_dot=args.no_dot, ignore=args.no_ignore, gitignore_spec=gitignore_spec)
    print(tree)


if __name__ == "__main__":
    main()
