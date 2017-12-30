from lib.services import connection

def loadForms(db, selectedDatabaseName):
    # Create list of Forms
    db.query('SELECT IDCID, IDCDescription FROM [' + selectedDatabaseName + '].[dbo].[A03_a2af16b2_671d_4465_874e_0b9d61f58f9e] with(nolock)', None)

    formIds = []
    formNames = []

    for row in db.cur:
        if row[0] > 0:
            formIds.append(row[0])
            formNames.append(row[1])

    formDictionary = dict(zip(formIds, formNames))
    
    return formDictionary

def loadDatabases(db):
    # Create list of Databases
    db.query('SELECT dbid, name FROM master.dbo.sysdatabases', None)

    databaseIds = []
    databaseNames = []

    for row in db.cur:
        if row[0] > 0:
            databaseIds.append(row[0])
            databaseNames.append(row[1])

    databaseDictionary = dict(zip(databaseIds, databaseNames))

    return databaseDictionary

def getSelectedDatabaseName(db, selectedDatabaseId):
    db.query('SELECT dbid, name FROM master.dbo.sysdatabases with(nolock) WHERE dbid=' + selectedDatabaseId, None)
    for row in db.cur:
        if row[0] > 0:
            selectedDatabaseName = row[1]

    return selectedDatabaseName

def updateForm(db, dbName, formId, hasRibbon, ribbonType, hasImg):
    
    db.sp("[" + dbName + "].dbo.st_updateFormXMLwithTemplate @createNewForm = 0, @FormIdcid = " + str(formId) + 
                  ", @InsertRibbon = " + str(hasRibbon) + ", @ribbonType = " + str(ribbonType) + 
                  ", @insertImages = " + str(hasImg) + ", @ErrorText = ''")

def getFormXML(db, dbName, formId):
    db.query('SELECT IDCID, IDCFormXML FROM ' + dbName + '.dbo.A03_a2af16b2_671d_4465_874e_0b9d61f58f9e WITH(nolock) WHERE IDCID =' + formId, None)
    return db.cur