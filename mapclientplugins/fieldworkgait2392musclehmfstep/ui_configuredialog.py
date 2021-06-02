# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuredialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        if not ConfigureDialog.objectName():
            ConfigureDialog.setObjectName(u"ConfigureDialog")
        ConfigureDialog.resize(550, 303)
        self.gridLayout = QGridLayout(ConfigureDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.configGroupBox = QGroupBox(ConfigureDialog)
        self.configGroupBox.setObjectName(u"configGroupBox")
        self.formLayout = QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.label0 = QLabel(self.configGroupBox)
        self.label0.setObjectName(u"label0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label0)

        self.lineEdit0 = QLineEdit(self.configGroupBox)
        self.lineEdit0.setObjectName(u"lineEdit0")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit0)

        self.label2 = QLabel(self.configGroupBox)
        self.label2.setObjectName(u"label2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label2)

        self.comboBox_in_unit = QComboBox(self.configGroupBox)
        self.comboBox_in_unit.setObjectName(u"comboBox_in_unit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_in_unit)

        self.label3 = QLabel(self.configGroupBox)
        self.label3.setObjectName(u"label3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label3)

        self.comboBox_out_unit = QComboBox(self.configGroupBox)
        self.comboBox_out_unit.setObjectName(u"comboBox_out_unit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox_out_unit)

        self.label4 = QLabel(self.configGroupBox)
        self.label4.setObjectName(u"label4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label4)

        self.checkBox_write_osim_file = QCheckBox(self.configGroupBox)
        self.checkBox_write_osim_file.setObjectName(u"checkBox_write_osim_file")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.checkBox_write_osim_file)

        self.label = QLabel(self.configGroupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label)

        self.checkBox_static_vas = QCheckBox(self.configGroupBox)
        self.checkBox_static_vas.setObjectName(u"checkBox_static_vas")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.checkBox_static_vas)

        self.label1 = QLabel(self.configGroupBox)
        self.label1.setObjectName(u"label1")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_osim_output_dir = QLineEdit(self.configGroupBox)
        self.lineEdit_osim_output_dir.setObjectName(u"lineEdit_osim_output_dir")

        self.horizontalLayout.addWidget(self.lineEdit_osim_output_dir)

        self.pushButton_osim_output_dir = QPushButton(self.configGroupBox)
        self.pushButton_osim_output_dir.setObjectName(u"pushButton_osim_output_dir")

        self.horizontalLayout.addWidget(self.pushButton_osim_output_dir)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_2 = QLabel(self.configGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_2)

        self.checkBox_update_knee_splines = QCheckBox(self.configGroupBox)
        self.checkBox_update_knee_splines.setObjectName(u"checkBox_update_knee_splines")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.checkBox_update_knee_splines)


        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit0, self.comboBox_in_unit)
        QWidget.setTabOrder(self.comboBox_in_unit, self.comboBox_out_unit)
        QWidget.setTabOrder(self.comboBox_out_unit, self.checkBox_write_osim_file)
        QWidget.setTabOrder(self.checkBox_write_osim_file, self.checkBox_static_vas)
        QWidget.setTabOrder(self.checkBox_static_vas, self.lineEdit_osim_output_dir)
        QWidget.setTabOrder(self.lineEdit_osim_output_dir, self.pushButton_osim_output_dir)
        QWidget.setTabOrder(self.pushButton_osim_output_dir, self.buttonBox)

        self.retranslateUi(ConfigureDialog)
        self.buttonBox.accepted.connect(ConfigureDialog.accept)
        self.buttonBox.rejected.connect(ConfigureDialog.reject)

        QMetaObject.connectSlotsByName(ConfigureDialog)
    # setupUi

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QCoreApplication.translate("ConfigureDialog", u"Configure Fieldwork Gait2392 Muscle HMF Step", None))
        self.configGroupBox.setTitle("")
        self.label0.setText(QCoreApplication.translate("ConfigureDialog", u"identifier:  ", None))
        self.label2.setText(QCoreApplication.translate("ConfigureDialog", u"Input unit:", None))
        self.label3.setText(QCoreApplication.translate("ConfigureDialog", u"Output unit:", None))
        self.label4.setText(QCoreApplication.translate("ConfigureDialog", u"Write Osim file:", None))
        self.checkBox_write_osim_file.setText("")
        self.label.setText(QCoreApplication.translate("ConfigureDialog", u"Static Vastus:", None))
        self.checkBox_static_vas.setText("")
        self.label1.setText(QCoreApplication.translate("ConfigureDialog", u"Output folder:", None))
        self.pushButton_osim_output_dir.setText(QCoreApplication.translate("ConfigureDialog", u"...", None))
        self.label_2.setText(QCoreApplication.translate("ConfigureDialog", u"Update Knee Splines:", None))
        self.checkBox_update_knee_splines.setText("")
    # retranslateUi

