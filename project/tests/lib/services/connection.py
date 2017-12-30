#!python3
import pymssql

class DBsqlsrv(object):
    con = None
    cur = None

    def __init__(self, userIn, passwordIn, hostIn):
        try:
            self.con = pymssql.connect(user = userIn, password = passwordIn, host = r'' + hostIn, database = '' , timeout = 8, autocommit = True)
            self.cur = self.con.cursor()
            print("connection successful!")
        except:
            print("Connection Failed ")
        

    def query(self, query, params):
        self.autocommit = True
        return self.cur.execute(query, params)

    def sp(self, spName):
        self.autocommit = True
        return self.cur.execute("exec " + spName)
    

    def executeScriptsFromFile(self, filename):
        # Open and read the file as a single buffer
        # for script in os.listdir(inputdir):
        self.autocommit = False
        with open(filename, 'r') as sqlfile:
            for stmt in self.split_sql_expressions(sqlfile.read()):
                try:
                    self.cur.execute(stmt)
                except Exception as inst:
                    print("Command skipped: ", inst)
        sqlfile.close()
        self.con.commit()

    def split_sql_expressions(self, text):
        results = []
        current = ''
        state = None
        for c in text:
            if state is None:  # default state, outside of special entity
                current += c
                if c in '"\'':
                    # quoted string
                    state = c
                elif c == '-':
                    # probably "--" comment
                    state = '-'
                elif c == '/':
                    # probably '/*' comment
                    state = '/'
                elif c == ';':
                    # remove it from the statement
                    current = current[:-1].strip()
                    # and save current stmt unless empty
                    if current:
                        results.append(current)
                    current = ''
            elif state == '-':
                if c != '-':
                    # not a comment
                    state = None
                    current += c
                    continue
                # remove first minus
                current = current[:-1]
                # comment until end of line
                state = '--'
            elif state == '--':
                if c == '\n':
                    # end of comment
                    # and we do include this newline
                    current += c
                    state = None
                # else just ignore
            elif state == '/':
                if c != '*':
                    state = None
                    current += c
                    continue
                # remove starting slash
                current = current[:-1]
                # multiline comment
                state = '/*'
            elif state == '/*':
                if c == '*':
                    # probably end of comment
                    state = '/**'
            elif state == '/**':
                if c == '/':
                    state = None
                else:
                    # not an end
                    state = '/*'
            elif state[0] in '"\'':
                current += c
                if state.endswith('\\'):
                    # prev was backslash, don't check for ender
                    # just revert to regular state
                    state = state[0]
                    continue
                elif c == '\\':
                    # don't check next char
                    state += '\\'
                    continue
                elif c == state[0]:
                    # end of quoted string
                    state = None
            else:
                raise Exception('Illegal state %s' % state)

        if current:
            current = current.rstrip(';').strip()
            if current:
                results.append(current)

        return results

    def __del__(self):
        self.con
