# diagnostics

Diagnostics for information management and data publishing at Jornada Basin LTER

The scripts here rely heavily on [pyEDIutils](https://github.com/jornada-im/pyEDIutils/).

## Directories and files

Scripts in this repository rely on a "reporting" folder where requests to repositories and file outputs are stored. Use the `config.py` to choose this directory and generate paths.

### This directory

```
|-- jupyter                  - Jupyter notebooks
`-- README.md                - This file
```

### The reporting directory (outputs)

```
|-- edi                      - EDI-related data
|   |-- changes_rq           -   Archived requests for dataset changes
|   `-- audit_rq             -   Archived requests for dataset access
|   |   `-- ds008_rodent.R   -     Build dataset 008
|   |-- jrn413_csis          -   JRN Study 413: Cross-scale
|   `-- (...)                -   Many more projects...
|-- config.R                 - Some configurations
|-- py                       - Common Python files
|-- R                        - Common R files
`-- README.md                - This file
```


