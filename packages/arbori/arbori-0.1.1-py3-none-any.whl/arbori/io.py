from pathlib import Path


def parse_input_file(input_content):
    lines = [line for line in input_content.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Input content is empty or only contains whitespace.")
    for line in lines:
        length = len(line)
        stripped_length = len(line.lstrip())
        if length != stripped_length:
            if (length - stripped_length) % 2 != 0:
                raise ValueError(f"Line has incorrect indentation: {line}")
    return lines


def build_directory_structure(node, base_path):
    base_path = Path(base_path)
    node_path = base_path / node.value
    node_path.mkdir(parents=True, exist_ok=True)
    for child in node.children:
        build_directory_structure(child, node_path)
