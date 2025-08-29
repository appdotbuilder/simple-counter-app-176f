from app.database import create_tables
import app.counter_ui


def startup() -> None:
    # this function is called before the first request
    create_tables()
    app.counter_ui.create()
