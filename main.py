from gui.dashboard import Dashboard
from db.db_config import DB

if __name__ == "__main__":

    database = DB()

    app = Dashboard()
    app.run()
