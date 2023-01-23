import sys
from os.path import exists
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QComboBox, QMenu, QMessageBox, QInputDialog, QLineEdit,
    QGroupBox, QSpinBox, QLayout
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction, QPixmap


import database
from utilities import formulas, natures_util
class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pocket Journal HGSS v.0.1")
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.master_canvas = QWidget()
        self.master_layout = QVBoxLayout()
        self.master_layout.setSizeConstraint(QLayout.SetFixedSize)

        # Database
        self.db = database.Database()
        
        # Init
        self.create_layer_one()
        self.create_layer_two()
        self.create_layer_three()
        self.create_layer_four()

        self.master_canvas.setLayout(self.master_layout)
        self.setCentralWidget(self.master_canvas)

        self.setFixedSize(self.master_canvas.sizeHint())
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
        self.party_box.currentIndexChanged.connect(self.update_data_shown)

        # Menu
        self.menu = QMenu()
        self.menu_btn = QPushButton(icon=QIcon("resources/icons/menu.png"))
        self.menu_btn.setMenu(self.menu)
        #Actions
        self.rename_action = QAction("Rename")
        self.menu.addAction(self.rename_action)
        self.rename_action.triggered.connect(self.rename_party)
        self.evolve_action = QAction("Evolve")
        self.menu.addAction(self.evolve_action)
        self.evolve_action.triggered.connect(self.evolve_party)
        self.remove_action = QAction("Remove from Party")
        self.menu.addAction(self.remove_action)
        self.remove_action.triggered.connect(self.remove_from_party)

        # Level
        level_label = QLabel("Level: ")
        self.level = QSpinBox()
        self.level.setValue(0)
        self.level.setMaximum(100)
        
        # Nature box
        self.nature_box = QComboBox()
        self.nature_box.addItem("Nature..")
        for item in self.db.get_natures_names():
            self.nature_box.addItem(item)
        self.nature_box.currentIndexChanged.connect(self.nature_box_changed)

        # Current Location
        self.location_box = QComboBox()
        self.location_box.addItem("Current Location..")
        for item in self.db.get_routes_names():
            self.location_box.addItem(item)
        self.location_box.currentIndexChanged.connect(self.update_wild)



        self.layer_one.addWidget(self.party_box)
        self.layer_one.addWidget(self.menu_btn)
        # self.layer_one.addStretch()
        self.layer_one.addWidget(self.location_box)
        self.layer_one.addWidget(level_label)
        self.layer_one.addWidget(self.level)
        self.layer_one.addStretch()
        self.layer_one.addWidget(self.nature_box)
        self.master_layout.addLayout(self.layer_one)

    def create_layer_two(self):
        self.layer_two = QHBoxLayout()
        self.layer_two.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.base_stats_group = QGroupBox("Base Stats")
        self.stats_group = QGroupBox("Stats")
        self.evs_group = QGroupBox("EVs")
        self.ivs_group = QGroupBox("IVs")

        stats = ["HP", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]

        base_labels_layout = QVBoxLayout()
        base_values_layout = QVBoxLayout()
        base_values_layout.setContentsMargins(20, 0, 0, 0)
        base_layout = QHBoxLayout()
        self.current_base_stats = []
        self.stat_labels = []
        for item in stats:
            label = QLabel(item)
            value = QLabel("-")
            value.setFixedWidth(20)
            value.setAlignment(Qt.AlignCenter)
            self.stat_labels.append(label)
            self.current_base_stats.append(value)
        for item in self.current_base_stats:
            base_values_layout.addWidget(item)
        for item in self.stat_labels:
            base_labels_layout.addWidget(item)

        base_layout.addLayout(base_labels_layout)
        base_layout.addLayout(base_values_layout)
        self.base_stats_group.setLayout(base_layout)

        stats_layout = QVBoxLayout()
        self.current_stats = []
        for item in stats:
            value = QSpinBox()
            value.setMinimum(0)
            value.setMaximum(1000)
            value.setFixedWidth(50)
            self.current_stats.append(value)
        for item in self.current_stats:
            stats_layout.addWidget(item)
        self.stats_group.setLayout(stats_layout)

        evs_layout = QVBoxLayout()
        self.current_evs = []
        for item in stats:
            value = QSpinBox()
            value.setMinimum(0)
            value.setMaximum(255)
            value.setFixedWidth(50)
            self.current_evs.append(value)
        for item in self.current_evs:
            evs_layout.addWidget(item)
        self.evs_group.setLayout(evs_layout)

        ivs_layout = QVBoxLayout()
        self.current_ivs = []
        for item in stats:
            label = QLabel("-")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(50)
            self.current_ivs.append(label)
        for item in self.current_ivs:
            ivs_layout.addWidget(item)
        self.ivs_group.setLayout(ivs_layout)

        self.sprite = QIcon("resources/sprites/pokeball.png")
        self.sprite_btn = QPushButton(icon=self.sprite)
        self.sprite_btn.setIconSize(QSize(80, 80))
        self.sprite_btn.clicked.connect(self.show_data)

        # self.stats_group.setContentsMargins(2, 0, 5, 0)
        # self.stats_group.setFixedWidth(80)
        # self.evs_group.setContentsMargins(2, 0, 5, 0)
        # self.evs_group.setFixedWidth(80)
        # self.ivs_group.setContentsMargins(2, 0, 5, 0)
        # self.ivs_group.setFixedWidth(80)




        self.layer_two.addWidget(self.base_stats_group)
        self.layer_two.addWidget(self.stats_group)
        self.layer_two.addWidget(self.evs_group)
        self.layer_two.addWidget(self.ivs_group)
        self.layer_two.addWidget(self.sprite_btn) 
        self.master_layout.addLayout(self.layer_two)

        # Style object names
        self.base_stats_group.setObjectName("base-group")
        self.sprite_btn.setObjectName("sprite-btn")
        self.master_canvas.setObjectName("canvas")

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
        
        
        
        # Calculate Ivs Button
        self.ivs_btn = QPushButton("Calculate IVs")
        self.ivs_btn.clicked.connect(self.calculate_ivs)

        self.update_party_data_btn = QPushButton("Update Stats")
        self.update_party_data_btn.setToolTip("Updates the stats and evs of the currently selected party Pokémon and stores the info in the database.")
        self.update_party_data_btn.clicked.connect(self.store_party_data)
        self.ivs_btn.setToolTip("Calculates the Individual Values of the selected Pokémon in the party and displays them.")

        self.layer_three.addWidget(self.dex_box)
        # button_layout = QHBoxLayout()
        # button_layout.addWidget(self.add_to_party_btn)
        # button_layout.addWidget(self.update_party_data_btn)
        # button_layout.addWidget(self.ivs_btn)
        # self.layer_three.addLayout(button_layout)
        # button_layout.setContentsMargins(17, 0, 0, 0)
        self.layer_three.addWidget(self.add_to_party_btn)
        self.layer_three.addWidget(self.update_party_data_btn)
        self.layer_three.addWidget(self.ivs_btn)
        self.master_layout.addLayout(self.layer_three)
    
    def create_layer_four(self):
        self.layer_four = QHBoxLayout()
        self.layer_four.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.encounter_box = QComboBox()
        self.encounter_box.setFixedWidth(100)
        self.encounter_box.addItem("Wild..")
        self.encounter_box.setToolTip("Pokémon found in the current location")

        self.add_ev_btn = QPushButton("Add EV")
        self.add_ev_btn.setToolTip("""Adds ev yields, from the Pokémon on the left box, to the selected Pokémon in your Party
Useful if you don't know the Pokémon's ev yields by heart.""")
        self.add_ev_btn.clicked.connect(self.add_evs)

        # Get pokemon on current location_box
        # Add them

        self.layer_four.addWidget(self.encounter_box)
        # button_layout = QHBoxLayout()
        # button_layout.setContentsMargins(17, 0, 0, 0)
        # button_layout.addWidget(self.add_ev_btn)
        self.layer_four.addWidget(self.add_ev_btn)
        self.master_layout.addLayout(self.layer_four)

    def reset_entries(self):
        for item in self.current_base_stats:
            item.setText("-")
        for item in self.current_stats:
            item.setValue(0)
        for item in self.current_evs:
            item.setValue(0)
        for item in self.current_ivs:
            item.setText("-")
        for item in self.stat_labels:
            item.setStyleSheet("color: black;")
        self.level.setValue(0)
        self.nature_box.setCurrentIndex(0)
        self.sprite = QIcon("resources/sprites/pokeball.png")
        self.sprite_btn.setIcon(self.sprite)
        self.sprite_btn.setToolTip("")

    # Party Related functions
    def show_data(self):
        pass

    def rename_party(self):
        name = self.party_box.currentText()
        if name == "Party box..":
            return
        else:
            new_name = self.dialog_nickname_add_party(original_name=name)
            if not new_name:
                return
            # print(new_name)
            # Update db.party
            new_poke = self.db.rename_party(name, new_name)
            # Update party box
            self.party_box.removeItem(self.party_box.findText(name))
            self.party_box.setCurrentIndex(0)
            self.party_box.addItem(new_name)
            self.party_box.setCurrentIndex(self.party_box.count()-1)

    def evolve_party(self):
        poke = self.party_box.currentText()
        if poke == "Party box..":
            return
        else:
            evolution = self.db.get_evolution(poke)
            if evolution not in self.db.get_dex_names():
                self.warning("Data missing", f"{poke}'s evolution not found in database.")
                return
            # Warning to evolve
            msg = f"Evolve {poke} into {evolution}"
            answer = self.dialog("Evolution", msg) 
            if answer:
                if poke == self.db.get_real_name(poke):
                    new_nick = self.db.get_evolution(poke)
                else:
                    new_nick = self.dialog_nickname_add_party(original_name=self.db.get_evolution(poke))
                    if not new_nick:
                        print("Evolution cancelled.")
                        return
                self.db.evolve(poke, new_nick=new_nick)
                # Update party box
                self.party_box.removeItem(self.party_box.findText(poke))
                self.party_box.setCurrentIndex(0)
                self.party_box.addItem(new_nick)
                self.party_box.setCurrentIndex(self.party_box.count()-1)
            else:
                print("Evolution cancelled.")

    def update_data_shown(self):
        """ Updates content shown when a new poke is added to the party or when party index changes """
        # Update base stats
        poke = self.party_box.currentText()
        if poke == "Party box..":
            self.reset_entries()
            return
        else:
            for item in self.current_ivs:
                item.setText("-")
            self.sprite_btn.setToolTip(f"Click to view {poke} data")
            sprite_path = f"resources/sprites/{self.db.find_dex_number(poke)}.png"
            if exists(sprite_path):
                sprite = QIcon(f"resources/sprites/{self.db.find_dex_number(poke)}.png")
                self.sprite_btn.setIcon(sprite)
            else:
                sprite = QIcon("resources/sprites/not_found.png")
                self.sprite_btn.setIcon(sprite)

            base_stats = self.db.get_base_stats(poke)
            for number in range(len(self.current_base_stats)):
                self.current_base_stats[number].setText(base_stats[number])
            
            # Look for party data and update data shown
            data = self.db.get_party_data(poke)
            if data:
                for item in range(len(self.current_stats)):
                    self.current_stats[item].setValue(data["stats"][item])
                for item in range(len(self.current_evs)):
                    self.current_evs[item].setValue(data["evs"][item])
                if data["nature"]:
                    self.nature_box.setCurrentIndex(self.nature_box.findText(data["nature"]))
                    self.highlight_natured_stats()
                else:
                    self.nature_box.setCurrentIndex(0)
                self.level.setValue(data["level"])
            # --> Update party visuals function call here
    
    def highlight_natured_stats(self):
        nature = self.nature_box.currentText()
        stats = ["HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"]
        for item in range(len(stats)):
            # print(natures_util.assert_nature_modifier(nature, self.stat_labels[item].text()))
            if natures_util.assert_nature_modifier(nature, stats[item]) == 1.1:
                self.stat_labels[item].setStyleSheet("color: #d7a3a7;")
            elif natures_util.assert_nature_modifier(nature, stats[item]) == 0.9:
                self.stat_labels[item].setStyleSheet("color: #83aaed;")
            else:
                self.stat_labels[item].setStyleSheet("color: black;")
    
    def nature_box_changed(self):
        nature = self.nature_box.currentText()
        if self.nature_box.currentIndex() == 0:
            pass
        elif self.party_box.currentIndex() == 0:
            pass
        else:
            stats = ["HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"]
            for item in range(len(stats)):
                # print(natures_util.assert_nature_modifier(nature, self.stat_labels[item].text()))
                if natures_util.assert_nature_modifier(nature, stats[item]) == 1.1:
                    self.stat_labels[item].setStyleSheet("color: #d7a3a7;")
                elif natures_util.assert_nature_modifier(nature, stats[item]) == 0.9:
                    self.stat_labels[item].setStyleSheet("color: #83aaed;")
                else:
                    self.stat_labels[item].setStyleSheet("color: black;")


    def store_party_data(self):
        poke = self.party_box.currentText()
        if poke == "Party box..":
            return
        else:
            stats = [item.value() for item in self.current_stats]
            evs = [item.value() for item in self.current_evs]
            level = self.level.value()
            nature = self.nature_box.currentText()
            if nature == "Nature..":
                self.warning("Invalid Nature", "Please select the nature of your Pokémon")
            else:
                self.db.update_party(poke, stats, evs, level, nature)

    def remove_from_party(self):
        poke = self.party_box.currentText()
        if poke == "Party box..":
            return
        else:
            # Remove from party_box
            self.party_box.setCurrentIndex(0)
            index_to_remove = self.party_box.findText(poke)
            self.party_box.removeItem(index_to_remove)
            # Remove from db.party
            self.db.remove_from_party(poke)
            # Save party db
            self.db.save_party()
        
    def update_wild(self):
        if self.location_box.currentIndex() == 0:
            # Reset encounter_box
            self.encounter_box.clear()
            self.encounter_box.addItem("Wild..")
            return
        pokes = self.db.get_route_wilds(self.location_box.currentText())
        self.encounter_box.clear()
        self.encounter_box.addItem("Wild..")
        for item in pokes:
            self.encounter_box.addItem(item)

    # Button Functions
    def add_evs(self):
        poke = self.encounter_box.currentText()
        if poke == "Wild..":
            return
        elif self.party_box.currentIndex() == 0:
            self.warning("Party", "Select a Pokémon in your party.")
            return
        else:
            ev_yields = self.db.get_ev_yields(poke)
            if not ev_yields:
                self.warning("Missing Data", f"{poke} data does not appear to be in the database")
                return
            else:
                for item in range(len(self.current_evs)):
                    self.current_evs[item].setValue(self.current_evs[item].value() + int(ev_yields[item]))

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
                    self.party_box.setCurrentIndex(self.party_box.count()-1) # --> this will trigger party_box.currentIndexChanged()
                    # reset dex_box
                    self.dex_box.setCurrentIndex(0)
                    
                else:
                    print("Action cancelled.")
            else:
                pass
    
    def calculate_ivs(self):
        poke = self.party_box.currentText()
        if poke == "Party box..":
            return
        elif self.nature_box.currentIndex() == 0:
            self.warning("Invalid Nature", "Please select the nature of your Pokémon")
            return
        else:
            self.store_party_data()
            for item in self.current_ivs:
                item.setStyleSheet("color: black;")
            base = self.db.get_base_stats(poke)
            evs = self.db.get_evs(poke)
            stats = self.db.get_stats(poke)
            level = self.db.get_level(poke)
            base_nature = self.db.get_nature(poke)
            
            hp_iv = formulas.calculate_hp_iv(int(base[0]), evs[0], level, stats[0])

            nature = natures_util.assert_nature_modifier(base_nature, "Attack")
            attack_iv = formulas.calculate_stat_iv(int(base[1]), evs[1], level, nature, stats[1])

            nature = natures_util.assert_nature_modifier(base_nature, "Defense")
            defense_iv = formulas.calculate_stat_iv(int(base[2]), evs[2], level, nature, stats[2])

            nature = natures_util.assert_nature_modifier(base_nature, "Special Attack")
            sp_attack_iv = formulas.calculate_stat_iv(int(base[3]), evs[3], level, nature, stats[3])

            nature = natures_util.assert_nature_modifier(base_nature, "Special Defense")
            sp_defense_iv = formulas.calculate_stat_iv(int(base[4]), evs[4], level, nature, stats[4])

            nature = natures_util.assert_nature_modifier(base_nature, "Speed")
            speed_iv = formulas.calculate_stat_iv(int(base[5]), evs[5], level, nature, stats[5])
            try:
                self.current_ivs[0].setText(f"{hp_iv[0]}-{hp_iv[-1]}")
            except TypeError:
                self.current_ivs[0].setText("Error")
                self.current_ivs[0].setStyleSheet("color: red;")

            try:
                self.current_ivs[1].setText(f"{attack_iv[0]}-{attack_iv[-1]}")
            except TypeError:
                self.current_ivs[1].setText("Error")
                self.current_ivs[1].setStyleSheet("color: red;")
            try:
                self.current_ivs[2].setText(f"{defense_iv[0]}-{defense_iv[-1]}")
            except TypeError:
                self.current_ivs[2].setText("Error")
                self.current_ivs[2].setStyleSheet("color: red;")
            try:
                self.current_ivs[3].setText(f"{sp_attack_iv[0]}-{sp_attack_iv[-1]}")
            except TypeError:
                self.current_ivs[3].setText("Error")                
                self.current_ivs[3].setStyleSheet("color: red;")
            try:
                self.current_ivs[4].setText(f"{sp_defense_iv[0]}-{sp_defense_iv[-1]}")
            except TypeError:
                self.current_ivs[4].setText("Error")
                self.current_ivs[4].setStyleSheet("color: red;")
            try:
                self.current_ivs[5].setText(f"{speed_iv[0]}-{speed_iv[-1]}")
            except TypeError:
                self.current_ivs[5].setText("Error")
                self.current_ivs[5].setStyleSheet("color: red;")

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
    
    def warning(self, title, msg):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)

        done = msg_box.exec()

    def dialog(self, title, msg):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(f"{msg}?")
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        decision = msg_box.exec()
        if decision == QMessageBox.Ok:
            return True
        else:
            return False

    def dialog_nickname_add_party(self, original_name=None):
        if not original_name:
            poke = self.dex_box.currentText()
        else:
            poke = original_name
        current_party = list(self.db.party.keys())
        nickname = poke
        try:
            real_name = self.db.get_real_name(nickname) + " nickname: "
        except KeyError:
            real_name = "Nickname: "
        while nickname in current_party:
            old_nickname = nickname
            nickname, ok = QInputDialog.getText(self, f"{real_name}", f"{old_nickname} already taken!\nNew Pokémon nickname:",
                                                QLineEdit.Normal, poke)
            if nickname == "":
                nickname = old_nickname
            if not ok:
                return None
        return nickname
            

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("main_theme.qss", "r") as file:
        app.setStyleSheet(file.read())
    window = App()
    sys.exit(app.exec())


# TODO
# tweak visuals (IN PROGRESS)
    # Highlight when IV is 100% precise
# run & test   
# Second window for advanced data
# If idle for 2 seconds --> save party_db
# Resize window --> disable!