# import glob
import os
import sys
import logging

from lib import paths, queries
from lib.services import xmlhandler
from lib.services.connection import DBsqlsrv

XML_DIRECTORY = paths.get_directory('download')
XML_PROCESSED_DIR = paths.get_directory('processed')

FILE_HISTORY_TABLE = paths.get_sql('filehistory')
IS_TEMP_TABLE = paths.get_sql('istemptable')

SEGMENT_INDICATOR = paths.get_xml('segmentIndicator')

def main():
    
    db = DBsqlsrv(paths.get_sql('name'), paths.get_sql('pass'), paths.get_sql('host'), paths.get_sql('dbase'), paths.get_sql('istemptable'))
    
    otherfiles = []
    filenames = []
    filesList = []
    filesID = []
    files = []
    filesTotal = 0
    filesProcessedTotal = 0

    # Supplementary table and column names
    SUPPL_ITEMS = paths.get_edi_template(EDI_TYPE, ':')


    # Get from the file history list which files of the specific EDI TYPE have not been parsed
    fhUnparsed = db.get_unparsed_from_fh(FILE_HISTORY_TABLE, EDI_TYPE)
    fhID = [i[0] for i in fhUnparsed]
    fhUnparsedFilename = [i[1] for i in fhUnparsed]
    fhUnparsedDocNum = [i[2] for i in fhUnparsed]

    filesList = dict(zip(fhUnparsedDocNum, fhID))
    
    # Config logger
    logging.basicConfig(filename='EDIparser.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Parser started...')

    # Make downloaded files list that contains only the requested EDI files e.g. Materials
    for i in os.listdir(XML_DIRECTORY):
        if os.path.isfile(os.path.join(XML_DIRECTORY,i)) and i.split('_')[0].upper() in EDI_TYPE:
            files.append(i) # All edi files of a specified type in the folder


    # Parse downloaded files one by one
    for filename in files:
        try:
            if filename.endswith(".xml"):
                #if filesTotal == 1: #test for one file
                #   break         #test for one file
                isProcessed = False

                # Update filename and docNum lists
                filenames.append(filename)
                a = filename.split('_')
                docNum = a[-1][:-4]

                logging.info("Found file {} to be parsed...".format(filename))

                # Check that the file in the folder matches the unparsed with the same id from the file history list
                if docNum in fhUnparsedDocNum:
                    
                    logging.info("xml file found: {}".format(filename))
                    # print("xml file found: {}".format(filename))

                    filesTotal += 1
                    
                    # Create EDI identifier
                    EDItype = a[0]

                    # Create an edi object with an xml file from the folder
                    currentEDI = xmlhandler.EDIm(XML_DIRECTORY + filename, SEGMENT_INDICATOR) #TEST
                
                    # Parse all nodes of the xml file
                    currentEDI.get_nodes()
                    parserOutput = currentEDI.parsedData

                    discoveredSegments = [i[1] for i in parserOutput]
                    
                    # Add Supplementary tables and columns
                    # prefix = '#' if IS_TEMP_TABLE == True else ''
                    supplTables = paths.get_edi_template(EDI_TYPE, ':').keys()
                    
                    for key in supplTables:
                        # If there should have been a segment according to the template but there wasn't, create it
                        if key not in discoveredSegments:
                            parserOutput.append([0,key,dict.fromkeys(paths.get_edi_template(EDI_TYPE, key), '')])
                            db.tablesColumns[key] = paths.get_edi_template(EDI_TYPE, key)
                            
                    
                    segmentQuantity = len(parserOutput)
                    
                    # Create Schema
                    for i in range(segmentQuantity):
                        # Define the table name
                        segmentName = parserOutput[i][1]
                        
                        # Fill missing columns
                        try:
                            supplColumns = paths.get_edi_template(EDI_TYPE, segmentName)

                            # Merge list of dynamically created column names with the remaining supplementary
                            if supplColumns != None:
                                for key in supplColumns:
                                    if key not in parserOutput[i][2].keys():
                                        # print(parserOutput[i][2].keys())
                                        parserOutput[i][2][key] = ''
                        except KeyError as e:
                            print('No such segment in template', e)
                            pass

                        # Define the column names
                        elementNames = parserOutput[i][2].keys()

                        # Create Table schema in memory
                        db.create_schema(segmentName, *elementNames)

                    # number of tables to be created
                    tableQuantity = len(db.nameList)
                    
                    # Store the table names in another variable to use for the drop part
                    tablesToDrop = list(db.nameList)
                    
                    # perform queries for every table and columns that were created in memory
                    db.create_tables()

                    # Insert Values
                    for i in range(segmentQuantity):
                        columnData = parserOutput[i][2]
                        try:
                            db.insert_values(parserOutput[i][1], **columnData)
                        except KeyError as e:
                            pass
                    

                    # Update the filesID list to inform the history table
                    filesID.append(docNum)

                    # Execute the stored procedure for this EDI type
                    try:
                        procName = paths.get_procedure(EDItype)
                        
                        procResult = db.sp(procName[0], filesList[docNum])
                        if procResult == '':
                            print(procResult)
                            isProcessed = True
                            # Move the file that was parsed to the corresponding local folder
                            move_to_processed(filename, XML_DIRECTORY)

                            filesProcessedTotal += 1
                        
                        
                    except Exception as e:
                        filesID.remove(docNum)
                        db.set_error_fh(FILE_HISTORY_TABLE, docNum, "could not find a procedure match for this type of edi")
                        logging.error("could not find a procedure match for this type of edi")
                        print(e, "could not find a procedure match for this type of edi")
                        sys.exit(1)
                        
                
                    # Clear temporary tables
                    # if IS_TEMP_TABLE == True:
                    db.clear_temp(tablesToDrop)

            else:
                otherfiles.append(filename)
                print(otherfiles[0] + ' Is not a valid file')
                

        except Exception as e:
            raise e
            print("There was a problem trying to parse file: {}".format(filename))
            logging.error('Unable to parse file {}'.format(filename))
            

    
    if len(files) > 0 and len(filesID) > 0:
        # update file history
        db.update_fh_table(FILE_HISTORY_TABLE, filesID)

    print("Total XML files processed: {} Out of {} files total".format(filesProcessedTotal, filesTotal))
    logging.info("Total XML files processed: {} Out of {} files total".format(filesProcessedTotal, filesTotal))

def move_to_processed(filename, fromDirectory):
    print(fromDirectory + filename)
    print('\"' + XML_PROCESSED_DIR + '\"')
    os.system("move {} {}".format('\"' + fromDirectory + filename + '\"', '\"' + XML_PROCESSED_DIR + '\"'))
    

if __name__ == "__main__":
    os.system('chcp 65001')
    try:
        EDI_TYPE = sys.argv[1].upper()
        main()
        logging.info('Parsing complete')
        print('parsing complete')
    except SyntaxError as e:
        print('Not enough number of arguments! You must specify the type of EDI', e)
        sys.exit(1)
        