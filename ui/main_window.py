import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QTextEdit, QPushButton, QLabel, QMessageBox
)
from core.ai import ask_ai
from core.plugins import discover_plugins

def launch_main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("M.A.B.E.L — AI Red/Blue Team Assistant")
        self.resize(900, 700)

        main_layout = QVBoxLayout()
        controls_layout = QHBoxLayout()
        plugin_layout = QHBoxLayout()

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Hacker Mode", "IT Fix Mode"])
        controls_layout.addWidget(QLabel("Agent Mode:"))
        controls_layout.addWidget(self.mode_selector)

        self.plugin_selector = QComboBox()
        self.reload_plugins()
        controls_layout.addWidget(QLabel("Plugin:"))
        controls_layout.addWidget(self.plugin_selector)
        self.reload_btn = QPushButton("Reload Plugins")
        self.reload_btn.clicked.connect(self.reload_plugins)
        controls_layout.addWidget(self.reload_btn)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("Type your command or plugin arguments here...")

        self.send_button = QPushButton("Send to AI")
        self.send_button.clicked.connect(self.on_send)

        self.run_plugin_btn = QPushButton("Run Plugin")
        self.run_plugin_btn.clicked.connect(self.on_run_plugin)

        plugin_layout.addWidget(self.send_button)
        plugin_layout.addWidget(self.run_plugin_btn)

        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.chat_display)
        main_layout.addWidget(self.input_area)
        main_layout.addLayout(plugin_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def reload_plugins(self):
        self.plugins = discover_plugins()
        self.plugin_selector.clear()
        for plugin in self.plugins:
            self.plugin_selector.addItem(plugin.name)

    def on_send(self):
        user_input = self.input_area.toPlainText().strip()
        if not user_input:
            return
        mode = self.mode_selector.currentText()
        self.chat_display.append(f"\n<b>You ({mode}):</b> {user_input}")
        self.chat_display.append("<i>AI: ...thinking...</i>")
        ai_reply = ask_ai(user_input, mode)
        self.chat_display.append(f"<b>AI:</b> {ai_reply}")
        self.input_area.clear()

    def on_run_plugin(self):
        idx = self.plugin_selector.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, "Plugin", "Select a plugin first.")
            return
        plugin = self.plugins[idx]
        args_text = self.input_area.toPlainText().strip()
        args = {}
        if args_text:
            for kv in args_text.split():
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    args[k.strip()] = v.strip()
        output = plugin.run(**args)
        self.chat_display.append(f"\n<b>Plugin [{plugin.name}] output:</b> {output}")
        self.input_area.clear()
    def on_run_plugin(self):
        idx = self.plugin_selector.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, "Plugin", "Select a plugin first.")
            return
        plugin = self.plugins[idx]
        args_text = self.input_area.toPlainText().strip()
        args = {}
        if args_text:
            # Parse arguments, handling quoted values
            for item in re.findall(r'(\w+=(?:\"[^\"]*\"|\'[^\']*\'|\S+))', args_text):
                key, value = item.split('=', 1)
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                args[key] = value
        
        self.chat_display.append(f"\n<b>Running Plugin:</b> {plugin.name} with args: {args}")
        try:
            output = plugin.run(**args)
            self.chat_display.append(f"<b>Plugin [{plugin.name}] output:</b> {output}")
        except Exception as e:
            self.chat_display.append(f"<b style='color:red;'>Plugin [{plugin.name}] error:</b> {e}")
        self.input_area.clear()
