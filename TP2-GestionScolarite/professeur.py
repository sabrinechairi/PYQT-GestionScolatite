import sys
import sqlite3
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QMessageBox, QHeaderView, QComboBox)

class GestionProfesseurs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Professeurs")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #f0f0f0; color: #333333;")
        self.setWindowIcon(QIcon("Icons/iconUni.png"))
        self.initDB()
        self.initUI()
        self.load_data()

    def initDB(self):
        self.conn = sqlite3.connect("scolarite.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Prof (
            id INTEGER,
            nom TEXT,
            prenom TEXT,
            immatriculation INTEGER PRIMARY KEY,
            departement TEXT
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
        self.input_immatriculation = QLineEdit()
        self.input_immatriculation.setPlaceholderText("Numéro d'Immatriculation")
        self.input_departement = QComboBox()
        self.input_departement.addItems(["Biologie","Chimie","Géologie","Informatique","Mathématiques","Physique"])

        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.input_id)
        form_layout.addWidget(QLabel("Nom:"))
        form_layout.addWidget(self.input_nom)
        form_layout.addWidget(QLabel("Prénom:"))
        form_layout.addWidget(self.input_prenom)
        form_layout.addWidget(QLabel("Immatriculation:"))
        form_layout.addWidget(self.input_immatriculation)
        form_layout.addWidget(QLabel("Département:"))
        form_layout.addWidget(self.input_departement)
        layout_principal.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.bouton_ajouter = QPushButton("Ajouter")
        self.bouton_ajouter.setStyleSheet("background-color: #28a745; color: white;")
        self.bouton_ajouter.clicked.connect(self.ajouter_professeur)

        self.bouton_modifier = QPushButton("Modifier")
        self.bouton_modifier.setStyleSheet("background-color: #4165D5; color: white;")
        self.bouton_modifier.clicked.connect(self.modifier_professeur)

        self.bouton_supprimer = QPushButton("Supprimer")
        self.bouton_supprimer.setStyleSheet("background-color: #CC0000; color: white;")
        self.bouton_supprimer.clicked.connect(self.supprimer_professeur)

        button_layout.addWidget(self.bouton_ajouter)
        button_layout.addWidget(self.bouton_modifier)
        button_layout.addWidget(self.bouton_supprimer)
        layout_principal.addLayout(button_layout)

        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Chercher un professeur")
        self.search_bar.textChanged.connect(self.filtrer_tableau)
        search_layout.addWidget(QLabel("Recherche:"))
        search_layout.addWidget(self.search_bar)
        layout_principal.addLayout(search_layout)


        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Immatriculation", "Département"])
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
        self.cursor.execute("SELECT * FROM Prof")
        for row_data in self.cursor.fetchall():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))

    
    def filtrer_tableau(self):
        recherche = self.search_bar.text().strip().lower()
        self.table.setRowCount(0)
        query = "SELECT * FROM Prof WHERE id LIKE ? OR LOWER(nom) LIKE ? OR LOWER(prenom) LIKE ? OR immatriculation LIKE ? OR LOWER(departement) LIKE ?"
        valeurs = (f"%{recherche}%", f"%{recherche}%", f"%{recherche}%", f"%{recherche}%", f"%{recherche}%")
        self.cursor.execute(query, valeurs)
        for row_data in self.cursor.fetchall():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))


    def ajouter_professeur(self):
        professeur_id = self.input_id.text().strip()
        nom = self.input_nom.text().strip()
        prenom = self.input_prenom.text().strip()
        immatriculation = self.input_immatriculation.text().strip()
        departement = self.input_departement.currentText()

        if not professeur_id or not nom or not prenom or not immatriculation:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO Prof (id, nom, prenom, immatriculation, departement) VALUES (?, ?, ?, ?, ?)",
                (professeur_id, nom, prenom, immatriculation, departement))
            self.conn.commit()
            self.load_data()
            self.input_id.clear()
            self.input_nom.clear()
            self.input_prenom.clear()
            self.input_immatriculation.clear()
            self.input_departement.setCurrentIndex(0)

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'ajout : {e}")

    def modifier_professeur(self):
        index = self.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un professeur à modifier.")
            return

        professeur_id = self.input_id.text().strip()
        nom = self.input_nom.text().strip()
        prenom = self.input_prenom.text().strip()
        immatriculation = self.input_immatriculation.text().strip()
        departement = self.input_departement.currentText()

        if not professeur_id or not nom or not prenom or not immatriculation:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        self.cursor.execute(
            "UPDATE Prof SET id = ?, nom = ?, prenom = ?, departement = ? WHERE immatriculation = ?",
            (professeur_id, nom, prenom, departement, immatriculation))

        self.conn.commit()
        self.load_data()

    def supprimer_professeur(self):
        index = self.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un professeur à supprimer.")
            return

        immatriculation = self.table.item(index, 3).text()
        immatriculation1 = self.table.item(index, 0).text()
        self.cursor.execute("DELETE FROM Prof WHERE immatriculation = ?", (immatriculation,))
        self.cursor.execute("DELETE FROM Prof WHERE id = ?", (immatriculation1,))
        self.conn.commit()
        self.load_data()

    def remplir_champs(self, item):
        index = self.table.currentRow()
        self.input_id.setText(self.table.item(index, 0).text())
        self.input_nom.setText(self.table.item(index, 1).text())
        self.input_prenom.setText(self.table.item(index, 2).text())
        self.input_immatriculation.setText(self.table.item(index, 3).text())
        self.input_departement.setCurrentText(self.table.item(index, 4).text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = GestionProfesseurs()
    main_win.show()
    sys.exit(app.exec_())
