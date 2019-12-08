"""
Parse a requirements.txt file and return its content.
"""


def read_requirements(file_path: str):
    """
    Parse a requirements.txt file and return its content.
    """
    content = open(file_path, "r").read()

    return [requirement for requirement in content.splitlines()]
