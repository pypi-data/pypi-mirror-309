import argparse
import sys
import subprocess
from pathlib import Path
import fnmatch

try:
    import pathspec
except ImportError:
    pathspec = None


def get_language_from_extension(file_path: Path) -> str:
    extension_to_language = {
        ".py": "python",
        ".rs": "rust",
        ".js": "javascript",
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".cs": "csharp",
        ".rb": "ruby",
        ".php": "php",
        ".json": "json",
        ".jsonc": "jsonc",
        ".md": "markdown",
        ".xml": "xml",
        ".sh": "bash",
    }
    return extension_to_language.get(file_path.suffix, "text")


def build_tree(
    directory: Path, tree_dict: dict[str, dict], ignore_list: list, gitignore_spec=None
):
    items = sorted(directory.iterdir())
    for item in items:
        if should_ignore(item.relative_to(directory), ignore_list, gitignore_spec):
            continue
        if item.is_dir():
            tree_dict[item.name] = {
                "path": str(item),
                "is_dir": True,
                "children": {},
            }
            build_tree(
                item, tree_dict[item.name]["children"], ignore_list, gitignore_spec
            )
        else:
            tree_dict[item.name] = {"path": str(item), "is_dir": False}


def format_tree(tree_dict: dict[str, dict], padding=""):
    lines = ""
    last_index = len(tree_dict) - 1
    for index, (name, node) in enumerate(tree_dict.items()):
        connector = "└──" if index == last_index else "├──"
        if node["is_dir"]:
            lines += f"{padding}{connector} {name}/\n"
            new_padding = padding + ("    " if index == last_index else "│   ")
            lines += format_tree(node["children"], new_padding)
        else:
            lines += f"{padding}{connector} {name}\n"
    return lines


def write_tree_to_file(
    directory: Path, output_handle, ignore_list: list, gitignore_spec=None
):
    tree_dict: dict[str, dict] = {}
    build_tree(directory, tree_dict, ignore_list, gitignore_spec)
    tree_str = format_tree(tree_dict)
    output_handle.write(tree_str.rstrip("\r\n") + "\n\n")


def append_to_file_markdown_style(
    relative_path: Path, file_content: str, output_handle
) -> None:
    language = get_language_from_extension(relative_path)
    output_handle.write(
        f"# File: {relative_path}\n```{language}\n"
        f"{file_content}\n```\n# End of file:"
        f" {relative_path}\n\n"
    )


def append_to_single_file(file_path: Path, git_path: Path, output_handle) -> None:
    if not file_path.is_file():
        return

    relative_path = file_path.relative_to(git_path)
    try:
        with file_path.open("r", encoding="utf-8") as f:
            file_content = f.read()
    except UnicodeDecodeError:
        return
    append_to_file_markdown_style(relative_path, file_content, output_handle)


def process_include_list(git_path: Path, output_handle, include_list: list) -> None:
    for relative_path in include_list:
        full_path = git_path / Path(relative_path)
        if not full_path.exists():
            print(f"Warning: Path does not exist: {relative_path}")
            continue
        if full_path.is_file():
            append_to_single_file(full_path, git_path, output_handle)
        elif full_path.is_dir():
            for file_path in full_path.rglob("*"):
                if file_path.is_file():
                    append_to_single_file(file_path, git_path, output_handle)


def process_path(
    git_path: Path, ignore_list: list, output_handle, gitignore_spec=None
) -> None:
    for file_path in git_path.rglob("*"):
        if not file_path.is_file():
            continue
        if should_ignore(file_path.relative_to(git_path), ignore_list, gitignore_spec):
            continue
        append_to_single_file(file_path, git_path, output_handle)


def should_ignore(
    path_relative_to_git_root: Path, ignore_list: list, gitignore_spec=None
) -> bool:
    path_str = str(path_relative_to_git_root)

    # Always ignore .git directory
    if path_str.startswith(".git"):
        return True

    # Check gitignore patterns
    if gitignore_spec:
        if path_relative_to_git_root.is_dir():
            path_str += "/"
        if gitignore_spec.match_file(path_str):
            return True

    # Check custom ignore patterns
    return any(fnmatch.fnmatch(path_str, pattern) for pattern in ignore_list)


def copy_to_clipboard_content(content: str) -> None:
    """Copy the given content to the clipboard using wl-copy."""
    try:
        process = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE)
        process.communicate(input=content.encode("utf-8"))
    except FileNotFoundError:
        print("Clipboard functionality requires 'wl-copy' to be installed.")
    except ValueError as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Process some files and directories.")
    parser.add_argument("path", help="Path to the git project directory.")
    parser.add_argument("-o", "--output", help="Output file path.")
    parser.add_argument(
        "-exc",
        "--exclude",
        nargs="*",
        help="List of files or directories to ignore (supports glob patterns).",
    )
    parser.add_argument(
        "-inc",
        "--include",
        nargs="*",
        help="List of files or directories to include "
        "(supports glob patterns). If specified only "
        "these paths will be included.",
    )
    parser.add_argument(
        "-se", "--skip-empty-files", action="store_true", help="Skip empty files."
    )
    parser.add_argument(
        "-cp",
        "--clipboard",
        action="store_true",
        help="Copy the output file content to clipboard.",
    )
    parser.add_argument(
        "-igi",
        "--ignoregitignore",
        action="store_true",
        help="Ignore .gitignore and .globalignore files.",
    )

    args = parser.parse_args()

    git_path = Path(args.path)

    if not git_path.is_dir():
        print(f"Error: Path not found or not a directory: {git_path}")
        sys.exit(1)

    ignore_list = args.exclude if args.exclude else []
    include_list = args.include if args.include else None

    # Handle .gitignore
    gitignore_spec = None
    if not args.ignoregitignore:
        if pathspec is None:
            print("Error: 'pathspec' module is required to parse .gitignore files.")
            print("Install it using 'pip install pathspec' or use -igi flag.")
            sys.exit(1)

        gitignore_patterns = []

        # Read .gitignore
        gitignore_path = git_path / ".gitignore"
        if gitignore_path.exists():
            with gitignore_path.open() as f:
                gitignore_patterns.extend(f.read().splitlines())

        # Read .globalignore
        globalignore_path = Path(__file__).parent / ".globalignore"
        if globalignore_path.exists():
            with globalignore_path.open() as f:
                gitignore_patterns.extend(f.read().splitlines())

        if gitignore_patterns:
            gitignore_spec = pathspec.PathSpec.from_lines(
                "gitwildmatch", gitignore_patterns
            )

    # Сначала собираем содержимое в буфер
    import io

    buffer = io.StringIO()

    if include_list is not None:
        process_include_list(git_path, buffer, include_list)
    else:
        write_tree_to_file(git_path, buffer, ignore_list, gitignore_spec)
        process_path(git_path, ignore_list, buffer, gitignore_spec)

    content = buffer.getvalue()
    buffer.close()

    if args.output:
        output_file = Path(args.output)
        with output_file.open("w", encoding="utf-8") as out_fh:
            out_fh.write(content)

        if args.clipboard:
            copy_to_clipboard_content(content)
            print(f"Contents from {output_file} copied to clipboard.")
    else:
        if args.clipboard:
            copy_to_clipboard_content(content)
            print("Contents copied to clipboard.")
        else:
            print(content)


if __name__ == "__main__":
    main()
