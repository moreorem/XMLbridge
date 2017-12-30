
def create_temp_table(tableName, columnNames, prefix):
    query = """CREATE TABLE {}{} ({}ID numeric PRIMARY KEY IDENTITY(1,1), parentID numeric Default 0,""".format(prefix ,tableName, tableName)
    columnDeclare = ''
    
    # Remove recognized parentID because we already declared it as a numeric
    listx = list(columnNames) 
    try:
        listx.remove('parentID')
    except ValueError as e:
        pass
    columnNames = tuple(listx)

    columnDeclare = ' varchar(200) COLLATE SQL_Latin1_General_CP1253_CI_AS,'.join(columnNames)
    finalQuery = query + columnDeclare + ' varchar(200) COLLATE SQL_Latin1_General_CP1253_CI_AS);'
    # print(finalQuery)
    
    return finalQuery


def insert_into_temp(tableName, columns, tupleLen):
    query = "INSERT INTO {}(parentID, {}) VALUES (".format(tableName, columns[1:]) + '%d' + (len(tupleLen) - 1) * ',%s' + ");"
    return query


def create_file_history_table(tableName, dbName):
    query = """if not exists (select * from sys.tables t join sys.schemas s on 
            (t.schema_id = s.schema_id) where s.name = '{}' and t.name = '{}') 
            begin create table dbo.{} ( FhID numeric PRIMARY KEY IDENTITY(1,1), 
            docNum varchar(60), isParsed bit not null, fileName varchar(200),
            regDateTime Datetime, updateDateTime DateTime, ErrorText nvarchar(max) Default '' ) end""".format(dbName, tableName, tableName)
    return query

def update_file_history_table(tableName, condition):
    query = """Update {} Set isParsed = 1, updateDateTime = getdate() Where fhID in ({})""".format(tableName, condition)
    return query

def insert_into_file_history_table(tableName):
    query = """Insert Into {}(docNum, fileName, isParsed, regDatetime, MESTYP) Values(%d, %s, 0, getDate(), %s)""".format(tableName)
    return query

def get_from_file_history_table(tableName, ediType):
    query = """Select cast(FhID as varchar(10)), fileName, docNum From {} with(nolock) Where isParsed = 0 and MESTYP='{}'""".format(tableName, ediType)
    return query

def set_error_file_history_table(tableName, fileID, errorText):
    query = """Update {} Set errorText = '{}' Where fhID = {}""".format(tableName, errorText, fileID)
    return query

def update_export_file_history_table(tableName, uploaded):
    if uploaded == True:
        query = """Update {} Set EfhIsUploaded = '{}', EfhUpdateDateTime = getdate() Where EfhID = %d and EfhIsUploaded = 0""".format(tableName, uploaded)
    else:
        query = ''
    return query

def get_export_file_history_table(tableName, groupID):
    query = """Select cast(EfhID as varchar(30)), EfhFileName From {} With(nolock) Where EfhIsUploaded = 0 and EfhGroupID = {}""".format(tableName, groupID)
    return query


def drop_temp_tables(tables):
    query = ''
    for table in tables:
        query += """DROP TABLE {}; """.format(table)
    return query