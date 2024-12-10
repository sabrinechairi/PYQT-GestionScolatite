import sys
import subprocess
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QVBoxLayout, QWidget, QLabel, QPushButton


class FenetreMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion de Scolarité")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("color: #333333;")
        self.setWindowIcon(QIcon("Icons/iconUni.png"))

        self.toolbar = self.addToolBar("Menu")

        self.action_accueil = QAction("Accueil", self)
        self.action_etudiant = QAction("Gérer les Étudiants", self)
        self.action_professeur = QAction("Gérer les Professeurs", self)
        self.action_module = QAction("Gérer les Modules", self)
        self.action_note = QAction("Gérer les Notes", self)

        self.toolbar.addAction(self.action_accueil)
        self.toolbar.addAction(self.action_etudiant)
        self.toolbar.addAction(self.action_professeur)
        self.toolbar.addAction(self.action_module)
        self.toolbar.addAction(self.action_note)

        self.action_accueil.triggered.connect(self.afficher_accueil)
        self.action_etudiant.triggered.connect(self.afficher_etudiant)
        self.action_professeur.triggered.connect(self.afficher_professeur)
        self.action_module.triggered.connect(self.afficher_module)
        self.action_note.triggered.connect(self.afficher_note)

        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #4165D5; /* Couleur de fond */
                color: white; /* Couleur du texte */
                font-size: 16px; /* Taille de police */
                border: 1px solid #333; /* Bordure */
            }
            QToolButton {
                background-color: #4165D5; /* Fond des boutons */
                color: white; /* Couleur du texte */
                padding: 5px; /* Espacement */
                border-radius: 5px; /* Coins arrondis */
            }
            QToolButton:hover {
                background-color: #4165D5; /* Couleur au survol */
            }
        """)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout_principal = QVBoxLayout(self.central_widget)

        self.label_contenu = QLabel("Bienvenue dans l'application Gestion de Scolarité", self)
        self.label_contenu.setStyleSheet("font-size: 15px; color: #cc0000; padding: 10px;")
        self.layout_principal.addWidget(self.label_contenu)
        self.layout_principal.addStretch() 

    def paintEvent(self, event):
        """Ajoute une image de fond redimensionnée à la fenêtre."""
        painter = QPainter(self)
        pixmap = QPixmap("Icons/GS.jpg") 
        if not pixmap.isNull():
            painter.drawPixmap(self.rect(), pixmap)  
        else:
            print("Erreur : Impossible de charger l'image de fond.")

    def afficher_accueil(self):
        subprocess.Popen(["python", "main.py"])

    def afficher_professeur(self):
        subprocess.Popen(["python", "professeur.py"])

    def afficher_etudiant(self):
        subprocess.Popen(["python", "etudiant.py"])

    def afficher_module(self):
        subprocess.Popen(["python", "module.py"])

    def afficher_note(self):
        subprocess.Popen(["python", "note.py"])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FenetreMenu()
    window.show()
    sys.exit(app.exec_())
