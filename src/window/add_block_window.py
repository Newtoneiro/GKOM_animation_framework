"""
This module contains the AddBlockWindow class.
"""

from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QDialog,
    QLineEdit,
    QButtonGroup,
    QRadioButton
    )


class AddBlockWindow(QDialog):
    """
    Class for the add block window.
    """
    def __init__(self, parent=None):
        super(AddBlockWindow, self).__init__(parent)
        self.hidden_elements = []
        self.name_input = QLineEdit()
        self.default_cube_button = QRadioButton('default cube')
        self.custom_model_button = QRadioButton('custom model')
        self.texture_path_input = QLineEdit()
        self.object_path_input = QLineEdit()
        self._init_ui()

    # ====== INITIALIZATION ====== #

    def _init_ui(self) -> None:
        """
        Initializes the window.
        """
        self.setWindowTitle('add block')
        self.layout = QGridLayout(self)

        self.create_input(
            label_text="new block name:",
            line_edit=self.name_input,
            grid_row=0,
            grid_col=0
        )
        self.create_radio_button_group(
            label_text="new block type:",
            buttons=[self.default_cube_button, self.custom_model_button],
            grid_row=1
        )
        self.default_cube_button.setChecked(True)
        self.default_cube_button.toggled.connect(self.enable_input)
        self.create_hidden_elements(
            label_text="model texture path:",
            line_edit=self.texture_path_input,
            button_callback=self.choose_texture_path,
            grid_row=3
        )
        self.create_hidden_elements(
            label_text="model object path:",
            line_edit=self.object_path_input,
            button_callback=self.choose_object_path,
            grid_row=5)
        self.create_confirm_buttons(
            label_text='add block?',
            grid_row=7,
            grid_col=0
        )

    # ====== PUBLIC METHODS ====== #

    def create_input(
        self,
        label_text: str,
        line_edit: QLineEdit,
        grid_row: int,
        grid_col: int
    ) -> None:
        """
        Creates an input element.
        """
        label = QLabel(label_text)
        self.layout.addWidget(label, grid_row, grid_col)
        self.layout.addWidget(line_edit, grid_row, grid_col + 1)

    def create_radio_button_group(
        self,
        label_text: str,
        buttons: list[QRadioButton],
        grid_row: int
    ) -> None:
        """
        Creates a radio button group.
        """
        label = QLabel(label_text)
        self.layout.addWidget(label, grid_row, 0)

        button_group = QButtonGroup()
        for grid_col, button in enumerate(buttons):
            self.layout.addWidget(button, grid_row + 1, grid_col)
            button_group.addButton(button)

    def create_hidden_elements(
        self,
        label_text: str,
        line_edit: QLineEdit,
        button_callback: callable,
        grid_row: int
    ) -> None:
        """
        Creates hidden elements.
        """
        label = QLabel(label_text)
        line_edit.setReadOnly(True)
        button = QPushButton('select')
        button.clicked.connect(button_callback)

        self.layout.addWidget(label, grid_row, 0)
        self.layout.addWidget(line_edit, grid_row, 1)
        self.layout.addWidget(button, grid_row + 1, 1)

        self.hidden_elements.extend([label, line_edit, button])
        for element in self.hidden_elements:
            element.setVisible(False)

    def create_confirm_buttons(
        self,
        label_text: str,
        grid_row: int,
        grid_col: int
    ) -> None:
        """
        Creates confirm buttons.
        """
        accept_label = QLabel(label_text)
        ok_button = QPushButton('ok')
        cancel_button = QPushButton('cancel')
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(accept_label, grid_row, grid_col)
        self.layout.addWidget(ok_button, grid_row + 1, grid_col)
        self.layout.addWidget(cancel_button, grid_row + 1, grid_col + 1)

    def choose_texture_path(self) -> None:
        """
        Opens the file dialog to choose the texture path.
        """
        file_ext = "JPEG Files (*.jpg);;All Files (*)"
        self.choose_file_path(self.texture_path_input, file_ext)

    def choose_object_path(self) -> None:
        """
        Opens the file dialog to choose the object path.
        """
        file_ext = "Wavefront OBJ Files (*.obj);;All Files (*)"
        self.choose_file_path(self.object_path_input, file_ext)

    def choose_file_path(
        self,
        line_edit: QLineEdit,
        file_ext: str
    ) -> None:
        """
        Opens the file dialog to choose the file path.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "./src/models/",
            file_ext,
            options=options
        )
        if file_name:
            line_edit.setText(file_name)

    def enable_input(self):
        """
        Enables the input elements.
        """
        is_default_cube_checked = self.default_cube_button.isChecked()
        for element in self.hidden_elements:
            element.setVisible(not is_default_cube_checked)
