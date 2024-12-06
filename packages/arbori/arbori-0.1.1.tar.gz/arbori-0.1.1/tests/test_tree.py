import pytest

from arbori.tree import Tree


def test_empty_input_fail():
    with pytest.raises(ValueError, match="Root cannot be empty"):
        Tree(None, [])


def test_invalid_node_value_fail():
    tree_input = ["root", "  child:1", "  child2"]

    with pytest.raises(
        ValueError, match="Value 'child:1' contains illegal character ':'"
    ):
        Tree("root", tree_input)


def test_single_root_node_pass():
    tree = Tree("root", [])

    assert tree.root.value == "root"
    assert len(tree.root.children) == 0


def test_root_with_one_child_pass():
    tree_input = ["child1"]

    tree = Tree("root", tree_input)

    assert tree.root.value == "root"
    assert len(tree.root.children) == 1
    assert tree.root.children[0].value == "child1"
    assert len(tree.root.children[0].children) == 0


def test_complicated_tree_pass():
    tree_input = [
        "parent",
        "  child1",
        "    grandchild1",
        "      greatgrandchild1",
        "    grandchild2",
        "  child2",
    ]

    tree = Tree("root", tree_input)
    parent = tree.root.children[0]
    child1 = parent.children[0]
    grandchild1 = child1.children[0]
    greatgrandchild1 = grandchild1.children[0]
    grandchild2 = child1.children[1]
    child2 = parent.children[1]

    assert tree.root.value == "root"
    assert len(tree.root.children) == 1
    assert parent.value == "parent"
    assert len(parent.children) == 2
    assert child1.value == "child1"
    assert len(child1.children) == 2
    assert grandchild1.value == "grandchild1"
    assert len(grandchild1.children) == 1
    assert greatgrandchild1.value == "greatgrandchild1"
    assert len(greatgrandchild1.children) == 0
    assert grandchild2.value == "grandchild2"
    assert len(grandchild2.children) == 0
    assert child2.value == "child2"
    assert len(child2.children) == 0
