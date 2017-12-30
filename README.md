# XML Bridge for EDI handling

The app allows downloading from ftp xml files, parsing them by recognizing each parent segment as a table and every element as a column name.
It fills the columns with the element text as data.

## Getting Started



### Prerequisites

For version 1.3.4 that uses Python 3.4, Visual C++ 2010 is required.
For version 1.3.6 that uses Python 3.6 Visual C++ 2013 is required.

To build, cx_Freeze is required
```
pip install cx_Freeze
```

Sometimes problems in installing cx_Freeze might occur with Python 3.4 so using a whl file would be appropriate
```
https://pypi.python.org/pypi/cx_Freeze/5.0.2
```

```
pip install cx_Freeze-5.0.2-cp34-cp34m-win_amd64.whl
```

Some extra libraries are also required:

```
pip install pymssql
```
```
pip install pyyaml
```
```
pip install pysftp
```


### Installing

To install for Windows XP, Windows Server 2003 and generally for every older platform

```
Install Visual C++ 2010
```

To install for modern Windows
```
Install Visual C++ 2013
```

## Deployment

Using cx_Freeze from a command line in the root folder where the setup.py resides type:
```
python setup.py build
```

Then copy the corresponding architecture folder from the build folder to the computer that you want to use it to.
The program runs from cmd shell using the proper commands

### Ftp client
To download from ftp, ensure that the config.yml is properly set up. The syntax is the following:
```
ftp-client.exe
```
To upload to ftp the syntax is the following:
```
ftp-client.exe U <groupIndex>
```
where groupIndex is the file group index according to the sql export history table. This column in the export history table has to exist in order to allow batch file uploading

### EDI parser
To call the parser, ensure that the config.yml is properly set up. The syntax is the following:
```
edi-parser.exe <EDI type>
```
where EDI type the type of EDI message the xml resembles. The parser always recognizes the edi types usually from the prefix of the filename or from the files history table Message Type column.


## Authors
    Orestis Moresis o.moresis@outlook.com
    

See also the list of contributors who participated in this project.
## License

This project is licensed under the Apache License, Version 2.0 - see the LICENSE.md file for details
