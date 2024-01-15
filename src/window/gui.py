from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QComboBox,
    QDoubleSpinBox,
    QPushButton,
    QSizePolicy,
    QMessageBox,
    QDialog
    )

import glm

from src.window.add_block_window import AddBlockWindow
from src.objects.cube import Cube
from src.objects.model_3d import Model3D
from src.constants import OPENGL_CONSTANTS, PROPERTIES_CONSTANTS
from src.graphics_engine import GraphicsEngine


class GUI(QWidget):
    def __init__(self, ge: GraphicsEngine):
        super(GUI, self).__init__()
        self.ge = ge
        self.selected_object = None
        self.properties_dict = {}
        self.render_initialized = False
        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout(self)
        self.create_label(text='current block:', grid_row=0)
        self.create_dropdown(grid_row=0)
        self.create_label(text='current block position:', grid_row=1)
        self.create_properties(
            target='object',
            property_name='pos',
            step=0.5,
            min_value=PROPERTIES_CONSTANTS.POSITION_MIN,
            max_value=PROPERTIES_CONSTANTS.POSITION_MAX,
            grid_row=2
            )
        self.create_label(text='current block rotation:', grid_row=5)
        self.create_properties(
            target='object',
            property_name='rot',
            step=1.0,
            min_value=PROPERTIES_CONSTANTS.ROTATION_MIN,
            max_value=PROPERTIES_CONSTANTS.ROTATION_MAX,
            grid_row=6
            )
        self.create_label(text='current block scale:', grid_row=9)
        self.create_properties(
            target='object',
            property_name='scale',
            step=0.1,
            min_value=PROPERTIES_CONSTANTS.SCALE_MIN,
            max_value=PROPERTIES_CONSTANTS.SCALE_MAX,
            grid_row=10
            )
        self.create_remove_button(grid_row=13)
        self.create_add_button(grid_row=13)
        self.create_label(text='current light position:', grid_row=14)
        self.create_properties(
            target='light',
            property_name='position',
            step=0.5,
            min_value=PROPERTIES_CONSTANTS.LIGHT_POSITION_MIN,
            max_value=PROPERTIES_CONSTANTS.LIGHT_POSITION_MAX,
            grid_row=15
            )

    # ====== GUI ELEMENTS' CREATION ====== #

    def create_label(self, text: str, grid_row: int) -> None:
        label = QLabel(text)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout.addWidget(label, grid_row, 0)

    def create_dropdown(self, grid_row: int) -> None:
        self.dropdown = QComboBox(self)
        self.layout.addWidget(self.dropdown, grid_row, 1)
        self.dropdown.currentIndexChanged.connect(self.on_selection_change)

    def create_properties(
            self,
            target: str,
            property_name: str,
            step: float,
            min_value: float,
            max_value: float,
            grid_row: int
    ) -> None:
        for comp in ['x', 'y', 'z']:
            label = QLabel(f'{comp}:')
            self.layout.addWidget(label, grid_row, 0)
            spin_box = QDoubleSpinBox()
            spin_box.setRange(min_value, max_value)
            spin_box.setSingleStep(step)
            self.properties_dict[f'{target}.{property_name}.{comp}'] = spin_box
            self.layout.addWidget(spin_box, grid_row, 1)
            grid_row += 1

            spin_box.valueChanged.connect(
                lambda value,
                prop=property_name,
                comp=comp: self.on_property_change(target, prop, comp, value)
            )

    def create_remove_button(self, grid_row: int) -> None:
        self.remove_button = QPushButton("remove current block")
        self.remove_button.clicked.connect(self.on_remove_button_click)
        self.layout.addWidget(self.remove_button, grid_row, 0)

    def create_add_button(self, grid_row: int) -> None:
        self.add_button = QPushButton("add new block")
        self.add_button.clicked.connect(self.on_add_button_click)
        self.layout.addWidget(self.add_button, grid_row, 1)

    # ====== GUI ELEMENTS' ACTIONS ====== #

    def on_selection_change(self, _) -> None:
        selected_option = self.sender().currentText()
        self.selected_object = next(
            (obj for obj in self.ge._scene if obj._name == selected_option),
            None)

        if self.selected_object is not None:
            degrees_rot = tuple(
                glm.degrees(a) for a in self.selected_object._rot
            )
            property_groups = {
                'pos': self.selected_object._pos,
                'rot': degrees_rot,
                'scale': self.selected_object._scale
            }

            for group_name, prop_values in property_groups.items():
                components = ['x', 'y', 'z']

                for comp in components:
                    spin_box_key = f'object.{group_name}.{comp}'
                    spin_box_value = prop_values[components.index(comp)]
                    self.properties_dict[spin_box_key].setValue(spin_box_value)

    def on_property_change(
            self,
            target: str,
            property_name: str,
            comp: int,
            value: float) -> None:
        obj = self.ge._light if target == 'light' else self.selected_object
        prop = getattr(obj, f'_{property_name}')

        index = {'x': 0, 'y': 1, 'z': 2}[comp]
        new_prop = list(prop)

        if property_name == 'rot':
            new_prop[index] = glm.radians(value)
        else:
            new_prop[index] = value

        new_prop = tuple(new_prop)

        if target == 'light':
            new_prop = glm.vec3(new_prop)

        setattr(obj, f'_{property_name}', new_prop)

    def on_remove_button_click(self) -> None:
        button = QMessageBox.question(
            self, 'remove block', 'are you sure you want to remove the block?'
        )
        if button == QMessageBox.Yes:
            self.remove_block()

    def on_add_button_click(self) -> None:
        add_popup = AddBlockWindow(self)
        result = add_popup.exec()

        if result == QDialog.Accepted:
            block_name = add_popup.name_input.text()
            if add_popup.default_cube_button.isChecked():
                self.add_cube(block_name)
            else:
                texture_path = add_popup.texture_path_input.text()
                object_path = add_popup.object_path_input.text()
                self.add_other(block_name, texture_path, object_path)

    # ====== UPDATE STATE ====== #

    def update(self):
        if self.render_initialized is False and self.ge._scene is not None:
            self.update_dropdown()
            self.render_initialized = True
        self.update_light()

    def update_light(self) -> None:
        components = ['x', 'y', 'z']
        for comp in components:
            spin_box_key = f'light.position.{comp}'
            spin_box_value = self.ge._light._position[components.index(comp)]
            self.properties_dict[spin_box_key].setValue(spin_box_value)

    def update_dropdown(self) -> None:
        self.dropdown.clear()
        for obj in self.ge._scene:
            self.dropdown.addItem(obj._name)

    def remove_block(self):
        self.ge._scene.remove(self.selected_object)
        self.selected_object.destroy()
        self.update_dropdown()

    def add_cube(self, block_name: str):
        cube = Cube(
            self.ge,
            texture_path="src/textures/crate.png",
            pos=OPENGL_CONSTANTS.DEFAULT_POSITION,
            rot=OPENGL_CONSTANTS.DEFAULT_ROTATION,
            scale=OPENGL_CONSTANTS.DEFAULT_SCALE,
            name=block_name
        )
        self.add_block(block_name, cube)

    def add_other(
            self,
            block_name: str,
            texture_path: str,
            object_path: str
    ) -> None:
        model = Model3D(
            self.ge,
            texture_path=texture_path,
            object_path=object_path,
            pos=OPENGL_CONSTANTS.DEFAULT_POSITION,
            rot=OPENGL_CONSTANTS.DEFAULT_ROTATION,
            scale=OPENGL_CONSTANTS.DEFAULT_SCALE,
            name=block_name
        )
        self.add_block(block_name, model)

    def add_block(
            self,
            block_name: str,
            block: Cube or Model3D
    ) -> None:
        name_exists = any(obj._name == block_name for obj in self.ge._scene)
        if block_name == "":
            self.name_empty()
        elif name_exists:
            self.name_exists()
        else:
            self.ge._scene.insert(0, block)
            self.update_dropdown()

    def name_empty(self) -> None:
        QMessageBox.warning(
            self,
            'add block error',
            'block name cannot be blank',
            QMessageBox.Ok
        )
        self.on_add_button_click()

    def name_exists(self) -> None:
        QMessageBox.warning(
            self,
            'add block error',
            'block with that name already exists',
            QMessageBox.Ok
        )
        self.on_add_button_click()
