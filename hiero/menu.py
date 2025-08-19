from PySide2 import QtWidgets
import hiero.ui
from pathlib import Path

# 1. Define your function
def my_custom_function():
    path_root = Path(__file__).parent
    ui_path = path_root / "scripts/edit_grabber/edit_grabber_ui.py"
    
    with open(ui_path, "r") as f:
        script_code = f.read()

    namespace = {"root": path_root}

    exec(script_code, namespace)

    namespace["run"]()

# 2. Create an action
my_action = QtWidgets.QAction("Edit Grabber v1", None)
my_action.triggered.connect(my_custom_function)

# 3. Access the main menu bar
main_window = hiero.ui.mainWindow()
menu_bar = main_window.menuBar()

# 4. Check if your menu already exists, otherwise create it
custom_menu = None
for menu in menu_bar.findChildren(QtWidgets.QMenu):
    if menu.title() == "TA Tools":
        custom_menu = menu
        break

if not custom_menu:
    custom_menu = QtWidgets.QMenu("TA Tools", menu_bar)
    menu_bar.addMenu(custom_menu)

# 5. Add your action to your custom menu
custom_menu.addAction(my_action)