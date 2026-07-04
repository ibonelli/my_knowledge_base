import sys

from PyQt6.QtWidgets import QApplication

from .. import index
from ..cli import DEFAULT_ARTICLES_DIR, DEFAULT_DB_PATH
from .main_window import MainWindow


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv if argv is None else [sys.argv[0]] + argv
    app = QApplication(argv)

    args = app.arguments()
    articles_dir = DEFAULT_ARTICLES_DIR
    db_path = DEFAULT_DB_PATH
    if "--articles-dir" in args:
        articles_dir = args[args.index("--articles-dir") + 1]
    if "--db" in args:
        db_path = args[args.index("--db") + 1]

    conn = index.connect(db_path)
    window = MainWindow(articles_dir, conn)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
