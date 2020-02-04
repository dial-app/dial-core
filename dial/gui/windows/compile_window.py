# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Window for all the parameters and compilation options (loss functions, epochs...)
"""

from PySide2.QtWidgets import QGridLayout, QWidget


class CompileWindow(QWidget):
    """
    Window for all the dataset related operations (Visualization, loading...)
    """

    def __init__(self, project_manager, parameters_form, parent=None):
        super().__init__(parent)

        # Initialize components
        self.__project_manager = project_manager

        # Initialize widgets
        self.__main_layout = QGridLayout()
        self.__parameters_form = parameters_form

        # Configure interface
        self.__setup_ui()

        # Connect signals
        self.__parameters_form.epoch_value_changed.connect(
            lambda value: self.__project_manager.change_parameter("epochs", value)
        )

    def __setup_ui(self):
        self.__main_layout.setContentsMargins(100, 100, 100, 100)

        self.__main_layout.addWidget(self.__parameters_form)

        self.setLayout(self.__main_layout)
