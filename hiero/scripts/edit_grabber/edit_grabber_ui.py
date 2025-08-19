import os
import hiero
from pathlib import Path
from PySide2 import QtWidgets, QtCore, QtGui

#CURRENT JOB
show = os.getenv("PROJECT")

print(root)

class CustomPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomPanel, self).__init__(parent)

        # Layouts
        main_layout = QtWidgets.QVBoxLayout(self)
        input_layout = QtWidgets.QHBoxLayout()
        toggles_layout = QtWidgets.QHBoxLayout()
        tasks = ["Editorial","Anim","Paint","Roto","Comp","Matchmove","Layout","Env","FX","CFX","Light","Client"]

        # Add dropdown
        self.dropdown = QtWidgets.QComboBox()
        self.dropdown.addItems(tasks)
        self.dropdown.setCurrentIndex(tasks.index("Comp"))
        input_layout.addWidget(self.dropdown)

        # Text input field
        self.label = QtWidgets.QLabel("Variant-Component:")
        self.textbox = QtWidgets.QLineEdit()
        self.textbox.setText("main-comp")
        input_layout.addWidget(self.label)
        input_layout.addWidget(self.textbox)

        # Add toggles
        self.toggle1 = QtWidgets.QCheckBox("Replace")
        toggles_layout.addWidget(self.toggle1)

        # Button
        self.button = QtWidgets.QPushButton("Update Edit")
        self.button.clicked.connect(self.run)

        # Assemble Layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(toggles_layout)
        main_layout.addWidget(self.button)

    def run(self):
        dropdown = self.dropdown.currentText()
        variant_component = self.textbox.text()
        replace = self.toggle1.isChecked()

        script_path = os.path.join(root, "scripts/edit_grabber/edit_grabber.py")

        with open(script_path, "r") as f:
            script_code = f.read()

        # print(dropdown, variant_component)

        variables = {
            "steps"             : [dropdown],
            "variant_component" : [variant_component],
            "replace"           : replace,
            "show"              : show
        }

        exec(script_code, variables)

def show_custom_panel():
    
    panel = CustomPanel()
    panel.setWindowTitle("Edit Grabber v1")
    panel.resize(350, 150)
    # window_manager = hiero.ui.windowManager()
    # window_manager.addWindow(panel, hiero.ui.WindowManager.WindowMenuSection.kApplicationSection, "Ctrl+Shift+E")
    panel.show()
    return panel

def run():
    hiero.core.executeInMainThread(show_custom_panel)
