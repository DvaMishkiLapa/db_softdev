import sqlite3

class DBManager():
    def __init__(self):
        try:
            self.connect = sqlite3.connect('db.sqlite')
        except sqlite3.Error as e:
            print(e)
        self.cursor = self.connect.cursor()

    def _query(self, arg):
        self.cursor.execute(arg)
        self.connect.commit()
        return self.cursor

    def get_workers(self):
        return self._query("SELECT * FROM workers")

    def get_projects(self):
        return self._query("SELECT * FROM projects")

    def get_current_projects(self, worker_id):
        return self._query("SELECT * FROM projects WHERE id IN (SELECT project_id FROM data WHERE data.worker_id='{}')".format(worker_id))

    def get_id_project(self, project_name):
        return self._query("SELECT id FROM projects WHERE name='{}'".format(project_name))

    def update_workers(self, worker_data):
        return self._query("UPDATE workers SET surname='{1}', name='{2}', patronymic='{3}', post='{4}' WHERE id='{0}'".format(*worker_data))

    def insert_workers(self, worker_data):
        try:
            return self._query("INSERT INTO workers VALUES ('{}', '{}', '{}', '{}', '{}')".format(*worker_data))
        except:
            return []

    def update_projects(self, project_data):
        return self._query("UPDATE projects SET name='{1}', deadline='{2}' WHERE id='{0}'".format(*project_data))

    def insert_data(self, project_data):
        if not list(self._query("SELECT * FROM data WHERE worker_id='{}' AND project_id='{}'".format(*project_data))):
            return self._query("INSERT INTO data VALUES ('{}', '{}')".format(*project_data))

    def insert_projects(self, project_data):
        try:
            return self._query("INSERT INTO projects VALUES ('{}', '{}', '{}')".format(*project_data))
        except:
            return []
    
    def del_inproject(self, project_id):
        return self._query("DELETE FROM data WHERE project_id='{}'".format(project_id))

    def __del__(self):
        self.connect.close()
