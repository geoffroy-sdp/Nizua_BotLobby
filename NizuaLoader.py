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
from gamepad_control import GamepadController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NIZUASHOP Interface with Gamepad")
        self.resize(1000, 800)

        self.dark_mode = True
        self.controllers = []
        self.controller_connected = False
        self.browser_urls = []
        self.launch_url = "https://www.xbox.com/en-US/play/launch/call-of-duty-black-ops-6---cross-gen-bundle/9PF528M6CRHQ"

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.menu_tab = QWidget()
        self._build_menu_tab()
        self.tabs.addTab(self.menu_tab, "Menu")

        self.lobby_tab = QWidget()
        self.tabs.addTab(self.lobby_tab, "Lobby")
        self.tabs.setTabEnabled(1, False)

        self.settings_tab = QWidget()
        self._build_settings_tab()
        self.tabs.addTab(self.settings_tab, "Settings")

        self.apply_stylesheet()

    def _build_menu_tab(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(15)

        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        logo = QLabel()
        pixmap = QPixmap("nizua_logo.png")
        logo.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setStyleSheet("margin-right: 10px;")
        title = QLabel("NIZUASHOP")
        title.setFont(QFont("Orbitron", 32, QFont.Bold))
        title.setObjectName("titleLabel")
        logo_layout.addWidget(logo)
        logo_layout.addWidget(title)
        layout.addLayout(logo_layout)

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

        btn_open = QPushButton("📂 Ouvrir Lobby")
        btn_open.setFixedSize(220, 50)
        btn_open.setObjectName("neonButton")
        btn_open.clicked.connect(self.open_lobby)
        layout.addWidget(btn_open, alignment=Qt.AlignCenter)

        btn_launch = QPushButton("🚀 Launch BO6")
        btn_launch.setFixedSize(220, 50)
        btn_launch.setObjectName("neonButton")
        btn_launch.clicked.connect(self.launch_bo6)
        layout.addWidget(btn_launch, alignment=Qt.AlignCenter)

        btn_connect = QPushButton("🎮 Connect Controllers")
        btn_connect.setFixedSize(220, 50)
        btn_connect.setObjectName("neonButton")
        btn_connect.clicked.connect(self.connect_controller)
        self.btn_connect = btn_connect
        layout.addWidget(btn_connect, alignment=Qt.AlignCenter)

        btn_movement = QPushButton("🕹️ Enable Mouvement")
        btn_movement.setFixedSize(220, 50)
        btn_movement.setObjectName("neonButton")
        btn_movement.clicked.connect(self.toggle_movement)
        self.btn_movement = btn_movement
        layout.addWidget(btn_movement, alignment=Qt.AlignCenter)

        btn_antiafk = QPushButton("⏱️ Anti-AFK")
        btn_antiafk.setFixedSize(220, 50)
        btn_antiafk.setObjectName("neonButton")
        btn_antiafk.clicked.connect(self.toggle_anti_afk)
        self.btn_antiafk = btn_antiafk
        layout.addWidget(btn_antiafk, alignment=Qt.AlignCenter)

        btn_class = QPushButton("🔧 Select Class")
        btn_class.setFixedSize(220, 50)
        btn_class.setObjectName("neonButton")
        btn_class.clicked.connect(self.select_class)
        self.btn_class = btn_class
        layout.addWidget(btn_class, alignment=Qt.AlignCenter)

        btn_toggle = QPushButton("🌗 Mode Jour")
        btn_toggle.setFixedSize(140, 40)
        btn_toggle.setObjectName("toggleButton")
        btn_toggle.clicked.connect(self.toggle_day_night)
        self.btn_toggle = btn_toggle
        layout.addWidget(btn_toggle, alignment=Qt.AlignCenter)

        self.menu_tab.setLayout(layout)

    def connect_controller(self):
        self.controllers.clear()
        count = self.spinbox.value()

        for i in range(count):
            ctrl = GamepadController()
            if ctrl.connect():
                ctrl.start()
                self.controllers.append(ctrl)
            else:
                print(f"❌ Gamepad {i+1} failed to connect")

        self.controller_connected = bool(self.controllers)
        self.btn_connect.setText(f"✅ {len(self.controllers)} Controller(s) Ready" if self.controller_connected else "❌ Connection Failed")

    def toggle_movement(self):
        if not self.controller_connected:
            self.btn_movement.setText("⚠️ Connect First")
            return
        enabled = not self.controllers[0].movement_enabled
        for ctrl in self.controllers:
            ctrl.movement_enabled = enabled
        self.btn_movement.setText("🚫 Disable Mouvement" if enabled else "🕹️ Enable Mouvement")

    def toggle_anti_afk(self):
        if not self.controller_connected:
            self.btn_antiafk.setText("⚠️ Connect First")
            return
        enabled = not self.controllers[0].anti_afk_enabled
        for ctrl in self.controllers:
            if enabled:
                ctrl.toggle_anti_afk()
            else:
                ctrl.anti_afk_enabled = False
        self.btn_antiafk.setText("🚫 Disable Anti-AFK" if enabled else "⏱️ Anti-AFK")

    def select_class(self):
        if not self.controller_connected:
            self.btn_class.setText("⚠️ Connect First")
            return
        for ctrl in self.controllers:
            ctrl.select_class()
        self.btn_class.setText("✅ Class Selected")

    def launch_bo6(self):
        for browser in self.browser_urls:
            browser.setUrl(QUrl(self.launch_url))

    def open_lobby(self):
        count = self.spinbox.value()
        initial_url = "https://www.xbox.com/en-US/play/launch/call-of-duty-black-ops-6---cross-gen-bundle/"
        self.browser_urls = []

        container = QWidget()
        main_layout = QVBoxLayout()
        container.setLayout(main_layout)

        cols = min(count, 5)
        rows = ceil(count / cols)
        root_splitter = QSplitter(Qt.Vertical)
        root_splitter.setHandleWidth(5)

        idx = 0
        for r in range(rows):
            row_splitter = QSplitter(Qt.Horizontal)
            row_splitter.setHandleWidth(5)
            this_row = min(cols, count - idx)
            for _ in range(this_row):
                browser = QWebEngineView()
                browser.setFixedSize(QSize(640, 360))
                browser.setUrl(QUrl(initial_url))
                self.browser_urls.append(browser)
                row_splitter.addWidget(browser)
                idx += 1
            root_splitter.addWidget(row_splitter)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(root_splitter)
        main_layout.addWidget(scroll)

        btn_back = QPushButton("🔙 Retour au menu")
        btn_back.setFixedSize(180, 45)
        btn_back.setObjectName("backButton")
        btn_back.clicked.connect(self.go_back_to_menu)
        main_layout.addWidget(btn_back, alignment=Qt.AlignHCenter)

        self.tabs.removeTab(1)
        self.lobby_tab = container
        self.tabs.insertTab(1, self.lobby_tab, "Lobby")
        self.tabs.setTabEnabled(1, True)
        self.tabs.setCurrentIndex(1)

    def go_back_to_menu(self):
        self.tabs.setCurrentIndex(0)
        self.tabs.setTabEnabled(1, False)

    def toggle_day_night(self):
        self.dark_mode = not self.dark_mode
        self.btn_toggle.setText("🌗 Mode Jour" if self.dark_mode else "🌙 Mode Nuit")
        self.apply_stylesheet()

    def apply_stylesheet(self):
        if self.dark_mode:
            self.setStyleSheet(self.dark_stylesheet())
        else:
            self.setStyleSheet(self.light_stylesheet())

    def _build_settings_tab(self):
        layout = QFormLayout()
        layout.setSpacing(20)
        lbl_theme = QLabel("Thème personnalisé :")
        line_theme = QLineEdit("#ff0040")
        layout.addRow(lbl_theme, line_theme)
        lbl_info = QLabel("Ajouter vos paramètres ici (API, URL, etc.)")
        lbl_info.setWordWrap(True)
        layout.addRow(lbl_info)
        self.settings_tab.setLayout(layout)

    def dark_stylesheet(self):
        return """
        QWidget { background-color: #0d0d0d; color: #e0e0e0; font-family: 'Segoe UI'; }
        QLabel#titleLabel {
            color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #ff0040, stop:0.5 #aa00ff, stop:1 #0040ff); }
        QPushButton#neonButton {
            background-color: #6f00ff; color: white;
            font-size: 16px; border: 2px solid #ff0040;
            border-radius: 8px; padding: 8px; }
        QPushButton#neonButton:hover { background-color: #ff0040; }
        QPushButton#backButton {
            background-color: #880808; color: white;
            border: 2px solid #ff0040; border-radius: 6px; padding: 6px; }
        QPushButton#backButton:hover { background-color: #aa0000; }
        """

    def light_stylesheet(self):
        return """
        QWidget { background-color: #f2f2f2; color: #202020; font-family: 'Segoe UI'; }
        QLabel#titleLabel {
            color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #ff0040, stop:0.5 #aa00ff, stop:1 #0040ff); }
        QPushButton#neonButton {
            background-color: #aa00ff; color: white;
            font-size: 16px; border: 2px solid #0040ff;
            border-radius: 8px; padding: 8px; }
        QPushButton#neonButton:hover { background-color: #0040ff; }
        QPushButton#backButton {
            background-color: #ff3366; color: white;
            border: 2px solid #aa00ff; border-radius: 6px; padding: 6px; }
        QPushButton#backButton:hover { background-color: #ff5588; }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
