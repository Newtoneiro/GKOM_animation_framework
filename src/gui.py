from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QComboBox,
    QDoubleSpinBox,
    QPushButton,
    QSizePolicy
    )

import glm


class GUI(QWidget):
    def __init__(self, ge, parent=None):
        super(GUI, self).__init__()
        self.ge = ge
        self.selected_object = None
        self.properties_dict = {}
        self.render_initialized = False
        self.init_gui_comps()

    def init_gui_comps(self):
        self.layout = QGridLayout(self)
        self.create_label(text='current block:', grid_row=0)
        self.create_dropdown(grid_row=0)
        self.create_label(text='current block position:', grid_row=1)
        self.create_properties(
            target='object',
            property_name='pos',
            step=0.5,
            min_value=-100.0,
            max_value=100.0,
            grid_row=2
            )
        self.create_label(text='current block rotation:', grid_row=5)
        # problems with values, needs rewriting
        self.create_properties(
            target='object',
            property_name='rot',
            step=1.0,
            min_value=-100.0,
            max_value=100.0,
            grid_row=6
            )
        self.create_label(text='current block scale:', grid_row=9)
        self.create_properties(
            target='object',
            property_name='scale',
            step=0.1,
            min_value=0.0,
            max_value=10.0,
            grid_row=10
            )
        self.create_remove_button(grid_row=13)
        self.create_add_button(grid_row=13)
        self.create_label(text='current light position:', grid_row=14)
        self.create_properties(
            target='light',
            property_name='position',
            step=0.5,
            min_value=-500.0,
            max_value=500.0,
            grid_row=15
            )

    # ====== GUI ELEMENTS' CREATION ====== #

    def create_label(self, text, grid_row) -> None:
        label = QLabel(text)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout.addWidget(label, grid_row, 0)

    def create_dropdown(self, grid_row) -> None:
        self.dropdown = QComboBox(self)
        self.layout.addWidget(self.dropdown, grid_row, 1)
        self.dropdown.currentIndexChanged.connect(self.on_selection_change)

    def create_properties(
            self, target, property_name, step, min_value, max_value, grid_row
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

    def create_remove_button(self, grid_row) -> None:
        self.remove_button = QPushButton("remove current block")
        self.remove_button.clicked.connect(self.on_remove_button_click)
        self.layout.addWidget(self.remove_button, grid_row, 0)

    def create_add_button(self, grid_row) -> None:
        self.add_button = QPushButton("add new block")
        self.add_button.clicked.connect(self.on_add_button_click)
        self.layout.addWidget(self.add_button, grid_row, 1)

    # ====== GUI ELEMENTS' ACTIONS ====== #

    def on_selection_change(self, index) -> None:
        selected_option = self.sender().currentText()
        self.selected_object = next(
            (obj for obj in self.ge._scene if obj._name == selected_option),
            None)

        if self.selected_object is not None:
            property_groups = {
                'pos': self.selected_object._pos,
                'rot': self.selected_object._rot,
                'scale': self.selected_object._scale
            }

            for group_name, prop_values in property_groups.items():
                comps = ['x', 'y', 'z']

                for comp in comps:
                    spin_box_key = f'object.{group_name}.{comp}'
                    spin_box_value = prop_values[comps.index(comp)]
                    self.properties_dict[spin_box_key].setValue(spin_box_value)

    def on_property_change(self, target, property_name, comp, value) -> None:
        if target == 'light':
            obj = self.ge._light
        else:
            obj = self.selected_object
        prop = getattr(obj, f'_{property_name}')
        index = {'x': 0, 'y': 1, 'z': 2}[comp]
        new_prop = list(prop)
        new_prop[index] = value
        new_prop = tuple(new_prop)
        if target == 'light':
            new_prop = glm.vec3(new_prop)
        setattr(obj, f'_{property_name}', new_prop)

    def on_remove_button_click(self) -> None:
        self.ge._scene.remove(self.selected_object)
        self.selected_object.destroy()
        self.update_dropdown()

    def on_add_button_click(self) -> None:
        # needs implementation
        pass

    # ====== UPDATE LOOP ====== #

    def update(self):
        if self.render_initialized is False and self.ge._scene is not None:
            self.update_dropdown()
            self.render_initialized = True
        self.update_light()

    def update_light(self) -> None:
        comps = ['x', 'y', 'z']
        for comp in comps:
            spin_box_key = f'light.position.{comp}'
            spin_box_value = self.ge._light._position[comps.index(comp)]
            self.properties_dict[spin_box_key].setValue(spin_box_value)

    def update_dropdown(self) -> None:
        self.dropdown.clear()
        for obj in self.ge._scene:
            self.dropdown.addItem(obj._name)
        self.current_objects = self.ge._scene
