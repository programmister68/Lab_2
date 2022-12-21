import sys
from unittest import TestCase

from PyQt5 import QtCore
from PyQt5.QtCore import QDate, QItemSelectionModel
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from DataBase import DataBase
from gui import MainWindow


class TestAddData(TestCase):
    def setUp(self):
        self.qapp = QApplication(sys.argv)
        self.db = DataBase()
        self.window = MainWindow()

    def test_add_cd(self):
        btn_add = self.window.ui.btn_add_cd  # Объявление кнопки

        self.window.ui.cd_name.setText("cd")
        self.window.ui.cd_descript.setText("test_test")
        self.window.ui.cd_genre.setText("test_test")
        self.window.ui.cd_pub.setText("test_test")

        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)

    def test_add_debtor(self):
        btn_add = self.window.ui.btn_add_deptor  # Объявление кнопки

        self.window.ui.debtor_name.setText("debtor_name")
        self.window.ui.debtor_date.setDate(QDate.fromString("01.01.2022"))
        self.window.ui.comboBox_cd.addItems(self.db.get_cds())

        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)
        self.db.delete_from_debtors(1)
        self.db.delete_from_debtors2(1)
        self.db.delete_from_cds(1)


class TestDeleteAndSave(TestCase):
    def setUp(self):
        self.qapp = QApplication(sys.argv)
        self.db = DataBase()
        self.window = MainWindow()

    def test_delete_cd(self):
        self.db.add_in_cds("name", "description", "genre", "publisher")
        QTest.mouseClick(self.window.ui.btn_save_cd, QtCore.Qt.MouseButton.LeftButton)

        rowcount = self.window.cd_table.rowCount()
        self.window.cd_table.setCurrentCell(rowcount-1, 1, QItemSelectionModel.SelectionFlag.Select)

        btn_del = self.window.ui.btn_del_cd
        QTest.mouseClick(btn_del, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.window.ui.btn_save_cd, QtCore.Qt.MouseButton.LeftButton)

    def test_delete_deb(self):
        self.db.add_in_debtors("name", "date", 1)
        QTest.mouseClick(self.window.ui.btn_save_deptor, QtCore.Qt.MouseButton.LeftButton)

        rowcount = self.window.debtor_table.rowCount()
        self.window.debtor_table.setCurrentCell(rowcount-1, 1, QItemSelectionModel.SelectionFlag.Select)

        btn_del = self.window.ui.btn_del_deptor
        QTest.mouseClick(btn_del, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.window.ui.btn_save_deptor, QtCore.Qt.MouseButton.LeftButton)
