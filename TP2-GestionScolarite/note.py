import sys
import sqlite3
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QMessageBox, QHeaderView)


class GestionNotes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Notes")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #f8f9fa; color: #333333;")
        self.setWindowIcon(QIcon("Icons/iconNote.png"))
        self.initDB()
        self.initUI()
        self.load_data()

    def initDB(self):
        self.conn = sqlite3.connect("scolarite.db")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Note (
                id INTEGER PRIMARY KEY,
                etudiant_num_apogee INTEGER,
                module_id INTEGER,
                note REAL,
                FOREIGN KEY (etudiant_num_apogee) REFERENCES Etudiant(num_apogee),
                FOREIGN KEY (module_id) REFERENCES Module(module_id)
                
            )
        ''')
        self.conn.commit()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout_principal = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID de la Note")
        self.input_etudiant_apogee = QLineEdit()
        self.input_etudiant_apogee.setPlaceholderText("Numéro Apogée Étudiant")
        self.input_module_id = QLineEdit()
        self.input_module_id.setPlaceholderText("ID du Module")
        self.input_note = QLineEdit()
        self.input_note.setPlaceholderText("Note (0 - 20)")

        form_layout.addWidget(QLabel("ID Note:"))
        form_layout.addWidget(self.input_id)
        form_layout.addWidget(QLabel("Numéro Apogée Étudiant:"))
        form_layout.addWidget(self.input_etudiant_apogee)
        form_layout.addWidget(QLabel("ID du Module:"))
        form_layout.addWidget(self.input_module_id)
        form_layout.addWidget(QLabel("Note:"))
        form_layout.addWidget(self.input_note)
        layout_principal.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.bouton_ajouter = QPushButton("Ajouter")
        self.bouton_ajouter.setStyleSheet("background-color: #28a745; color: white;")
        self.bouton_ajouter.clicked.connect(self.ajouter_note)

        self.bouton_modifier = QPushButton("Modifier")
        self.bouton_modifier.setStyleSheet("background-color: #007bff; color: white;")
        self.bouton_modifier.clicked.connect(self.modifier_note)

        self.bouton_supprimer = QPushButton("Supprimer")
        self.bouton_supprimer.setStyleSheet("background-color: #dc3545; color: white;")
        self.bouton_supprimer.clicked.connect(self.supprimer_note)

        button_layout.addWidget(self.bouton_ajouter)
        button_layout.addWidget(self.bouton_modifier)
        button_layout.addWidget(self.bouton_supprimer)
        layout_principal.addLayout(button_layout)

        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Chercher une note")
        self.search_bar.textChanged.connect(self.filtrer_tableau)
        search_layout.addWidget(QLabel("Recherche:"))
        search_layout.addWidget(self.search_bar)
        layout_principal.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Numéro Apogée", "ID Module", "Note"])
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
        self.cursor.execute("SELECT * FROM Note")
        for row_data in self.cursor.fetchall():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))


    def filtrer_tableau(self):
        recherche = self.search_bar.text().strip().lower()
        self.table.setRowCount(0)
        query = "SELECT * FROM Note WHERE id LIKE ? OR etudiant_num_apogee LIKE ? OR module_id LIKE ? OR note LIKE ?"
        valeurs = (f"%{recherche}%", f"%{recherche}%", f"%{recherche}%", f"%{recherche}%", f"%{recherche}%")
        self.cursor.execute(query, valeurs)
        for row_data in self.cursor.fetchall():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))

    def ajouter_note(self):
        note_id = self.input_id.text().strip()
        etudiant_apogee = self.input_etudiant_apogee.text().strip()
        module_id = self.input_module_id.text().strip()
        note = self.input_note.text().strip()

        if not note_id or not etudiant_apogee or not module_id or not note:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            note = float(note)
            if note < 0 or note > 20:
                raise ValueError("La note doit être entre 0 et 20.")

            # Vérifier si une entrée avec le même etudiant_apogee et module_id existe déjà
            self.cursor.execute(
                "SELECT COUNT(*) FROM Note WHERE etudiant_num_apogee = ? AND module_id = ?",
                (etudiant_apogee, module_id)
            )
            if self.cursor.fetchone()[0] > 0:
                QMessageBox.critical(self, "Erreur", "Une note avec ce numéro Apogée et cet ID de module existe déjà.")
                return

            # Insérer la note si aucune duplication n'est trouvée
            self.cursor.execute(
                "INSERT INTO Note (id, etudiant_num_apogee, module_id, note) VALUES (?, ?, ?, ?)",
                (note_id, etudiant_apogee, module_id, note)
            )
            self.conn.commit()

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(note_id))
            self.table.setItem(row_position, 1, QTableWidgetItem(etudiant_apogee))
            self.table.setItem(row_position, 2, QTableWidgetItem(module_id))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(note)))

            self.input_id.clear()
            self.input_etudiant_apogee.clear()
            self.input_module_id.clear()
            self.input_note.clear()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'ajout : {e}")
        except ValueError as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def modifier_note(self):
        index = self.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une note à modifier.")
            return

        note_id = self.table.item(index, 0).text()
        etudiant_apogee = self.input_etudiant_apogee.text().strip()
        module_id = self.input_module_id.text().strip()
        note = self.input_note.text().strip()

        if not etudiant_apogee or not module_id or not note:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            note = float(note)
            if note < 0 or note > 20:
                raise ValueError("La note doit être entre 0 et 20.")

            self.cursor.execute(
                "UPDATE Note SET etudiant_num_apogee = ?, module_id = ?, note = ? WHERE id = ?",
                (etudiant_apogee, module_id, note, note_id))
            self.conn.commit()
            self.table.setItem(index, 1, QTableWidgetItem(etudiant_apogee))
            self.table.setItem(index, 2, QTableWidgetItem(module_id))
            self.table.setItem(index, 3, QTableWidgetItem(str(note)))

            QMessageBox.information(self, "Succès", "La note a été modifié avec succès.")

        except ValueError as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def supprimer_note(self):
        index = self.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une note à supprimer.")
            return

        note_id = self.table.item(index, 0).text()
        self.cursor.execute("DELETE FROM Note WHERE id = ?", (note_id,))
        self.conn.commit()
        self.table.removeRow(index)

        QMessageBox.information(self, "Succès", "La note a été supprimé avec succès.")

    def remplir_champs(self, item):
        index = self.table.currentRow()
        self.input_id.setText(self.table.item(index, 0).text())
        self.input_etudiant_apogee.setText(self.table.item(index, 1).text())
        self.input_module_id.setText(self.table.item(index, 2).text())
        self.input_note.setText(self.table.item(index, 3).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = GestionNotes()
    main_win.show()
    sys.exit(app.exec_())
