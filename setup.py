import os
import sys
from cx_Freeze import Executable, setup

execs = [Executable(script="D:\\Workspace\\Python\\XMLbridge\\project\\edi-parser.py", base=None), Executable(script="D:\\Workspace\\Python\\XMLbridge\\project\\ftp-client.py", base=None)]


includes = []
includeFiles = [
                 r"D:\\Workspace\\Python\\XMLbridge\\project\\resources",
                 r"D:\\Workspace\\Python\\XMLbridge\\project\\lib",
                 r"D:\\Workspace\\Python\\XMLbridge\\project\\config.yml",
                 r"D:\\Workspace\\Python\\XMLbridge\\project\\schema-template.yml"
                 ]
packages = ["os", "pymssql", "_mssql", "decimal", "xml", "pysftp", "yaml", "uuid", "cffi", "idna", "logging"]
build_exe_options = {
            "packages": packages, 
            "include_files": includeFiles
        }


setup( 
    name='XMLbridge',
    version='1.7',
    description='Bridge for XML EDI files to datatables',
    author='Orestis Moresis',
    author_email='o.moresis@outlook.com',
    options={"build_exe": build_exe_options},
    executables = execs
    )
