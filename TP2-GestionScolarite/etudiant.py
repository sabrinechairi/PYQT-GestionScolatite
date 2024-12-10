import sys
import sqlite3
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QMessageBox, QHeaderView, QComboBox)

class GestionScolarite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Étudiants")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #f0f0f0; color: #333333;")
        self.setWindowIcon(QIcon("Icons/iconUni.png"))
        self.initDB()
        self.initUI()
        self.load_data()

    def initDB(self):
        self.conn = sqlite3.connect("scolarite.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Etudiant (
            id INTEGER ,
            nom TEXT,
            prenom TEXT,
            num_apogee INTEGER PRIMARY KEY,
            master TEXT
        )''')
        self.conn.commit()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout_principal = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID")
        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Nom")
        self.input_prenom = QLineEdit()
        self.input_prenom.setPlaceholderText("Prénom")
        self.input_num_apogee = QLineEdit()
        self.input_num_apogee.setPlaceholderText("Numéro Apogé")
        self.input_master = QComboBox()
        self.input_master.addItems(["B2S", "MQSE", "MRF", "MLAI",
            "CARA", "IBGE", "MM", "GPM",
            "MQL", "M2I", "MGEER"])

        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.input_id)
        form_layout.addWidget(QLabel("Nom:"))
        form_layout.addWidget(self.input_nom)
        form_layout.addWidget(QLabel("Prénom:"))
        form_layout.addWidget(self.input_prenom)
        form_layout.addWidget(QLabel("Numéro Apogé:"))
        form_layout.addWidget(self.input_num_apogee)
        form_layout.addWidget(QLabel("Master:"))
        form_layout.addWidget(self.input_master)
        layout_principal.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.bouton_ajouter = QPushButton("Ajouter")
        self.bouton_ajouter.setStyleSheet("background-color: #28a745; color: white;")
        self.bouton_ajouter.clicked.connect(self.ajouter_etudiant)

        self.bouton_modifier = QPushButton("Modifier")
        self.bouton_modifier.setStyleSheet("background-color: #4165D5; color: white;")
        self.bouton_modifier.clicked.connect(self.modifier_etudiant)

        self.bouton_supprimer = QPushButton("Supprimer")
        self.bouton_supprimer.setStyleSheet("background-color: #CC0000; color: white;")
        self.bouton_supprimer.clicked.connect(self.supprimer_etudiant)

        button_layout.addWidget(self.bouton_ajouter)
        button_layout.addWidget(self.bouton_modifier)
        button_layout.addWidget(self.bouton_supprimer)
        layout_principal.addLayout(button_layout)

        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un étudiant")
        self.search_bar.textChanged.connect(self.filtrer_tableau)
        search_layout.addWidget(QLabel("Recherche:"))
        search_layout.addWidget(self.search_bar)
        layout_principal.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Numéro Apogé", "Master"])
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
        self.cursor.execute("SELECT * FROM Etudiant")
        for row_data in self.cursor.fetchall():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))

    def filtrer_tableau(self):
        recherche = self.search_bar.text().strip().lower()
        self.table.setRowCount(0)

        query = "SELECT * FROM Etudiant WHERE id LIKE ? OR LOWER(nom) LIKE ? OR LOWER(prenom) LIKE ? OR num_apogee LIKE ? OR LOWER(master) LIKE ?"
        valeurs = (f"%{recherche}%", f"%{recherche}%", f"%{recherche}%", f"%{recherche}%", f"%{recherche}%")
        self.cursor.execute(query, valeurs)
        for row_data in self.cursor.fetchall():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))


    def valider_num_apogee(self, num_apogee):
        if not num_apogee.isdigit() or len(num_apogee) != 8:
            QMessageBox.warning(self, "Erreur", "Le numéro Apogée doit être un code composé de 8 chiffres.")
            return False
        return True


    def ajouter_etudiant(self):
        etudiant_id = self.input_id.text().strip()
        nom = self.input_nom.text().strip()
        prenom = self.input_prenom.text().strip()
        num_apogee = self.input_num_apogee.text().strip()
        master = self.input_master.currentText()

        if not etudiant_id or not nom or not prenom or not num_apogee:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        if not self.valider_num_apogee(num_apogee):
            return

        try:
            self.cursor.execute(
                "INSERT INTO Etudiant (id, nom, prenom, num_apogee, master) VALUES (?, ?, ?, ?, ?)",
                (etudiant_id, nom, prenom, num_apogee, master))
            self.conn.commit()

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(etudiant_id))
            self.table.setItem(row_position, 1, QTableWidgetItem(nom))
            self.table.setItem(row_position, 2, QTableWidgetItem(prenom))
            self.table.setItem(row_position, 3, QTableWidgetItem(num_apogee))
            self.table.setItem(row_position, 4, QTableWidgetItem(master))

            self.input_id.clear()
            self.input_nom.clear()
            self.input_prenom.clear()
            self.input_num_apogee.clear()
            self.input_master.setCurrentIndex(0)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'ajout : {e}")


    def modifier_etudiant(self):
        index = self.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un étudiant à modifier.")
            return

        etudiant_id = self.input_id.text().strip()
        nom = self.input_nom.text().strip()
        prenom = self.input_prenom.text().strip()
        num_apogee = self.input_num_apogee.text().strip()
        master = self.input_master.currentText()

        if not etudiant_id or not nom or not prenom or not num_apogee:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        if not self.valider_num_apogee(num_apogee):
            return

        self.cursor.execute(
            "UPDATE Etudiant SET nom = ?, prenom = ?, id = ?, master = ? WHERE num_apogee = ?",
            (nom, prenom, etudiant_id, master, num_apogee))
        self.conn.commit()

        self.table.setItem(index, 0, QTableWidgetItem(etudiant_id))
        self.table.setItem(index, 1, QTableWidgetItem(nom))
        self.table.setItem(index, 2, QTableWidgetItem(prenom))
        self.table.setItem(index, 3, QTableWidgetItem(num_apogee))
        self.table.setItem(index, 4, QTableWidgetItem(master))

        self.input_id.clear()
        self.input_nom.clear()
        self.input_prenom.clear()
        self.input_num_apogee.clear()
        self.input_master.setCurrentIndex(0)

        QMessageBox.information(self, "Succès", "Les informations de l'étudiant ont été modifiées avec succès.")


    def supprimer_etudiant(self):
        index = self.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un étudiant à supprimer.")
            return

        etudiant_id = self.table.item(index, 3).text()
        etudiant_id1 = self.table.item(index, 0).text()

        self.cursor.execute("DELETE FROM Etudiant WHERE num_apogee = ?", (etudiant_id,))
        self.cursor.execute("DELETE FROM Etudiant WHERE id = ?", (etudiant_id1,))
        self.conn.commit()

        self.table.removeRow(index)

        QMessageBox.information(self, "Succès", "L'étudiant a été supprimé avec succès.")

    def remplir_champs(self, item):
        index = self.table.currentRow()
        self.input_id.setText(self.table.item(index, 0).text())
        self.input_nom.setText(self.table.item(index, 1).text())
        self.input_prenom.setText(self.table.item(index, 2).text())
        self.input_num_apogee.setText(self.table.item(index, 3).text())
        self.input_master.setCurrentText(self.table.item(index, 4).text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = GestionScolarite()
    main_win.show()
    sys.exit(app.exec_())
