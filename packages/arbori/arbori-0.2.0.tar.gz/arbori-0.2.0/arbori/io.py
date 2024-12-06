from pathlib import Path


def parse_input_file(input_content):
    lines = [line for line in input_content.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Input content is empty or only contains whitespace.")
    indent = -1
    indent_set = False
    for line in lines:
        length = len(line)
        stripped_length = len(line.lstrip())
        # Check for nested directory via detecting indent
        if length != stripped_length:
            if not indent_set:
                # Set indent level based on first indented line
                indent = length - stripped_length
                indent_set = True
            if (length - stripped_length) % indent != 0:
                # Raise error if indent level is not consistent
                raise ValueError(f"Line has incorrect indentation: {line}")
    # Update lines to strip extra spaces so 1 space = 1 level
    indent_corrected_lines = [
        f"{' ' * ((len(line) - len(line.lstrip())) // indent)}{line.lstrip()}"
        for line in lines
    ]
    return indent_corrected_lines


def build_directory_structure(node, base_path):
    base_path = Path(base_path)
    node_path = base_path / node.value
    node_path.mkdir(parents=True, exist_ok=True)
    for child in node.children:
        build_directory_structure(child, node_path)
