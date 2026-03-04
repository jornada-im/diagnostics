# reporting

This repository contains code and other resources that information managers can use to generate data management reports for proposals, annual reports to funders, publication lists, and similar reporting items.

The scripts here rely heavily on [pyEDIutils](https://github.com/jornada-im/pyEDIutils/).

## Directories and files

Code in this repository uses a shared directory called "reporting_io" where input data, such as data from requests to repositories, and report outputs (tables, figures) should be stored. Use the `config.py` script to select this directory and generate useful paths.

### This directory

```
|-- jupyter                  - Jupyter notebooks
|-- config.py                - Configuration script to set paths
`-- README.md                - This file
```

### The reporting_io directory (for inputs and outputs)

```
|-- edi                                     - EDI-related data
|   |-- audit_rq                            -   Archived requests for dataset access
|   |   `-- <scope>_raw_datadownloads.csv   -     EDI audit report for  <scope> data downloads
|   `-- changes_rq                          -   Archived requests for dataset changes
|   |   `-- <scope>_20250701-20251231.xml   -     XML responses from change API for <scope>
|   `-- soft_deletes                        -   Listing of datasets soft-deleted
|-- report_figures                          - Figures saved from jupyter notebooks
|-- report_tables                           - Annual report tables
`-- README.md
```


