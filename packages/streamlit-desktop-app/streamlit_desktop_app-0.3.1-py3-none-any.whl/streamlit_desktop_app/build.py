import argparse
import ast
import os
import sys
import tempfile
from typing import Optional, Dict, List, Union
import PyInstaller.__main__


def extract_imports(script_path: str) -> List[str]:
    """Extract all top-level imported modules from the given script."""
    imports = set()

    with open(script_path, "r") as file:
        tree = ast.parse(file.read(), filename=script_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(
                    alias.name.split(".")[0]
                )  # Capture only the top-level module
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(
                    node.module.split(".")[0]
                )  # Capture only the top-level module

    return list(imports)


def parse_streamlit_options(
    options: Optional[Union[List[str], Dict[str, str]]],
) -> Optional[Dict[str, str]]:
    """
    Parse Streamlit options from either a list of arguments or a dictionary.

    Args:
        options: A list of arguments (e.g., ["--theme.base", "dark"]) or a dictionary.

    Returns:
        A dictionary of options (e.g., {"theme.base": "dark"}).
    """
    if not options:
        return None

    if isinstance(options, dict):
        # If already a dictionary, return as is
        return options

    options_dict = {}
    current_key = None

    for token in options:
        if token.startswith("--"):
            # Strip the leading '--' and prepare for a new key
            if "=" in token:
                key, value = token.lstrip("-").split("=", 1)
                options_dict[key] = value
            else:
                current_key = token.lstrip("-")
                options_dict[current_key] = (
                    True  # Assume flag is True unless overridden
                )
        else:
            # This token is the value for the last key
            if current_key:
                options_dict[current_key] = token
                current_key = None  # Reset after value assignment

    return options_dict


def build_executable(
    script_path: str,
    name: str,
    script_type: str="raw",
    raw_script_path: Optional[str] = None, 
    icon: Optional[str] = None,
    pyinstaller_options: Optional[List[str]] = None,
    streamlit_options: Optional[list[str]] = None,
):
    """
    Build an executable using PyInstaller with explicit script type.

    Args:
        script_path: Path to the wrapped or raw Streamlit script.
        name: Name of the output executable.
        script_type: Type of script ('raw' or 'wrapped').
        raw_script_path: Path to the raw Streamlit script (if script_type is 'wrapped').
        icon: Path to the icon file for the executable.
        pyinstaller_options: Additional arguments to pass to PyInstaller.
        streamlit_options: Additional Streamlit CLI options.
    """
    if not os.path.exists(script_path):
        sys.exit(f"Error: The script '{script_path}' does not exist.")

    script_path = os.path.abspath(script_path)
    if icon:
        icon = os.path.abspath(icon)

    if script_type == "raw":
        raw_script_path  = script_path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_wrapper:
            wrapper_path = tmp_wrapper.name
            wrapper_content = f"""
import os
import sys

from streamlit_desktop_app import start_desktop_app

def get_script_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "{os.path.basename(script_path)}")
    else:
        return os.path.join(os.path.dirname(sys.executable), "{os.path.basename(script_path)}")

if __name__ == "__main__":
    if '_PYI_SPLASH_IPC' in os.environ:
        import pyi_splash
        pyi_splash.close()
    start_desktop_app(get_script_path(), title="{name}", options={parse_streamlit_options(streamlit_options)})
"""
            tmp_wrapper.write(wrapper_content.encode())

    elif script_type == "wrapped":
        wrapper_path = script_path
        if not raw_script_path:
            sys.exit("Error: --raw-script-path must be provided for wrapped scripts.")
    else:
        sys.exit(f"Error: Invalid script type '{script_type}'. Use 'raw' or 'wrapped'.")

    imports = extract_imports(raw_script_path)

    args = [
        "--name",
        name,
        "--paths",
        ".",
        "--collect-all",
        "streamlit",
        "--copy-metadata",
        "streamlit",
        "--add-data",
        f"{script_path}:.",  # Add the script as a data file
        wrapper_path,
    ]


    # Add raw script as a data file
    if script_type == "raw":
        args.extend(["--add-data", f"{raw_script_path}:."])

    for pkg in imports:
        args.extend(["--hidden-import", pkg])

    if icon:
        args.extend(["-i", icon])

    if pyinstaller_options:
        args.extend(pyinstaller_options)

    PyInstaller.__main__.run(args)

    if wrapper_path != script_path:
        os.remove(wrapper_path)


def main():
    parser = argparse.ArgumentParser(
        description="Build a standalone executable for your Streamlit desktop app."
    )
    parser.add_argument(
        "--script", required=True, help="Path to the Streamlit script to be packaged."
    )
    parser.add_argument("--name", required=True, help="Name of the output executable.")
    parser.add_argument("--icon", help="Path to the icon file for the executable.")
    parser.add_argument(
        "--script-type",
        choices=["raw", "wrapped"],
        default="raw",
        help="Type of script ('raw' or 'wrapped').",
    )
    parser.add_argument(
        "--raw-script",
        help="Path to the raw Streamlit script (required if script-type is 'wrapped').",
    )
    parser.add_argument(
        "--pyinstaller-options",
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to PyInstaller.",
    )
    parser.add_argument(
        "--streamlit-options",
        nargs=argparse.REMAINDER,
        help="Additional Streamlit CLI options.",
    )
    args = parser.parse_args()

    pyinstaller_options = []
    streamlit_options = []

    if args.pyinstaller_options:
        if "--streamlit-options" in args.pyinstaller_options:
            split_index = args.pyinstaller_options.index("--streamlit-options")
            pyinstaller_options = args.pyinstaller_options[:split_index]
            streamlit_options = args.pyinstaller_options[split_index + 1 :]
        else:
            pyinstaller_options = args.pyinstaller_options

    if args.streamlit_options:
        if "--pyinstaller-options" in args.streamlit_options:
            split_index = args.streamlit_options.index("--pyinstaller-options")
            streamlit_options = args.streamlit_options[:split_index]
            pyinstaller_options = args.streamlit_options[split_index + 1 :]
        else:
            streamlit_options = args.streamlit_options

    try:
        build_executable(
            script_path=args.script_path,
            name=args.name,
            icon=args.icon,
            script_type=args.script_type,
            raw_script_path=args.raw_script,
            pyinstaller_options=pyinstaller_options,
            streamlit_options=streamlit_options,
        )
    except Exception as e:
        sys.exit(f"Build failed: {e}")


if __name__ == "__main__":
    main()
