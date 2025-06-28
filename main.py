from gui.page_manager import PageManager
from gui.root_window import Root
from db.db_config import DB

if __name__ == "__main__":
    db = DB()
    root = Root()
    connection = db.get_connection()
    controller = PageManager(root.get_root(), db)

    root.inject_controller(controller)  # sidebar needs to call controller
    controller.show_page("dashboard")

    root.run()
