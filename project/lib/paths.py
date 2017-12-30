import yaml
import sys
import os

''' Contains Paths of the program'''

MAIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__ + '\..')) + '\\'
CONFIG_NAME = 'config.yml'    
SCHEMA_TEMPLATE = 'schema-template.yml'

def get_root_dir():
    return MAIN_DIRECTORY + '\\'#+ 'project\\' #change it for the compiled version remove 'project'

# returns directory paths of the program
def get_directory(section):
    with open(MAIN_DIRECTORY + CONFIG_NAME) as ymlfile:
        cfg = yaml.load(ymlfile)
    path = ''.join(cfg['directories'][section])
    return path

# returns ftp configuration from file
def get_ftp(section):
    with open(MAIN_DIRECTORY + CONFIG_NAME) as ymlfile:
        cfg = yaml.load(ymlfile)
    ftpconf = cfg['ftp'][section]
    return ftpconf

# returns sql server configuration
def get_sql(section):
    with open(MAIN_DIRECTORY + CONFIG_NAME) as ymlfile:
        cfg = yaml.load(ymlfile)
    sqlconf = cfg['sql'][section]
    return sqlconf

# returns corresponding procedure
def get_procedure(section):
    with open(MAIN_DIRECTORY + CONFIG_NAME) as ymlfile:
        cfg = yaml.load(ymlfile)
    try:
        procconf = cfg['procedures'][section]
    except KeyError as e:
        print('Cannot find procedure for this type of EDI', e)
        sys.exit(1)
    return procconf

# returns xml configuration for the bridge
def get_edi_template(ediType, tableName):
    with open(MAIN_DIRECTORY + SCHEMA_TEMPLATE) as ymlfile:
        tpl = yaml.load(ymlfile)
    try:
        if tableName == ':':
            return tpl[ediType]
        else:
            try:
                return tpl[ediType][tableName]
            except KeyError as e:
                print('no {} segment in template'.format(e))
                pass
    except KeyError as e:
        print('There is no EDI type with the name {} or segment with the name {} in the template'.format(ediType, tableName))
        return 1

# returns xml configuration from file
def get_xml(section):
    with open(MAIN_DIRECTORY + CONFIG_NAME) as ymlfile:
        cfg = yaml.load(ymlfile)
    xmlconf = cfg['xml'][section]
    return xmlconf