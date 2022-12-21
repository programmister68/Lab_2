from DataBase import DataBase
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog, QMessageBox

import sys

import logging
logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DataBase('cd_catalog.db')
        self.ui = uic.loadUi("forms/main.ui", self)
        self.window().setWindowTitle("Каталог CD-дисков")
        self.window().setWindowIcon(QIcon('img/cd.png'))

        self.ui.btn_add_cd.clicked.connect(self.add_cd)  # В скобках прописываем название функции
        self.ui.btn_save_cd.clicked.connect(self.save_cd)
        self.ui.btn_del_cd.clicked.connect(self.delete_cd)

        self.ui.btn_add_deptor.clicked.connect(self.add_debtor)  # В скобках прописываем название функции
        self.ui.btn_save_deptor.clicked.connect(self.save_debtor)
        self.ui.btn_del_deptor.clicked.connect(self.delete_debtor)

        self.comboBox_cd.addItems(self.db.get_cds())
        self.draw_cd()
        self.draw_debtor()
        logging.log(logging.INFO, 'Приложение запущено.')

    def add_debtor(self):
        name = self.ui.debtor_name.text()
        date = self.ui.debtor_date.text()
        cd_id = self.comboBox_cd.currentText()
        cd_id = cd_id.split(' ')[0]
        if name == '':
            msg = QMessageBox(self)
            # msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('img/error.ico'))
            msg.setText("Укажите имя должника")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            logging.log(logging.INFO, 'Ошибка.')
        else:
            self.db.add_in_debtors(name, date, cd_id)
            self.update_draw_debtor()
            self.label_message_dep.setText(' ')
            logging.log(logging.INFO, 'Данные добавлены в таблицу "Debtors".')

    def update_combobox(self):
        self.comboBox_cd.clear()
        self.comboBox_cd.addItems(self.db.get_cds())
        logging.log(logging.INFO, 'Виджет ComboBox обновлён.')

    def save_debtor(self):
        self.table = self.ui.debtor_table
        data = self.get_from_table()
        for string in data:
            if string[1] != '':
                self.db.update_debtors(string[0], string[1], string[2], string[3])
            else:
                self.db.delete_from_debtors(string[0])
        self.update_draw_debtor()
        self.label_message_dep.setStyleSheet("color:green")  # Изменение цвета шрифта на зелёный
        self.label_message_dep.setText('Данные о должниках сохранены')
        logging.log(logging.INFO, 'Данные сохранены.')

    def save_cd(self):
        self.table = self.ui.cd_table
        data = self.get_from_table()
        for string in data:
            if string[1] != '':
                self.db.update_cds(string[0], string[1], string[2], string[3], string[4])
            else:
                self.db.delete_from_cds(string[0])
        self.update_draw_cd()
        self.update_draw_debtor()
        self.update_combobox()
        self.label_message_cd.setStyleSheet("color:green")
        self.label_message_cd.setText('Данные о дисках сохранены')
        logging.log(logging.INFO, 'Данные сохранены.')

    def add_cd(self):
        name = self.ui.cd_name.text()
        descript = self.ui.cd_descript.text()
        genre = self.ui.cd_genre.text()
        pub = self.ui.cd_pub.text()

        if name == '':
            msg = QMessageBox(self)
            # msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('img/error.ico'))
            msg.setText("Укажите название диска")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            logging.log(logging.INFO, 'Ошибка.')
        else:
            self.db.add_in_cds(name, descript, genre, pub)
            self.update_draw_cd()
            self.update_combobox()
            self.label_message_cd.setText(' ')
            logging.log(logging.INFO, 'Данные добавлены в таблицу "CDs".')

    def update_draw_cd(self):
        self.table = self.ui.cd_table
        self.table.clear()
        self.draw_cd()

    def update_draw_debtor(self):
        self.table = self.ui.debtor_table
        self.table.clear()
        self.draw_debtor()

    def draw_cd(self):
        self.table = self.ui.cd_table
        rec = self.db.get_from_cds()
        self.table.setColumnCount(5)
        self.table.setRowCount(len(rec))
        self.ui.cd_table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Описание', 'Жанр', 'Издатель'])
        i = 0
        for cd in rec:
            x = 0
            self.table.setRowCount(i+1)
            for field in cd:
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)
                x += 1
            i += 1

    def draw_debtor(self):
        self.table = self.ui.debtor_table
        rec = self.db.get_from_debtors()
        self.table.setColumnCount(4)
        self.table.setRowCount(len(rec))
        i = 0
        self.ui.ui.debtor_table.setHorizontalHeaderLabels(
            ['ID', 'Имя', 'Дата', 'ID Диска'])
        for deb in rec:
            x = 0
            self.table.setRowCount(i+1)
            for field in deb:
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:  # для id делаем некликабельные (чтобы их нельзя было переписать) ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)
                x += 1
            i += 1

    def get_from_table(self):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                try:
                    tmp.append(self.table.item(row, col).text())
                except:
                    tmp.append('Error: No data')
            data.append(tmp)
        return data

    @pyqtSlot()
    def delete_cd(self):
        SelectedRow = self.cd_table.currentRow()
        rowcount = self.cd_table.rowCount()
        colcount = self.cd_table.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            # msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('img/error.ico'))
            msg.setText("В таблице нет данных")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            logging.log(logging.INFO, 'Ошибка.')

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            # msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('img/error.ico'))
            msg.setText("Выберите поле для удаления")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            logging.log(logging.INFO, 'Ошибка.')

        else:
            for col in range(1, colcount):
                self.cd_table.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.cd_table.model().index(-1, -1)
            self.cd_table.setCurrentIndex(ix)
            logging.log(logging.INFO, 'Данные удалены из таблицы "CDs".')
        self.label_message_cd.setText(' ')

    def delete_debtor(self):
        SelectedRow = self.debtor_table.currentRow()
        rowcount = self.debtor_table.rowCount()
        colcount = self.debtor_table.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setWindowIcon(QIcon('img/error.ico'))
            msg.setText("В таблице нет данных")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            logging.log(logging.INFO, 'Ошибка.')

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            # msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('img/error.ico'))
            msg.setText("Выберите поле для удаления")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            logging.log(logging.INFO, 'Ошибка.')

        else:
            for col in range(1, colcount):
                self.debtor_table.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.debtor_table.model().index(-1, -1)
            self.debtor_table.setCurrentIndex(ix)
            logging.log(logging.INFO, 'Данные удалены из таблицы "Debtors".')
        self.label_message_dep.setText(' ')


class Builder:
    def __init__(self):
        qapp = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        qapp.exec()


if __name__ == '__main__':
    B = Builder()
    logging.log(logging.INFO, 'Приложение завершило свою работу.')

