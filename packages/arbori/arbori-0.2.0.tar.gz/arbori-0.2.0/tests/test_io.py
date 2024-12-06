from unittest.mock import MagicMock

import pytest

from arbori.io import build_directory_structure, parse_input_file


def test_parse_input_file_empty_fail():
    input_content = """


    """

    with pytest.raises(ValueError):
        parse_input_file(input_content)


def test_parse_input_file_invalid_indent_fail():
    input_content = """
root
   child1
     grandchild1
    """

    with pytest.raises(ValueError):
        parse_input_file(input_content)


def test_parse_input_file_invalid_indent_two_fail():
    input_content = """
root
  child1
     grandchild1
  child2
    """

    with pytest.raises(ValueError):
        parse_input_file(input_content)


def test_parse_input_file_empty_lines_pass():
    input_content = """

root

child1
    """

    result = parse_input_file(input_content)

    assert result == ["root", "child1"]


def test_parse_input_file_indent_two_spaces_pass():
    input_content = """
root
  child1
    grandchild1
  child2
    """

    result = parse_input_file(input_content)

    assert result == ["root", " child1", "  grandchild1", " child2"]


def test_parse_input_file_indent_four_spaces_pass():
    input_content = """
root
    child1
        grandchild1
    child2
    """

    result = parse_input_file(input_content)

    assert result == ["root", " child1", "  grandchild1", " child2"]


def test_create_folders_from_tree_empty_tree_pass(tmp_path):
    empty_node = MagicMock()
    empty_node.value = "root"
    empty_node.children = []

    build_directory_structure(empty_node, tmp_path)

    assert (tmp_path / "root").exists()


def test_create_folders_from_tree_pass(tmp_path):
    root_node = MagicMock()
    root_node.value = "root"
    root_node.children = []

    child_node = MagicMock()
    child_node.value = "child1"
    child_node.children = []
    root_node.children.append(child_node)

    build_directory_structure(root_node, tmp_path)

    assert (tmp_path / "root").exists()
    assert (tmp_path / "root" / "child1").exists()


def test_create_folders_from_detailed_tree_pass(tmp_path):
    root_node = MagicMock()
    root_node.value = "root"
    root_node.children = []

    child_node = MagicMock()
    child_node.value = "child1"
    child_node.children = []
    root_node.children.append(child_node)

    grandchild_node = MagicMock()
    grandchild_node.value = "grandchild1"
    grandchild_node.children = []
    child_node.children.append(grandchild_node)

    great_grandchild_node = MagicMock()
    great_grandchild_node.value = "greatgrandchild1"
    great_grandchild_node.children = []
    grandchild_node.children.append(great_grandchild_node)

    grandchild_two_node = MagicMock()
    grandchild_two_node.value = "grandchild2"
    grandchild_two_node.children = []
    child_node.children.append(grandchild_two_node)

    child_two_node = MagicMock()
    child_two_node.value = "child2"
    child_two_node.children = []
    root_node.children.append(child_two_node)

    build_directory_structure(root_node, tmp_path)

    assert (tmp_path / "root").exists()
    assert (tmp_path / "root" / "child1").exists()
    assert (tmp_path / "root" / "child1" / "grandchild1").exists()
    assert (tmp_path / "root" / "child1" / "grandchild1" / "greatgrandchild1").exists()
    assert (tmp_path / "root" / "child1" / "grandchild2").exists()
    assert (tmp_path / "root" / "child2").exists()
