#!python3
from lib import queries
from tkinter import *
from tkinter import ttk
from lib.gui import elements
from lib.gui import dialog

flag = 0
dbDict = {}
fDict = {}


class MainFrame(Toplevel):
    def __init__(self, dbCon):
        Toplevel.__init__(self)
        self.geometry("800x600")
        self.flag = flag
        self.dbDict = dbDict
        self.fDict = fDict
        self.dbName = ''
        self.dbCon = dbCon

        # Initialize attribute options
        self.ribbonVar = IntVar()
        self.imgColVar = IntVar()

        self.dropdownChoices = [ 'From-To', 'Timespan', 'Ισοζύγιο' ]
        self.ribbonDropdownVar = StringVar()
        self.ribbonType = 0

        # Initialize the user interface
        self.el = self.init_gui()
  
        if flag == 0:
            self.dbDict = queries.loadDatabases(self.dbCon)
            # Populate treeview with form names
            for k, v in self.dbDict.items():
                self.tree.insert('', 'end', iid=k, values=(k, v))

    def init_gui(self):
        """Builds GUI."""
        return elements.Elements.create_widgets(self)
        
    def update_form(self):
        formId = self.tree.focus()
        
        dl = dialog.MyDialog(self, 'Είστε σίγουροι ότι θέλετε να αλλάξετε τη φόρμα No.' + formId + ';').show()
        
        if dl == True:
            # INSERT PROGRESS BAR CALL HERE
            queries.updateForm(self.dbCon, self.dbName, formId, self.check_ribbon(), self.ribbonType, self.check_imgCol())
            
    def restore_form(self):
        formId = self.tree.focus()
        dl = dialog.MyDialog(self, 'Είστε σίγουροι ότι θέλετε να επαναφέρετε τη φόρμα No.' + formId + ';').show()
        
        if dl == True:
            queries.updateForm(self.dbCon, formId, self.check_ribbon, self.ribbonType, self.check_imgCol)

    def new_form(self):
        nextId = max(formIds) + 1
        self.dbCon.executeScriptsFromFile("scripts\Insert_Form.sql")
        xml = xmlhandler.FormXml()
        for child in xml.get_xml():
            print(child.tag, child.attrib)

    def use_database(self):
                
        isUsed = self.flag

        if isUsed == 0:
            selectedDatabaseId = self.tree.focus()        
            selectedDatabaseName = queries.getSelectedDatabaseName(self.dbCon, selectedDatabaseId)
            
            self.flag = 1
            for i in self.tree.get_children():
                self.tree.delete(i)
            
            self.fDict = queries.loadForms(self.dbCon, selectedDatabaseName)
            
            # Populate treeview with form names
            for k, v in self.fDict.items():
                self.tree.insert('', 'end', iid=k, values=(k, v))    

            elements.Elements.changeText(self, 'Exit DB')
            elements.Elements.showButtons(self)
            self.dbName = selectedDatabaseName

        elif isUsed == 1:
            self.flag = 0
            self.dbDict = queries.loadDatabases(db)

            # Clear the tree
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Populate treeview with database names
            for k, v in self.dbDict.items():
                self.tree.insert('', 'end', iid=k, values=(k, v)) 
            
            elements.Elements.changeText(self, 'Use DB')
            elements.Elements.hideButtons(self)
            
    def exit_manager(self):
        self.quit()

    # Checkbox methods for each attribute
    def check_ribbon(self):
        return self.ribbonVar.get()

    def check_imgCol(self):
        return self.imgColVar.get()

    def choice_ribbon(self, value):
        if value == 'From-To':
            self.ribbonType = 0
        elif value == 'Timespan':
            self.ribbonType = 1
        elif value == 'Ισοζύγιο':
            self.ribbonType = 2



            