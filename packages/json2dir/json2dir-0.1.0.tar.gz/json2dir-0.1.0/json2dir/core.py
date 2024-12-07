"""Core functionality for json2dir package."""

import json
import os
from pathlib import Path
from typing import Dict, Union, Any


def json_to_dir(json_file: Union[str, Path], output_dir: Union[str, Path]) -> None:
    """Convert JSON structure to directory structure.

    Args:
        json_file: Path to JSON file
        output_dir: Path to output directory
    """
    with open(json_file, 'r') as f:
        structure = json.load(f)
    
    output_dir = Path(output_dir)
    _create_structure(structure, output_dir)


def dir_to_json(directory: Union[str, Path], output_file: Union[str, Path]) -> None:
    """Convert directory structure to JSON.

    Args:
        directory: Path to directory
        output_file: Path to output JSON file
    """
    directory = Path(directory)
    structure = _parse_directory(directory)
    
    with open(output_file, 'w') as f:
        json.dump(structure, f, indent=4)


def _create_structure(structure: Dict[str, Any], base_path: Path) -> None:
    """Recursively create directory structure from dictionary.

    Args:
        structure: Dictionary representing directory structure
        base_path: Base path to create structure in
    """
    for name, content in structure.items():
        path = base_path / name
        if content is None:
            # It's a file
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        else:
            # It's a directory
            path.mkdir(parents=True, exist_ok=True)
            _create_structure(content, path)


def _parse_directory(directory: Path) -> Dict[str, Any]:
    """Recursively parse directory structure into dictionary.

    Args:
        directory: Directory to parse

    Returns:
        Dictionary representing directory structure
    """
    structure = {}
    
    for item in directory.iterdir():
        if item.is_file():
            structure[item.name] = None
        else:
            structure[item.name] = _parse_directory(item)
    
    return structure
