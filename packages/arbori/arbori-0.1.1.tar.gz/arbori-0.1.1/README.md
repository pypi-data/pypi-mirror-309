# Arbori

A lightweight command line tool that generates folder structures from simple text files. Simply provide an input file with your desired folder hierarchy using indentation (2 spaces) to indicate nesting levels, specify an output directory, and arbori will create the complete folder structure for you.

The name is inspired by arboriculture - the cultivation, management, and study of individual trees.

## Example

Input file (structure.txt):

```txt
parent
  child1
    grandchild1
    grandchild2
  child2
    grandchild3
    grandchild4
  child3
    grandchild5
    grandchild6
```

Run arbori:

```bash
arbori create structure.txt output-directory
```

Will generate the following folders.

```
.
└── parent
    ├── child1
    │   ├── grandchild1
    │   └── grandchild2
    ├── child2
    │   ├── grandchild3
    │   └── grandchild4
    └── child3
        ├── grandchild5
        └── grandchild6
```

## Installation

Install from PyPI:

```bash
pip install arbori
```

## Usage

Basic usage:

```bash
arbori input.txt output/directory/
```

## Contributing

Contributions are welcome! Here's how to get started:

1. Fork and clone the repository
2. Set up your Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install .
pip install -e '.[dev]'
```

4. Create your feature branch

```bash
git checkout -b feature/new-feature
```

5. Development Guidelines:

- Write tests for new features using pytest
- Add documentation for new features

6. Submit a Pull Request:

- GitHub Actions will lint, format, and test code
- Ensure all tests pass
- Update documentation if needed
- Pull requests without tests will not be reviewed

## License

This project is licensed under the MIT License - see the LICENSE file for more details.
