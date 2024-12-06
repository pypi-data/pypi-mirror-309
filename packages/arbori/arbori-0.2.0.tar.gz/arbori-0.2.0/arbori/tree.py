class Tree:
    class Node:
        def __init__(self, value):
            self.__validate_value(value)
            self.value = value
            self.children = []

        def __repr__(self, level=0):
            ret = " " * level + repr(self.value) + "\n"
            for child in self.children:
                ret += child.__repr__(level + 1)
            return ret

        def __validate_value(self, value):
            invalid_chars = [":", "/", "\\", "<", ">", '"', "|", "?", "*"]
            for char in invalid_chars:
                if char in value:
                    raise ValueError(
                        f"Value '{value}' contains illegal character '{char}'"
                    )

        def add_child(self, child_node):
            self.children.append(child_node)
            self.children.sort(key=lambda x: x.value)

    def __init__(self, root_value, tree_input):
        if root_value is None:
            raise ValueError("Root cannot be empty")
        self.root = self._build_tree(root_value, tree_input)

    def __repr__(self):
        return self.root.__repr__()

    def _build_tree(self, root_value, lines):
        """
        Build the tree structure from the input lines.
        Returns the root node of the tree.
        """
        if not lines:
            return Tree.Node(root_value)

        def get_depth(line):
            """
            Calculate the depth level based on leading spaces (1 spaces = 1 level)
            This is parsed to this requirement via the io.py:parse_input_file function
            """
            return len(line) - len(line.lstrip())

        def build_subtree(lines, start_idx, parent_depth):
            """Recursively build subtrees for each node"""
            assert start_idx < len(lines)
            node = Tree.Node(lines[start_idx].strip())
            current_idx = start_idx + 1

            while current_idx < len(lines):
                current_depth = get_depth(lines[current_idx])

                if current_depth <= parent_depth:
                    break

                assert current_depth == parent_depth + 1
                child_node, new_idx = build_subtree(lines, current_idx, current_depth)
                if child_node:
                    node.add_child(child_node)
                current_idx = new_idx

            return node, current_idx

        root = Tree.Node(root_value)
        current_idx = 0

        while current_idx < len(lines):
            assert get_depth(lines[current_idx]) == 0
            child_node, new_idx = build_subtree(lines, current_idx, 0)
            if child_node:
                root.add_child(child_node)
            current_idx = new_idx

        return root
