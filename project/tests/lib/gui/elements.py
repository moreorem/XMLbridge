from tkinter import ttk

class Elements:
    def create_widgets(self):
        
        # New button
        self.new_button = ttk.Button(self, text='Create New Form', command = self.new_form)
    
        # Use button
        self.use_button = ttk.Button(self, text='Use Database', command = self.use_database)
        
        self.update_btngroup = ttk.Frame(self)   
        # Update button
        self.update_button = ttk.Button(self.update_btngroup, text='Update Form', command = self.update_form)
    
        # Restore button
        self.restore_button = ttk.Button(self.update_btngroup, text='Undo Last Update', command = self.restore_form)

        self.xml_btngroup = ttk.Frame(self)
        # Download form button
        self.downloadform_button = ttk.Button(self.xml_btngroup, text='Download XML', command = self.download_form)

        # Exit button
        self.exit_button = ttk.Button(self, text = "QUIT", command = self.exit_manager)

        # Treeview
        self.tree = ttk.Treeview(self, columns = ('ID', 'Form Name'))
        self.tree.column('#0', width = 0)
        self.tree.heading('#1', text = 'IDCID')
        self.tree.heading('#2', text = 'Form Name')

        # Scrollbar
        self.treeScroll = ttk.Scrollbar(self)
        # Connect scrollbar to treeview
        self.treeScroll.configure(command = self.tree.yview)
        self.tree.configure(yscrollcommand = self.treeScroll.set)
        
        # Checkboxes
        self.attrContainer = ttk.Frame(self)
        self.checkRibbon = ttk.Checkbutton(self.attrContainer, text = 'Ribbon Control', variable = self.ribbonVar, command = self.check_ribbon)
        self.checkImgCol = ttk.Checkbutton(self.attrContainer, text = 'Image Collection', variable = self.imgColVar, command = self.check_imgCol)
        
        # Dropdowns
        self.ddRibbonType = ttk.OptionMenu(self.attrContainer, self.ribbonDropdownVar, self.dropdownChoices[0], *self.dropdownChoices, command = self.choice_ribbon)

        # Progress Bar
        self.progress = ttk.Progressbar(self, orient = 'horizontal', length = 200, mode = 'indeterminate')


        # Pack everything

        self.tree.pack(side = 'left', fill = 'y')
        self.treeScroll.pack(side = 'left', fill = 'y')
        
        self.attrContainer.pack(side = 'right', anchor = 'ne')
        
        self.progress.pack(side = 'bottom', anchor = 'se')

        self.exit_button.pack(anchor = 's', side = 'bottom')
        
        self.use_button.pack(side = 'top', anchor = 'nw')
        
        self.update_btngroup.pack(anchor = 'nw')
        
        self.xml_btngroup.pack(anchor = 'nw')
        

    def hideButtons(self):
        # Hide attribute elements
        self.new_button.pack_forget()
        self.checkImgCol.pack_forget()
        self.ddRibbonType.pack_forget()
        self.checkRibbon.pack_forget()
        
        # Hide buttons
        self.update_button.pack_forget()
        self.restore_button.pack_forget()
        self.new_button.pack_forget()
        self.downloadform_button.pack_forget()

    def showButtons(self):
        # Show attribute elements
        self.checkImgCol.pack(anchor = 'ne', ipadx = 5)
        self.ddRibbonType.pack(anchor = 'ne', side = 'right', ipadx = 2)
        self.checkRibbon.pack(anchor = 'ne', side = 'right', ipadx = 5)
        
        # Show buttons
        self.new_button.pack()
        self.update_button.pack(ipadx = 12, side = 'top')
        self.restore_button.pack(side = 'top')
        self.new_button.pack(side = 'top', anchor = 'nw')
        self.downloadform_button.pack(side = 'top', anchor = 'nw')

    def changeText(self, text):
        self.use_button["text"] = str(text)

    def disableElements(self):
        self.buttons.config(state='DISABLED')
    
