# ui/main_window.py

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QTextEdit, QPushButton, QLabel, QMessageBox
)
from core.plugins import discover_plugins, reload_plugins, get_plugin_by_name

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Hacker — Advanced Plugin Platform")
        self.resize(900, 700)

        # Layout
        main_layout = QVBoxLayout()

        # --- Top Row: Mode Selector & Plugin Selector ---
        top_row = QHBoxLayout()
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Hacker Mode", "IT Fix Mode"])
        top_row.addWidget(QLabel("Agent Mode:"))
        top_row.addWidget(self.mode_selector)

        self.plugin_selector = QComboBox()
        self.plugins = discover_plugins()
        self.update_plugin_selector()
        top_row.addWidget(QLabel("Plugin:"))
        top_row.addWidget(self.plugin_selector)

        # Reload Plugins Button
        self.reload_button = QPushButton("Reload Plugins")
        self.reload_button.clicked.connect(self.reload_plugins)
        top_row.addWidget(self.reload_button)

        main_layout.addLayout(top_row)

        # --- Chat/Console Display ---
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        main_layout.addWidget(self.chat_display)

        # --- User Input ---
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("Type your command or plugin arguments here...")
        main_layout.addWidget(self.input_area)

        # --- Action Buttons ---
        action_row = QHBoxLayout()
        self.send_button = QPushButton("Send to AI")
        self.send_button.clicked.connect(self.on_send)
        action_row.addWidget(self.send_button)

        self.run_plugin_button = QPushButton("Run Plugin")
        self.run_plugin_button.clicked.connect(self.run_plugin)
        action_row.addWidget(self.run_plugin_button)

        main_layout.addLayout(action_row)

        # Central Widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def update_plugin_selector(self):
        """Refreshes the plugin selector with the latest discovered plugins."""
        self.plugin_selector.clear()
        self.plugins = discover_plugins()
        for plugin in self.plugins:
            self.plugin_selector.addItem(plugin.name)

    def reload_plugins(self):
        """Explicitly reload all plugins (e.g., after creating new ones)."""
        reload_plugins()
        self.update_plugin_selector()
        QMessageBox.information(self, "Plugins Reloaded", "Plugin list refreshed!")

    def on_send(self):
        """Handles sending user input to the AI agent (placeholder, expand as needed)."""
        user_input = self.input_area.toPlainText().strip()
        mode = self.mode_selector.currentText()
        if not user_input:
            return
        self.chat_display.append(f"<b>You ({mode}):</b> {user_input}")
        # TODO: Connect to your AI backend and display response
        ai_reply = "(AI agent response here)"
        self.chat_display.append(f"<b>AI:</b> {ai_reply}")
        self.input_area.clear()

    def run_plugin(self):
        """Runs the selected plugin with arguments from input area."""
        plugin_name = self.plugin_selector.currentText()
        plugin = get_plugin_by_name(plugin_name)
        if not plugin:
            QMessageBox.critical(self, "Plugin Not Found", f"Could not load plugin: {plugin_name}")
            return
        # Parse arguments from input_area (supports key=value pairs, one per line)
        raw_args = self.input_area.toPlainText().strip()
        kwargs = {}
        for line in raw_args.splitlines():
            if "=" in line:
                key, val = line.split("=", 1)
                kwargs[key.strip()] = val.strip()
        try:
            result = plugin.run(**kwargs)
            self.chat_display.append(f"<b>Plugin [{plugin.name}] output:</b>\n{result}")
        except Exception as e:
            self.chat_display.append(f"<b>[ERROR]</b> {e}")

# Entrypoint for launching the GUI app directly
def launch_main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    launch_main_window()
