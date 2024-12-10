import sys
import sqlite3
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QMessageBox, QHeaderView, QComboBox)


class GestionModules(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Modules")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #f0f0f0; color: #333333;")
        self.setWindowIcon(QIcon("Icons/iconUni.png"))
        self.initDB()
        self.initUI()
        self.load_data()

    def initDB(self):
        self.conn = sqlite3.connect("scolarite.db")
        self.conn.execute("PRAGMA foreign_keys = ON") 
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
           CREATE TABLE IF NOT EXISTS Module (
            module_id INTEGER PRIMARY KEY,
            etudiant_num_apogee INTEGER,
            prof_matricule INTEGER,
            nom TEXT, 
            FOREIGN KEY (etudiant_num_apogee) REFERENCES Etudiant(num_apogee),
            FOREIGN KEY (prof_matricule) REFERENCES Prof(immatriculation)
        );
        ''')
        self.conn.commit()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout_principal = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.input_module_id = QLineEdit()
        self.input_module_id.setPlaceholderText("ID du module")
        self.input_etudiant_apogee = QLineEdit()
        self.input_etudiant_apogee.setPlaceholderText("Numéro Apogée Étudiant")
        self.input_prof_matricule = QLineEdit()
        self.input_prof_matricule.setPlaceholderText("Matricule Professeur")
        self.input_nom_module = QLineEdit()
        self.input_nom_module.setPlaceholderText("Nom du Module")

        form_layout.addWidget(QLabel("ID du module:"))
        form_layout.addWidget(self.input_module_id)
        form_layout.addWidget(QLabel("Numéro Apogée Étudiant:"))
        form_layout.addWidget(self.input_etudiant_apogee)
        form_layout.addWidget(QLabel("Matricule Professeur:"))
        form_layout.addWidget(self.input_prof_matricule)
        form_layout.addWidget(QLabel("Nom du Module:"))
        form_layout.addWidget(self.input_nom_module)
        layout_principal.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.bouton_ajouter = QPushButton("Ajouter")
        self.bouton_ajouter.setStyleSheet("background-color: #28a745; color: white;")  # Vert
        self.bouton_ajouter.clicked.connect(self.ajouter_module)

        self.bouton_modifier = QPushButton("Modifier")
        self.bouton_modifier.setStyleSheet("background-color: #4165D5; color: white;")  # Bleu
        self.bouton_modifier.clicked.connect(self.modifier_module)

        self.bouton_supprimer = QPushButton("Supprimer")
        self.bouton_supprimer.setStyleSheet("background-color: #CC0000; color: white;")  # Rouge
        self.bouton_supprimer.clicked.connect(self.supprimer_module)

        button_layout.addWidget(self.bouton_ajouter)
        button_layout.addWidget(self.bouton_modifier)
        button_layout.addWidget(self.bouton_supprimer)
        layout_principal.addLayout(button_layout)

        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un module")
        self.search_bar.textChanged.connect(self.filtrer_tableau)
        search_layout.addWidget(QLabel("Recherche:"))
        search_layout.addWidget(self.search_bar)
        layout_principal.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID du Module", "Numéro Apogée Étudiant", "Matricule Professeur", "Nom"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemClicked.connect(self.remplir_champs)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #4165D5;
                border: 2px solid #4165D5;
            }
            QTableWidget::item {
                background-color: #F5F9FF;
                color: #333333;
            }
            QTableWidget::item:selected {
                background-color: #4165D5;
                color: white;
            }
            QHeaderView::section {
                background-color: #4165D5;
                color: white;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #D0D0D0;
            }
        """)

        layout_principal.addWidget(self.table)
        self.central_widget.setLayout(layout_principal)

    def load_data(self):
        self.table.setRowCount(0)
        self.cursor.execute("SELECT * FROM Module")
        for row_data in self.cursor.fetchall():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))


    def filtrer_tableau(self):
        recherche = self.search_bar.text().strip().lower()
        self.table.setRowCount(0)
        query = "SELECT * FROM Module WHERE module_id LIKE ? OR etudiant_num_apogee LIKE ? OR prof_matricule LIKE ? OR LOWER(nom) LIKE ?"
        valeurs = (f"%{recherche}%", f"%{recherche}%", f"%{recherche}%", f"%{recherche}%")
        self.cursor.execute(query, valeurs)
        for row_data in self.cursor.fetchall():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))


    def ajouter_module(self):
        module_id = self.input_module_id.text().strip()
        etudiant_apogee = self.input_etudiant_apogee.text().strip()
        prof_matricule = self.input_prof_matricule.text().strip()
        nom_module = self.input_nom_module.text().strip()

        if not module_id or not etudiant_apogee or not prof_matricule or not nom_module:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO Module (module_id, etudiant_num_apogee, prof_matricule, nom) VALUES (?, ?, ?, ?)",
                (module_id, etudiant_apogee, prof_matricule, nom_module))
            self.conn.commit()

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(module_id))
            self.table.setItem(row_position, 1, QTableWidgetItem(etudiant_apogee))
            self.table.setItem(row_position, 2, QTableWidgetItem(prof_matricule))
            self.table.setItem(row_position, 3, QTableWidgetItem(nom_module))

            self.input_module_id.clear()
            self.input_etudiant_apogee.clear()
            self.input_prof_matricule.clear()
            self.input_nom_module.clear()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'ajout : {e}")

    def modifier_module(self):
        index = self.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un module à modifier.")
            return

        module_id = self.input_module_id.text().strip()
        etudiant_apogee = self.input_etudiant_apogee.text().strip()
        prof_matricule = self.input_prof_matricule.text().strip()
        nom_module = self.input_nom_module.text().strip()

        if not module_id or not etudiant_apogee or not prof_matricule or not nom_module:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        self.cursor.execute(
            "UPDATE Module SET etudiant_num_apogee = ?, prof_matricule = ?, nom = ? WHERE module_id = ?",
            (etudiant_apogee, prof_matricule, nom_module, module_id))
        self.conn.commit()

        self.table.setItem(index, 0, QTableWidgetItem(module_id))
        self.table.setItem(index, 1, QTableWidgetItem(etudiant_apogee))
        self.table.setItem(index, 2, QTableWidgetItem(prof_matricule))
        self.table.setItem(index, 3, QTableWidgetItem(nom_module))

        QMessageBox.information(self, "Succès", "Le module a été modifié avec succès.")

    def supprimer_module(self):
        index = self.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un module à supprimer.")
            return

        module_id = self.table.item(index, 0).text()
        self.cursor.execute("DELETE FROM Module WHERE module_id = ?", (module_id,))
        self.conn.commit()
        self.table.removeRow(index)

        QMessageBox.information(self, "Succès", "Le module a été supprimé avec succès.")

    def remplir_champs(self, item):
        index = self.table.currentRow()
        self.input_module_id.setText(self.table.item(index, 0).text())
        self.input_etudiant_apogee.setText(self.table.item(index, 1).text())
        self.input_prof_matricule.setText(self.table.item(index, 2).text())
        self.input_nom_module.setText(self.table.item(index, 3).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = GestionModules()
    main_win.show()
    sys.exit(app.exec_())