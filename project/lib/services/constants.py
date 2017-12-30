UNDEF = -1
RS_SQL_STRING_SPACE_ONE = " "
RS_SQL_DOT = "."
RS_SQL_QUOTED_CHAR = System.Convert.ToChar("'")

RS_SQL_LEFT_PARENTHESIS = "("
RS_SQL_RIGHT_PARENTHESIS = ")"
RS_SQL_LEFT_BRACKET = "["
RS_SQL_RIGHT_BRACKET = "]"
RS_SQL_COMMA = ","

RS_SQL_SELECT = "SELECT"
RS_SQL_COMMAND_GET_DB_COLLATION = "Select Cast(DATABASEPROPERTYEX(DB_NAME(), 'Collation') as varchar(512)) as Collation"

SQL_SERVER_IMAGE_MAX_VALUE = 8000     //(in bytes)

rsMsg_FailureOnCheckIfMustUpdateDBVersion = "Παρουσιάσθηκε πρόβλημα στην μέθοδο [ CheckIfMustUpdateDBVersion() ] με μήνυμα λάθους :\n<< {0} >>"