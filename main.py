from ui.main_window import launch_main_window
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QTextEdit, QPushButton, QLabel, QMessageBox,
)
from core.ai import ask_ai
from core.plugins import discover_plugins
import re
from core.memory import memory
from datetime import datetime

if __name__ == "__main__":
    launch_main_window()

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

        self.history_button = QPushButton("View History")
        self.history_button.clicked.connect(self.view_history)
        controls_layout.addWidget(self.history_button)

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
        
        # Log user input
        memory.log({"type": "user_input", "mode": mode, "input": user_input})

        ai_reply = ask_ai(user_input, mode)
        
        # The ask_ai function already logs its own raw response and plugin actions.
        # We just need to display the final result.
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

    def view_history(self):
        history_window = HistoryWindow(self)
        history_window.show()
class HistoryWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("M.A.B.E.L History")
        self.resize(800, 600)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        layout.addWidget(self.history_display)

        self.load_history()

    def load_history(self):
        history_data = memory.get_history()
        self.history_display.clear()
        for entry in history_data:
            entry_type = entry.get("type", "unknown")
            timestamp = datetime.fromtimestamp(entry.get("timestamp", 0)).strftime('%Y-%m-%d %H:%M:%S')

            if entry_type == "user_input":
                mode = entry.get("mode", "N/A")
                user_input = entry.get("input", "N/A")
                self.history_display.append(f"<b>[{timestamp}] You ({mode}):</b> {user_input}")
            elif entry_type == "ai_response":
                user_input = entry.get("user_input", "N/A")
                ai_raw_response = entry.get("ai_raw_response", "N/A")
                self.history_display.append(f"<b>[{timestamp}] AI (Raw Response to '{user_input}'):</b> {ai_raw_response}")
            elif entry_type == "plugin_run":
                plugin = entry.get("plugin", "N/A")
                args = entry.get("args", {})
                output = entry.get("output", "N/A")
                self.history_display.append(f"<b>[{timestamp}] Plugin Run ({plugin}) with args {args}:</b> {output}")
            elif entry_type == "ai_plugin_action_result":
                plugin_command = entry.get("plugin_command", "N/A")
                plugin_output = entry.get("plugin_output", "N/A")
                self.history_display.append(f"<b>[{timestamp}] AI Plugin Action:</b> {plugin_command}<br><b>Output:</b> {plugin_output}")
            else:
                self.history_display.append(f"<b>[{timestamp}] Unknown Entry Type:</b> {entry}")