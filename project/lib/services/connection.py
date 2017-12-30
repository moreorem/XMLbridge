#!python3
import pymssql
from collections import defaultdict
from lib import queries


class DBsqlsrv(object):

    def __init__(self, userIn, passwordIn, hostIn, dbName, temporary):
        try:
            self.conn = pymssql.connect(user = userIn, password = passwordIn, host = r'' + hostIn, database = dbName , timeout = 8, autocommit=True)
            self.cursor = self.conn.cursor()
            self.nameList = []
            self.dbName = dbName
            self.iters = 0
            self.tablesColumns = {}
            if temporary == True:
                self.prefix = '#'
            else:
                self.prefix = ''

            print("Connection successful!")
        except ConnectionError:
            print("Connection Failed ")

    
    # creates a table according to the schema of a corresponding xml segment
    def create_schema(self, tableName, *args):
        colNamesCurrent = args

        # Store segment's schema into memory if there is not another one with the same name 
        if tableName in self.nameList:
            # Update the table's column info by merging any differences in the new one with the same name
            self.tablesColumns[tableName] = self.merge_lists(self.tablesColumns[tableName], colNamesCurrent)
        else:
            # add the name of the table to the list
            self.nameList.append(tableName)
            # Add an entry for this table's column names
            self.tablesColumns[tableName] = args
            

    def create_tables(self):
        num = 0

        # create the temporary table that gets the xml data dynamically
        while len(self.nameList) > 0:
            tableName = self.nameList[0]
            colNames = self.tablesColumns[tableName]
            
            # Remove the created table from the list so that it wont try to create it again
            self.nameList.remove(tableName)

            query = queries.create_temp_table(tableName, colNames, self.prefix)

            # execute query
            self.cursor.execute(query)
       
            num+=1
        print('created {} tables!'.format(num))
            

    def insert_values(self, tableName, **valueList):
        columnString = ''
        dataInsert = []
        prTableName = self.prefix + tableName

        for key, value in valueList.items():
            if key != 'parentID':
                # column names
                columnString += ',{}'.format(key)
                
                # data part for each column
                dataInsert.append(str(value).strip())

        # Insert parentID value in the beginning of the list
        dataInsert.insert(0, valueList['parentID'])
        # If the parentID is empty convert it to zero to avoid operational error
        if isinstance(dataInsert[0], str):
            dataInsert[0] = int('0')
        # print(dataInsert)
        query = queries.insert_into_temp(prTableName, columnString, dataInsert) 
        try:
            self.cursor.execute(query, tuple(dataInsert))
        except pymssql.OperationalError as e:
            print(query, dataInsert, e)
        
        
    def sp(self, spName, fileID):
        ErrorText = ''
        try:
            msg = self.cursor.callproc(spName, (fileID, pymssql.output(str)))
        except pymssql.OperationalError as e:
            print('A procedure with the name {} does not exist'.format(spName), e)
            return 1

        return msg[1]
        

    
    # creates the file history table if not exists
    def create_fh_table(self, tableName):
        self.cursor.execute(queries.create_file_history_table(tableName, self.dbName))

    # updates the file history table with file info
    def update_fh_table(self, tableName, filesID):
        condition = ','.join([str(i) for i in filesID])
        try:
            self.cursor.execute(queries.update_file_history_table(tableName, condition))
        except Exception as e:
            print('No file history entries to update! ', e)

    def insert_into_fh(self, tableName, docNum, filenames, ediType):
        data = [tuple(a) for a in zip(docNum, filenames, ediType)]

        self.cursor.executemany(queries.insert_into_file_history_table(tableName), data)
    
    def get_unparsed_from_fh(self, tableName, ediType):
        self.cursor.execute(queries.get_from_file_history_table(tableName, ediType))
        return self.cursor.fetchall()
        
    def set_error_fh(self, tableName, fileID, errorText):
        self.cursor.execute(queries.set_error_file_history_table(tableName, fileID, errorText))

    def clear_temp(self, tables):
        for i in range(len(tables)):
            tables[i] = self.prefix + tables[i]
       
        self.cursor.execute(queries.drop_temp_tables(tables))        

    
    # Method that updates the upload info history table
    def update_uh(self, tableName, uploaded, idToUpdate):
        try:
            self.cursor.executemany(queries.update_export_file_history_table(tableName, uploaded), idToUpdate)
        except pymssql.OperationalError as e:
            print('problem with query', e)

    def get_uh(self, tableName, groupID):
        self.cursor.execute(queries.get_export_file_history_table(tableName, groupID))
        return self.cursor.fetchall()

    def merge_lists(self, a, b):
        a = list(a)
        b = list(b)
        diff = list(set(a) - set(b))
        return diff + b
