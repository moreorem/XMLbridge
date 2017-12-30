import logging
import os
import sys
import pysftp
from lib import paths
from lib.services import connection

REMOTE_WORKPATH = paths.get_ftp('remoteWorkpath')
REMOTE_UPPATH = paths.get_ftp('remoteUpload')

LOCAL_DOWNLOAD = paths.get_directory('download')
EXPORT_PATH = paths.get_directory('export') 
UPLOAD_PATH = paths.get_directory('uploaded')

HOSTNAME = paths.get_ftp('host')
USERNAME = paths.get_ftp('name')
PASSWORD = paths.get_ftp('pass')

FILE_HISTORY_TABLE = paths.get_sql('filehistory')
EXPORT_FILE_HISTORY_TABLE = paths.get_sql('exporthistory')



def main():
    
    logging.basicConfig(filename='ftp.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Client started in download mode...')
    
    # Create SQL Connection
    db = connection.DBsqlsrv(paths.get_sql('name'), paths.get_sql('pass'), paths.get_sql('host'), paths.get_sql('dbase'), paths.get_sql('istemptable'))
    
    # SFTP config
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  

    # Initialize some variables
    docNums = []
    ediTypes = []
    filenames = []

    try:
        fhUnparsed = db.get_unparsed_from_fh(FILE_HISTORY_TABLE)
        fhUnparsed = [i[1] for i in fhUnparsed]
    except:
        fhUnparsed = []

    # Connect to FTP server
    try:
        with pysftp.Connection(HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts) as sftp:
            print('connection successful!')
        
            if sftp.exists(REMOTE_WORKPATH + 'backup') == False:
                try:
                    sftp.mkdir(REMOTE_WORKPATH + 'backup')
                except Exception as e:
                    logging.error('Could not create backup folder on remote server')
                    print(e, 'Could not create backup folder on remote server')

            print(sftp.stat(REMOTE_WORKPATH))
            
            fileList = sftp.listdir(REMOTE_WORKPATH)

            for filename in fileList:
                if filename[-4:] == '.xml' and filename not in fhUnparsed:
                    if filename not in os.listdir(paths.get_directory('download')):
                        try:
                            # download files locally
                            sftp.get(REMOTE_WORKPATH + filename, LOCAL_DOWNLOAD + filename)
                            
                            # move files from remote workpath folder to remote backup
                            sftp.rename(REMOTE_WORKPATH + filename, REMOTE_WORKPATH + 'backup/' + filename)
                        except IOError as e:
                            logging.warning("Could not download or perform backup")
                            print(e, "Could not download or perform backup")
                        
                        # Update filename, ediTypes and docNum lists
                        filenames.append(filename)
                        a = filename.split('_')
                        ediTypes.append(a[0])
                        docNum = a[-1][:-4]
                        docNums.append(docNum)

        # Close the ftp connection
        sftp.close()

    except pysftp.SSHException as e:
        logging.error('Unable to connect to {}'.format(e))
        return 1
    

    logging.info(" {} xml files were downloaded!".format(len(docNums)))
    print("{} xml files were downloaded!".format(len(docNums)))
    
    # Insert file info into history table
    db.insert_into_fh(FILE_HISTORY_TABLE, docNums, filenames, ediTypes)


def upload():
  
    logging.basicConfig(filename='ftp.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Client started in upload mode...')
    # Connect to SQL server
    db = connection.DBsqlsrv(paths.get_sql('name'), paths.get_sql('pass'), paths.get_sql('host'), paths.get_sql('dbase'), paths.get_sql('istemptable'))
    logging.info('Connected to db.')

    # SFTP config
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None 
    exportFiles = tuple(os.listdir(EXPORT_PATH + "\\"))

    # Initialize some variables
    idsToUpdate = []
    uhIDs = []
    uhFilenames = []
    successCount = 0

    # Connect to FTP server
    try:
        with pysftp.Connection(HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts) as sftp:
            logging.info('Connect to FTP.')
            sftp.cwd(u'' + REMOTE_UPPATH)
            
        
            for row in db.get_uh(EXPORT_FILE_HISTORY_TABLE, GROUP_ID):
                uhIDs.append(int(row[0]))
                uhFilenames.append(row[1])
            
            exports = [tuple(uhIDs), tuple(uhFilenames)]

            for filename in exportFiles:
                if filename in exports[1]:
                    try:
                        idx = exports[1].index(filename)

                        # Upload file to ftp remote
                        sftp.put(localpath=EXPORT_PATH + filename, remotepath=filename, confirm=True, preserve_mtime=True)
                        idsToUpdate.append(exports[0][idx])

                        # Move file from export folder to uploaded folder
                        os.system("move {} {}".format('\"' + EXPORT_PATH + '\\' + filename + '\"' , '\"' + UPLOAD_PATH + '\\' + '\"'))
                        successCount += 1
                    except ValueError as e:
                        print('Could not found file', filename, e)
            
        # Close the ftp connection
        sftp.close()

    except pysftp.SSHException as e:
        logging.error('Unable to connect to {}'.format(e))
        sys.exit(1)

    # Update export file history table
    db.update_uh(EXPORT_FILE_HISTORY_TABLE, True, idsToUpdate)
    logging.info('Uploaded {} files!'.format(successCount))



if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].upper() == 'U' or sys.argv[1].upper() =='EXPORT':
            try:
                GROUP_ID = sys.argv[2]
                upload()
                
            except SyntaxError as e:
                print("You didn't provide a group ID", e)
    else:
        main()
