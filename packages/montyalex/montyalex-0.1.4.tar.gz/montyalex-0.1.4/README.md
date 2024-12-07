# montyalex

## Installation

```bash
pip install montyalex
```

## Initialization

```bash
mtax init
```

- Another entry point: "montyalex" also exists; If you'd prefer to use it over "mtax"
- If you wish to initialize only the cache or settings independently, subsequent commands are available

## Features

### Settings

Settings can be changed within the specified file of the directory.

The file is available in JSON, TOML, YAML and MessagePack formats. Any can be used independently and in a future version will support *backup* setting files for data recovery purposes, and also a *synced* settings environment enabling support for all formats to be used in conjunction.

### Cache

The program will automatically track certain *variables* or *(retrieved/configured) data* to provide
quicker responses when executing commands.

The cache can be enabled/disabled by a toggle in the settings.

Many features included in the cache itself **will** be further discussed in it's own README, located in the cache_tools directory. (A link will be included when accessible)

### Files

- Create
  - a single empty file
  - many empty files
  - a single file with preset content
  - many files with preset content
- Remove
  - a single file
  - many files with;
    - a similar name pattern
    - in a common directory
    - in a defined list

### Directories

- Create
  - a single empty directory
  - a single directory with an empty file
  - a single directory with a file with preset content
  - many empty directories
  - many directories with an empty file or many empty files
  - many directories with a file with preset content or many files with preset content
- Remove
  - a single directory
  - many directories with;
    - a similar name pattern
    - within a defined tree
    - in another directory
    - in a defined list

### Trees [ PLANNED by v1.0.0 ]

- Create
  - a single empty tree
  - a single tree with an empty directory
  - a single tree with a directory with a single empty file
  - many empty trees
  - many trees with an empty directory or many empty directories
  - many trees with a directory containing;
    - a single empty file or many empty files
    - a single file or many files containing preset content
- Remove
  - a single tree
  - many trees with;
    - a similar name pattern
    - in another defined tree
    - in a defined list
