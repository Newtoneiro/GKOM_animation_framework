from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QComboBox,
    QDoubleSpinBox,
    QPushButton,
    QSizePolicy
    )


class GUI(QWidget):
    def __init__(self, ge, parent=None):
        super(GUI, self).__init__()
        self.ge = ge
        self.selected_object = None
        self.current_objects = None
        self.properties_dict = {}

        self.layout = QGridLayout(self)
        self.create_label(text='current block:', grid_row=0)
        self.create_dropdown(grid_row=0)
        self.create_label(text='current block position:', grid_row=1)
        self.create_properties(
            property_name='pos',
            step=0.5,
            min_value=-100.0,
            max_value=100.0,
            grid_row=2
            )
        self.create_label(text='current block rotation:', grid_row=5)
        # problems with values, needs rewriting
        self.create_properties(
            property_name='rot',
            step=1.0,
            min_value=-100.0,
            max_value=100.0,
            grid_row=6
            )
        self.create_label(text='current block scale:', grid_row=9)
        self.create_properties(
            property_name='scale',
            step=0.1,
            min_value=0.0,
            max_value=10.0,
            grid_row=10
            )
        self.create_remove_button(grid_row=13)
        self.create_add_button(grid_row=13)
        self.create_label(text='current light position:', grid_row=14)
        # placeholder for light movement, not yet implemented
        self.create_properties(
            property_name='light',
            step=1.0,
            min_value=-100.0,
            max_value=100.0,
            grid_row=15
            )

    def create_label(self, text, grid_row) -> None:
        label = QLabel(text)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout.addWidget(label, grid_row, 0)

    def create_dropdown(self, grid_row) -> None:
        self.dropdown = QComboBox(self)
        self.layout.addWidget(self.dropdown, grid_row, 1)
        self.dropdown.currentIndexChanged.connect(self.on_selection_change)

    def check_dropdown(self) -> None:
        if self.ge._scene != self.current_objects:
            self.update_dropdown()
        else:
            pass

    def update_dropdown(self) -> None:
        self.dropdown.clear()
        for obj in self.ge._scene:
            self.dropdown.addItem(obj._name)
        self.current_objects = self.ge._scene

    def on_selection_change(self, index) -> None:
        selected_option = self.sender().currentText()
        self.selected_object = next(
            (obj for obj in self.ge._scene if obj._name == selected_option),
            None)

        property_groups = {
            'pos': self.selected_object._pos,
            'rot': self.selected_object._rot,
            'scale': self.selected_object._scale
        }

        for group_name, prop_values in property_groups.items():
            components = ['x', 'y', 'z']

            for component in components:
                spin_box_key = f'{group_name}.{component}'
                spin_box_value = prop_values[components.index(component)]
                self.properties_dict[spin_box_key].setValue(spin_box_value)

    def create_properties(
            self, property_name, step, min_value, max_value, grid_row
            ) -> None:
        for component in ['x', 'y', 'z']:
            label = QLabel(f"{component}:")
            self.layout.addWidget(label, grid_row, 0)
            spin_box = QDoubleSpinBox()
            spin_box.setRange(min_value, max_value)
            spin_box.setSingleStep(step)
            self.properties_dict[f'{property_name}.{component}'] = spin_box
            self.layout.addWidget(spin_box, grid_row, 1)
            grid_row += 1

            spin_box.valueChanged.connect(
                lambda value,
                prop=property_name,
                comp=component: self.property_change(prop, comp, value))

    def property_change(self, property_name, component, value) -> None:
        prop = getattr(self.selected_object, f"_{property_name}")
        index = {'x': 0, 'y': 1, 'z': 2}[component]
        new_prop = list(prop)
        new_prop[index] = value
        setattr(self.selected_object, f"_{property_name}", tuple(new_prop))

    def create_remove_button(self, grid_row) -> None:
        self.remove_button = QPushButton("remove current block")
        self.remove_button.clicked.connect(self.on_remove_button_click)
        self.layout.addWidget(self.remove_button, grid_row, 0)

    def create_add_button(self, grid_row) -> None:
        self.add_button = QPushButton("add new block")
        self.add_button.clicked.connect(self.on_add_button_click)
        self.layout.addWidget(self.add_button, grid_row, 1)

    def on_remove_button_click(self) -> None:
        # needs implementation
        print('remove')

    def on_add_button_click(self) -> None:
        # needs implementation
        print('add')
