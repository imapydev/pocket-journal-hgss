import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QComboBox, QMenu, QMessageBox, QInputDialog, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction


import database

class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.master_canvas = QWidget()
        self.master_layout = QVBoxLayout()

        # Database
        self.db = database.Database()
        
        # Init
        self.create_layer_one()
        # --> create layer 2 goes here
        self.create_layer_three()

    
        

        self.master_canvas.setLayout(self.master_layout)
        self.setCentralWidget(self.master_canvas)
        self.show()

    # Layer creations
    def create_layer_one(self):
        self.layer_one = QHBoxLayout()

        # Party Combobox
        self.party_box = QComboBox()
        self.party_box.setFixedWidth(100)
        self.layer_one.setAlignment(Qt.AlignLeft | Qt.AlignTop )
        self.party_box.addItem("Party box..")
        # Populate party_box
        party_names = self.db.get_party_names()
        for item in party_names:
            self.party_box.addItem(item)

        # Menu
        self.menu = QMenu()
        self.menu_btn = QPushButton(icon=QIcon("resources/icons/menu.png"))
        self.menu_btn.setMenu(self.menu)
        #Actions
        self.rename_action = QAction("Rename")
        self.menu.addAction(self.rename_action)
        # --> rename function connect goes here
        self.evolve_action = QAction("Evolve")
        self.menu.addAction(self.evolve_action)
        # --> evolve function connect goes here
        self.remove_action = QAction("Remove from Party")
        self.menu.addAction(self.remove_action)
        # --> remove from party function connet goes here




        self.layer_one.addWidget(self.party_box)
        self.layer_one.addWidget(self.menu_btn)
        self.master_layout.addLayout(self.layer_one)

    def create_layer_three(self):
        self.layer_three = QHBoxLayout()
        self.layer_three.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Dex Combobox
        self.dex_box = QComboBox()
        self.dex_box.setFixedWidth(100)
        self.dex_box.addItem("Pokédex..")
        dex_names = self.db.get_dex_names()
        for item in dex_names:
            self.dex_box.addItem(item)

        # Buttons
        self.add_to_party_btn = QPushButton("Add to Party")
        self.add_to_party_btn.setToolTip("Adds the Pokémon on the left box to your party")
        self.add_to_party_btn.clicked.connect(self.add_to_party)
        self.add_ev_btn = QPushButton("Add EV")
        self.add_ev_btn.setToolTip("Adds ev yields, from the Pokémon on the left box, to the selected Pokémon in your Party")

        self.layer_three.addWidget(self.dex_box)
        self.layer_three.addWidget(self.add_to_party_btn)
        self.layer_three.addWidget(self.add_ev_btn)
        self.master_layout.addLayout(self.layer_three)

    # Party Related functions
    def party_updated(self):
        # set party item to last
        self.party_box.setCurrentIndex(self.party_box.count()-1)
        # Update base stats
        # --> update base stats funtion call here
        # Update party stats/evs/sprite shown
        # --> Update party visuals function call here
        # Save party to db file
        self.db.save_party()

    # Button Functions
    def add_to_party(self):
        poke = self.dex_box.currentText()
        if poke == "Pokédex..":
            return
        else:
            if self.dialog_add_party():
                print("Ready to add to party.")
                # Name Selection
                # Default should be the real name
                nickname = self.dialog_nickname_add_party()
                if nickname:
                    print(f"{nickname} added to party!")
                    # Add nickname to db.party with basic info
                    self.db.add_to_party(nickname, poke)
                    # Add nickname to party_box
                    self.party_box.addItem(nickname)
                    # Update things shown in layer 2
                    self.party_updated()
                else:
                    print("Action cancelled.")
            else:
                pass
    
    # Dialog/Message functions
    def dialog_add_party(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(f"Add {self.dex_box.currentText()} to party?")
        msg_box.setWindowTitle("Pokémon caught!")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        decision = msg_box.exec()
        if decision == QMessageBox.Ok:
            return True
        else:
            return False

    def dialog_nickname_add_party(self):
        poke = self.dex_box.currentText()
        current_party = list(self.db.party.keys())
        nickname = poke
        while nickname in current_party:
            old_nickname = nickname
            nickname, ok = QInputDialog.getText(self, "Nickname: ", f"{old_nickname} already taken!\nNew Pokémon nickname:",
                                                QLineEdit.Normal, poke)
            if nickname == "":
                nickname = old_nickname
            if not ok:
                return None
        
        return nickname
            




app = QApplication(sys.argv)
window = App()
app.exec()