import sys
from math import ceil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QSpinBox, QVBoxLayout, QHBoxLayout, QScrollArea, QTabWidget,
    QSplitter, QGraphicsOpacityEffect, QFormLayout, QLineEdit
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QPropertyAnimation, QEasingCurve, QSize, QTimer
from PyQt5.QtGui import QFont, QPixmap, QMovie


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NIZUASHOP Interface")
        self.resize(1000, 700)

        # --- État global ---
        self.dark_mode = True
        self.lobby_widgets = []        # liste des QWebEngineView du lobby
        self.remaining_loads = 0       # compteur de chargements restants

        # --- Onglets en haut : Menu / Lobby / Settings ---
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.setCentralWidget(self.tabs)

        # --- Onglet Menu ---
        self.menu_tab = QWidget()
        self._build_menu_tab()
        self.tabs.addTab(self.menu_tab, "Menu")

        # --- Onglet Lobby (initialement vide, on désactive) ---
        self.lobby_tab = QWidget()
        self.tabs.addTab(self.lobby_tab, "Lobby")
        self.tabs.setTabEnabled(1, False)

        # --- Onglet Settings (exemple) ---
        self.settings_tab = QWidget()
        self._build_settings_tab()
        self.tabs.addTab(self.settings_tab, "Settings")

        # Appliquer le style initial (mode Nuit)
        self.apply_stylesheet()

    # ------------------------------
    # Construction de l’onglet Menu
    # ------------------------------
    def _build_menu_tab(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(20)

        # → Logo + Titre “NIZUASHOP”
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        logo = QLabel()
        pixmap = QPixmap("nizua_logo.png")
        logo.setPixmap(
            pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        logo.setStyleSheet("margin-right: 10px;")
        title = QLabel("NIZUASHOP")
        title.setFont(QFont("Orbitron", 32, QFont.Bold))
        title.setObjectName("titleLabel")
        logo_layout.addWidget(logo)
        logo_layout.addWidget(title)
        layout.addLayout(logo_layout)

        # → Choix du nombre de tabs (1 à 20)
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)
        lbl = QLabel("Nombre de tabs :")
        lbl.setObjectName("plainLabel")
        spin = QSpinBox()
        spin.setRange(1, 20)
        spin.setValue(3)
        spin.setFixedWidth(60)
        spin.setObjectName("spinBox")
        self.spinbox = spin
        hbox.addWidget(lbl)
        hbox.addWidget(spin)
        layout.addLayout(hbox)

        # → Bouton “Open Lobby” animé
        btn_open = QPushButton("🚀 Open Lobby")
        btn_open.setFixedSize(220, 50)
        btn_open.setObjectName("neonButton")
        btn_open.clicked.connect(self.animate_and_open_lobby)
        layout.addWidget(btn_open, alignment=Qt.AlignCenter)

        # → Toggle Jour / Nuit
        btn_toggle = QPushButton("🌗 Mode Jour")
        btn_toggle.setFixedSize(140, 40)
        btn_toggle.setObjectName("toggleButton")
        btn_toggle.clicked.connect(self.toggle_day_night)
        self.btn_toggle = btn_toggle
        layout.addWidget(btn_toggle, alignment=Qt.AlignCenter)

        self.menu_tab.setLayout(layout)

    # --------------------------------
    # Animation puis ouverture Lobby
    # --------------------------------
    def animate_and_open_lobby(self):
        btn = self.sender()
        effect = QGraphicsOpacityEffect(btn)
        btn.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(400)
        anim.setStartValue(1.0)
        anim.setEndValue(0.4)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.finished.connect(lambda: (effect.setOpacity(1.0), self.open_lobby()))
        anim.start()

    # ------------------------------
    # Bascule Jour / Nuit
    # ------------------------------
    def toggle_day_night(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.btn_toggle.setText("🌗 Mode Jour")
        else:
            self.btn_toggle.setText("🌙 Mode Nuit")
        self.apply_stylesheet()

    def apply_stylesheet(self):
        if self.dark_mode:
            self.setStyleSheet(self.dark_stylesheet())
        else:
            self.setStyleSheet(self.light_stylesheet())

    # --------------------------------
    # Création / rafraîchissement Lobby
    # --------------------------------
    def open_lobby(self):
        count = self.spinbox.value()
        url = "https://www.xbox.com/en-US/play/launch/call-of-duty-black-ops-6---cross-gen-bundle/9PF528M6CRHQ"

        # Réinitialiser si on avait déjà un lobby
        self.lobby_widgets.clear()
        self.remaining_loads = count

        # --- Construction de l’onglet Lobby ---
        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        container.setLayout(main_layout)

        # 1) Overlay Loader animé
        loader_overlay = QWidget(container)
        loader_overlay.setObjectName("loaderOverlay")
        loader_overlay.setGeometry(0, 0, self.width(), self.height())
        loader_overlay.setAttribute(Qt.WA_StyledBackground, True)

        loader_label = QLabel(loader_overlay)
        loader_label.setObjectName("loaderLabel")
        loader_label.setAlignment(Qt.AlignCenter)
        movie = QMovie("loader.gif")
        loader_label.setMovie(movie)
        movie.start()
        loader_label.setFixedSize(200, 200)
        loader_label.move(
            (self.width() - loader_label.width()) // 2,
            (self.height() - loader_label.height()) // 2,
        )

        # 2) Grille de QSplitter redimensionnables
        cols = min(count, 5)
        rows = ceil(count / cols)
        root_splitter = QSplitter(Qt.Vertical)
        root_splitter.setHandleWidth(5)

        idx = 0
        for r in range(rows):
            row_splitter = QSplitter(Qt.Horizontal)
            row_splitter.setHandleWidth(5)
            this_row = min(cols, count - idx)
            for c in range(this_row):
                browser = QWebEngineView()
                browser.setUrl(QUrl(url))
                browser.setMinimumSize(QSize(200, 112))  # ratio 16:9 mini
                browser.loadFinished.connect(lambda ok, ov=loader_overlay: self.on_tab_loaded(ov))
                self.lobby_widgets.append(browser)
                row_splitter.addWidget(browser)
                idx += 1

            # Si moins de 5 colonnes, ajouter des "spacers" transparents
            if this_row < cols:
                for _ in range(cols - this_row):
                    spacer = QWidget()
                    spacer.setStyleSheet("background: transparent;")
                    row_splitter.addWidget(spacer)

            root_splitter.addWidget(row_splitter)

        # Ajouter le splitter dans un QScrollArea (scroll si > hauteur)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(root_splitter)
        main_layout.addWidget(scroll)

        # 3) Bouton “Retour au menu”
        btn_back = QPushButton("🔙 Retour au menu")
        btn_back.setFixedSize(180, 45)
        btn_back.setObjectName("backButton")
        btn_back.clicked.connect(self.go_back_to_menu)
        main_layout.addWidget(btn_back, alignment=Qt.AlignHCenter | Qt.AlignBottom)

        # Remplacer l’onglet Lobby
        self.tabs.removeTab(1)
        self.lobby_tab = container
        self.tabs.insertTab(1, self.lobby_tab, "Lobby")
        self.tabs.setTabEnabled(1, True)
        self.tabs.setCurrentIndex(1)

        # Replacer l’overlay Loader au-dessus, après que tout ait été layouté
        QTimer.singleShot(100, lambda: loader_overlay.raise_())

    # --------------------------------
    # Callback quand chaque tab est chargée
    # --------------------------------
    def on_tab_loaded(self, overlay: QWidget):
        self.remaining_loads -= 1
        if self.remaining_loads <= 0:
            # Tous les onglets ont fini de charger → on fait disparaître le loader
            anim = QPropertyAnimation(overlay, b"windowOpacity", self)
            anim.setDuration(500)
            anim.setStartValue(1.0)
            anim.setEndValue(0.0)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            anim.finished.connect(overlay.hide)
            anim.start()

    # ----------------------------
    # Retour au Menu depuis Lobby
    # ----------------------------
    def go_back_to_menu(self):
        # Désactiver l’onglet Lobby et revenir à Menu
        self.tabs.setCurrentIndex(0)
        self.tabs.setTabEnabled(1, False)
        # On pourra remplacer complètement l’onglet Lobby à la prochaine ouverture

    # --------------------------------
    # Contenu de l’onglet Settings
    # --------------------------------
    def _build_settings_tab(self):
        layout = QFormLayout()
        layout.setSpacing(20)
        lbl_theme = QLabel("Thème personnalisé :")
        line_theme = QLineEdit("#ff0040")
        layout.addRow(lbl_theme, line_theme)

        lbl_info = QLabel(
            "Ici, vous pouvez ajouter vos paramètres.\n"
            "Exemple : config d’URL, clés API, etc."
        )
        lbl_info.setWordWrap(True)
        layout.addRow(lbl_info)
        self.settings_tab.setLayout(layout)

    # --------------------------------
    # Stylesheet Mode Nuit (futuriste)
    # --------------------------------
    def dark_stylesheet(self):
        return """
        QWidget {
            background-color: #0d0d0d;
            color: #e0e0e0;
            font-family: 'Segoe UI', sans-serif;
        }
        QLabel#titleLabel {
            color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #ff0040, stop:0.5 #aa00ff, stop:1 #0040ff
            );
        }
        QLabel#plainLabel {
            color: #cccccc;
            font-size: 16px;
        }
        QSpinBox#spinBox {
            background-color: #1a1a1a;
            color: #f0f0f0;
            border: 2px solid #6f00ff;
            border-radius: 5px;
            padding: 4px;
        }
        QSpinBox#spinBox::up-button, QSpinBox#spinBox::down-button {
            width: 16px; height: 16px;
        }
        QPushButton#neonButton {
            background-color: #6f00ff;
            color: white;
            font-size: 16px;
            border: 2px solid #ff0040;
            border-radius: 8px;
            padding: 8px;
        }
        QPushButton#neonButton:hover {
            background-color: #ff0040;
            border: 2px solid #aa00ff;
        }
        QPushButton#neonButton:pressed {
            background-color: #aa00ff;
            border: 2px solid #0040ff;
        }
        QPushButton#toggleButton {
            background-color: #222222;
            color: #ffcc00;
            font-size: 14px;
            border: 1px solid #ffcc00;
            border-radius: 6px;
            padding: 6px;
        }
        QPushButton#toggleButton:hover {
            background-color: #333333;
        }
        QPushButton#backButton {
            background-color: #880808;
            color: white;
            font-size: 14px;
            border: 2px solid #ff0040;
            border-radius: 6px;
            padding: 6px;
        }
        QPushButton#backButton:hover {
            background-color: #aa0000;
        }
        QWidget#loaderOverlay {
            background-color: rgba(10, 10, 10, 0.85);
        }
        QLabel#loaderLabel {
            border: none;
        }
        """

    # --------------------------------
    # Stylesheet Mode Jour (futuriste clair)
    # --------------------------------
    def light_stylesheet(self):
        return """
        QWidget {
            background-color: #f2f2f2;
            color: #202020;
            font-family: 'Segoe UI', sans-serif;
        }
        QLabel#titleLabel {
            color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #ff0040, stop:0.5 #aa00ff, stop:1 #0040ff
            );
        }
        QLabel#plainLabel {
            color: #202020;
            font-size: 16px;
        }
        QSpinBox#spinBox {
            background-color: #ffffff;
            color: #202020;
            border: 2px solid #0040ff;
            border-radius: 5px;
            padding: 4px;
        }
        QSpinBox#spinBox::up-button, QSpinBox#spinBox::down-button {
            width: 16px; height: 16px;
        }
        QPushButton#neonButton {
            background-color: #aa00ff;
            color: white;
            font-size: 16px;
            border: 2px solid #0040ff;
            border-radius: 8px;
            padding: 8px;
        }
        QPushButton#neonButton:hover {
            background-color: #0040ff;
            border: 2px solid #ff0040;
        }
        QPushButton#neonButton:pressed {
            background-color: #ff0040;
            border: 2px solid #aa00ff;
        }
        QPushButton#toggleButton {
            background-color: #dddddd;
            color: #aa00ff;
            font-size: 14px;
            border: 1px solid #aa00ff;
            border-radius: 6px;
            padding: 6px;
        }
        QPushButton#toggleButton:hover {
            background-color: #cccccc;
        }
        QPushButton#backButton {
            background-color: #ff3366;
            color: white;
            font-size: 14px;
            border: 2px solid #aa00ff;
            border-radius: 6px;
            padding: 6px;
        }
        QPushButton#backButton:hover {
            background-color: #ff5588;
        }
        QWidget#loaderOverlay {
            background-color: rgba(255, 255, 255, 0.85);
        }
        QLabel#loaderLabel {
            border: none;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
