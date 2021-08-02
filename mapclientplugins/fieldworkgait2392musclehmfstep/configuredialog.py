import os
from PySide2 import QtWidgets
from mapclientplugins.fieldworkgait2392musclehmfstep.ui_configuredialog import Ui_ConfigureDialog
from mapclientplugins.fieldworkgait2392musclehmfstep.gait2392musclecusthmf import VALID_UNITS

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''


class ConfigureDialog(QtWidgets.QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """

    def __init__(self, parent=None):
        """
        Constructor
        """
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)

        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._setupDialog()
        self._makeConnections()

    def _setupDialog(self):
        for s in VALID_UNITS:
            self._ui.comboBox_in_unit.addItem(s)
            self._ui.comboBox_out_unit.addItem(s)

    def _makeConnections(self):
        self._ui.lineEdit0.textChanged.connect(self.validate)
        self._ui.lineEdit_osim_output_dir.textChanged.connect(self._osimOutputDirEdited)
        self._ui.pushButton_osim_output_dir.clicked.connect(self._osimOutputDirClicked)

    def accept(self):
        """
        Override the accept method so that we can confirm saving an
        invalid configuration.
        """
        result = QtWidgets.QMessageBox.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(self, 'Invalid Configuration',
                                                   'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            QtWidgets.QDialog.accept(self)

    def validate(self):
        """
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        """
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        idValue = self.identifierOccursCount(self._ui.lineEdit0.text())
        idValid = (idValue == 0) or (idValue == 1 and self._previousIdentifier == self._ui.lineEdit0.text())
        if idValid:
            self._ui.lineEdit0.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.lineEdit0.setStyleSheet(INVALID_STYLE_SHEET)

        osimOutputDirValid = os.path.exists(self._ui.lineEdit_osim_output_dir.text())
        if osimOutputDirValid:
            self._ui.lineEdit_osim_output_dir.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.lineEdit_osim_output_dir.setStyleSheet(INVALID_STYLE_SHEET)

        valid = idValid and osimOutputDirValid
        self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(valid)

        return valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = self._ui.lineEdit0.text()
        config = {}
        config['identifier'] = self._ui.lineEdit0.text()
        config['osim_output_dir'] = self._ui.lineEdit_osim_output_dir.text()
        config['in_unit'] = self._ui.comboBox_in_unit.currentText()
        config['out_unit'] = self._ui.comboBox_out_unit.currentText()
        if self._ui.checkBox_write_osim_file.isChecked():
            config['write_osim_file'] = True
        else:
            config['write_osim_file'] = False
        if self._ui.checkBox_update_knee_splines.isChecked():
            config['update_knee_splines'] = True
        else:
            config['update_knee_splines'] = False
        if self._ui.checkBox_static_vas.isChecked():
            config['static_vas'] = True
        else:
            config['static_vas'] = False
        return config

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = config['identifier']
        self._ui.lineEdit0.setText(config['identifier'])
        self._previousOsimOutputDir = config['osim_output_dir']
        self._ui.lineEdit_osim_output_dir.setText(config['osim_output_dir'])
        self._ui.comboBox_in_unit.setCurrentIndex(
            VALID_UNITS.index(
                config['in_unit']
            )
        )
        self._ui.comboBox_out_unit.setCurrentIndex(
            VALID_UNITS.index(
                config['out_unit']
            )
        )

        if config['write_osim_file']:
            self._ui.checkBox_write_osim_file.setChecked(bool(True))
        else:
            self._ui.checkBox_write_osim_file.setChecked(bool(False))

        if config.get('update_knee_splines') is None:
            config['update_knee_splines'] = False
        if config['update_knee_splines']:
            self._ui.checkBox_update_knee_splines.setChecked(bool(True))
        else:
            self._ui.checkBox_update_knee_splines.setChecked(bool(False))

        if config['static_vas']:
            self._ui.checkBox_static_vas.setChecked(bool(True))
        else:
            self._ui.checkBox_static_vas.setChecked(bool(False))

    def _osimOutputDirClicked(self):
        location = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory', self._previousOsimOutputDir)
        if location:
            self._previousOsimOutputDir = location
            self._ui.lineEdit_osim_output_dir.setText(location)

    def _osimOutputDirEdited(self):
        self.validate()
