import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.NewButton.clicked.connect(self.add)
        self.EditButton.clicked.connect(self.edit)
        self.updatetab()

    def updatetab(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM Coffi").fetchall()
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
        self.tableWidget.setRowCount(0)
        for row, items in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for col, item in enumerate(items):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))

    def edit(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if len(ids) == 1:
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            res = cur.execute(
                f'''SELECT Id, Name, Stepen, Molot, Vkys, Sum, Obem FROM Coffi WHERE id = {ids[0]}''').fetchall()
            self.add_film_widget = AddFilmWidget(self, res)
            self.add_film_widget.show()

    def add(self):
        self.add_film_widget = AddFilmWidget(self)
        self.add_film_widget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
