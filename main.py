import sys
from PyQt5 import QtWidgets
import db
import ui

dbm = db.DBManager()

class ExampleApp(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        for worker in dbm.get_workers():
            row_pos = self.workers_table.rowCount()
            self.workers_table.insertRow(row_pos)
            i = 0
            for x in worker:
                self.workers_table.setItem(row_pos, i, QtWidgets.QTableWidgetItem(str(x)))
                i += 1
        
        for project in dbm.get_projects():
            row_pos = self.projects_table.rowCount()
            self.projects_table.insertRow(row_pos)
            i = 0
            for x in project:
                self.projects_table.setItem(row_pos, i, QtWidgets.QTableWidgetItem(str(x)))
                i += 1
        
        # buttons events
        self.workers_table.itemSelectionChanged.connect(self.current_projects_update)
        self.add_worker.clicked.connect(self.add_worker_click)
        self.del_worker.clicked.connect(self.del_worker_click)
        self.save_workers.clicked.connect(self.save_workers_click)
        
        self.add_project.clicked.connect(self.add_project_click)
        self.del_project.clicked.connect(self.del_project_click)
        self.save_projects.clicked.connect(self.save_project_click)

        self.new_inproject.clicked.connect(self.new_inproject_click)
        self.del_inproject.clicked.connect(self.del_inproject_click)

        self.worker_len = self.workers_table.rowCount()
        self.projects_len = self.projects_table.rowCount()

        self.get_list_projects()

    def current_projects_update(self):
        self.current_projects_table.setRowCount(0)
        items = self.workers_table.selectedItems()
        try:
            if items[4].text() == 'Уборщик':
                self.new_inproject.setEnabled(False)
                self.del_inproject.setEnabled(False)
                self.project_box.setEnabled(False)
            else:
                self.new_inproject.setEnabled(True)
                self.del_inproject.setEnabled(True)
                self.project_box.setEnabled(True)
            project_id = str(items[0].text())
        except IndexError:
            return
        for project in dbm.get_current_projects(project_id):
            row_pos = self.current_projects_table.rowCount()
            self.current_projects_table.insertRow(row_pos)
            i = 0
            for x in project:
                self.current_projects_table.setItem(row_pos, i, QtWidgets.QTableWidgetItem(str(x)))
                i += 1

    # buttons near workers_table
    def add_worker_click(self):
        row_pos = self.workers_table.rowCount()
        self.workers_table.insertRow(row_pos)

    def del_worker_click(self):
        indices = self.workers_table.selectionModel().selectedRows()
        for index in sorted(indices):
            self.workers_table.removeRow(index.row())

    def save_workers_click(self):
        row_pos = self.workers_table.rowCount()
        data = []
        for row in range(row_pos):
            data.append([])
            for col in range(5):
                try:
                    data[row].append(self.workers_table.item(row, col).text())
                except AttributeError:
                    pass
            if self.worker_len > row:
                dbm.update_workers(data[row])
            else:
                if dbm.insert_workers(data[row]):
                    self.worker_len = self.workers_table.rowCount()

    # buttons near current_projects_table
    def new_inproject_click(self):
        project_id = list(dbm.get_id_project(str(self.project_box.currentText())))[0][0]
        try:
            row = self.workers_table.selectionModel().selectedRows()[0].row()
        except IndexError:
            return
        worker_id = int(self.workers_table.item(row, 0).text())
        data = [worker_id, project_id]
        dbm.insert_data(data)
        self.current_projects_update()

    def del_inproject_click(self):
        try:
            row = self.current_projects_table.selectionModel().selectedRows()[0].row()
        except IndexError:
            return
        project_id = int(self.current_projects_table.item(row, 0).text())
        dbm.del_inproject(project_id)
        self.current_projects_update()

    def get_list_projects(self):
        projects_list = [x[1] for x in dbm.get_projects()]
        self.project_box.clear()
        self.project_box.addItems(projects_list)

    # buttons near projects_table
    def add_project_click(self):
        row_pos = self.projects_table.rowCount()
        self.projects_table.insertRow(row_pos)

    def del_project_click(self):
        indices = self.projects_table.selectionModel().selectedRows()
        for index in sorted(indices):
            self.projects_table.removeRow(index.row())

    def save_project_click(self):
        row_pos = self.projects_table.rowCount()
        data = []
        for row in range(row_pos):
            data.append([])
            for col in range(3):
                try:
                    data[row].append(self.projects_table.item(row, col).text())
                except AttributeError:
                    pass
            if self.projects_len > row:
                dbm.update_projects(data[row])
            else:
                if dbm.insert_projects(data[row]):
                    self.projects_len = self.projects_table.rowCount()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()