from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from .. import core, storage
from ..models import MEDIA_TYPES

THUMBNAIL_SIZE = 96


def _split_list(text: str) -> list[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


class MainWindow(QMainWindow):
    def __init__(self, articles_dir: str, conn):
        super().__init__()
        self.articles_dir = articles_dir
        self.conn = conn
        self.current_id: str | None = None

        self.setWindowTitle("Article Catalog")
        self.resize(1100, 700)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_list_panel())
        splitter.addWidget(self._build_detail_panel())
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        self.setCentralWidget(splitter)

        self.refresh_list()
        self.on_new()

    # ---- list/search panel (FR-011 left side) ----
    def _build_list_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)

        search_row = QHBoxLayout()
        self.tag_filter = QLineEdit()
        self.tag_filter.setPlaceholderText("tag")
        self.title_filter = QLineEdit()
        self.title_filter.setPlaceholderText("title")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.on_search)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.on_clear_search)
        search_row.addWidget(self.tag_filter)
        search_row.addWidget(self.title_filter)
        search_row.addWidget(search_btn)
        search_row.addWidget(clear_btn)
        layout.addLayout(search_row)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.list_widget.currentItemChanged.connect(self.on_select)
        layout.addWidget(self.list_widget)

        button_row = QHBoxLayout()
        new_btn = QPushButton("New")
        new_btn.clicked.connect(self.on_new)
        reindex_btn = QPushButton("Reindex")
        reindex_btn.clicked.connect(self.on_reindex)
        button_row.addWidget(new_btn)
        button_row.addWidget(reindex_btn)
        layout.addLayout(button_row)

        return panel

    # ---- detail/edit panel (FR-011 right side) ----
    def _build_detail_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)

        form = QFormLayout()
        self.title_edit = QLineEdit()
        self.media_type_combo = QComboBox()
        self.media_type_combo.addItems(sorted(MEDIA_TYPES))
        self.summary_edit = QLineEdit()
        self.tags_edit = QLineEdit()
        self.references_edit = QLineEdit()
        self.images_edit = QLineEdit()
        self.published_date_edit = QLineEdit()
        self.published_date_edit.setPlaceholderText("YYYY-MM-DD (blank = today)")
        form.addRow("Title", self.title_edit)
        form.addRow("Media type", self.media_type_combo)
        form.addRow("Summary", self.summary_edit)
        form.addRow("Tags (comma-separated)", self.tags_edit)
        form.addRow("References (comma-separated)", self.references_edit)
        form.addRow("Images (comma-separated paths)", self.images_edit)
        form.addRow("Published date", self.published_date_edit)
        layout.addLayout(form)

        # FR-009: split-pane Markdown editor + live rendered preview.
        body_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.body_edit = QPlainTextEdit()
        self.body_edit.textChanged.connect(self.on_body_changed)
        self.body_preview = QTextBrowser()
        body_splitter.addWidget(self.body_edit)
        body_splitter.addWidget(self.body_preview)
        layout.addWidget(body_splitter, stretch=1)

        # FR-010: inline image thumbnail previews.
        self.thumbnails_row = QHBoxLayout()
        layout.addLayout(self.thumbnails_row)

        button_row = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.on_save)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.on_delete)
        button_row.addWidget(self.save_btn)
        button_row.addWidget(self.delete_btn)
        layout.addLayout(button_row)

        return panel

    # ---- list / search ----
    def refresh_list(self, rows=None) -> None:
        self.list_widget.clear()
        rows = rows if rows is not None else core.list_articles(self.conn)
        for article_id, title, media_type, published_date, _file_path in rows:
            item = QListWidgetItem(f"[{media_type}] {title}  ({published_date or '-'})")
            item.setData(Qt.ItemDataRole.UserRole, article_id)
            self.list_widget.addItem(item)

    def on_search(self) -> None:
        tag = self.tag_filter.text().strip() or None
        title = self.title_filter.text().strip() or None
        self.refresh_list(core.search_articles(self.conn, tag=tag, title=title))

    def on_clear_search(self) -> None:
        self.tag_filter.clear()
        self.title_filter.clear()
        self.refresh_list()

    def on_select(self, current: QListWidgetItem, _previous) -> None:
        if current is None:
            return
        article_id = current.data(Qt.ItemDataRole.UserRole)
        article = core.get_article(self.articles_dir, article_id)
        self.load_article(article)

    # ---- detail form ----
    def on_new(self) -> None:
        self.current_id = None
        self.title_edit.clear()
        self.media_type_combo.setCurrentIndex(0)
        self.summary_edit.clear()
        self.tags_edit.clear()
        self.references_edit.clear()
        self.images_edit.clear()
        self.published_date_edit.clear()
        self.body_edit.clear()
        self.delete_btn.setEnabled(False)
        self._update_thumbnails([])

    def load_article(self, article) -> None:
        self.current_id = article.id
        self.title_edit.setText(article.title)
        combo_index = self.media_type_combo.findText(article.media_type)
        if combo_index >= 0:
            self.media_type_combo.setCurrentIndex(combo_index)
        self.summary_edit.setText(article.summary)
        self.tags_edit.setText(", ".join(article.tags))
        self.references_edit.setText(", ".join(article.references))
        self.images_edit.setText(", ".join(article.images))
        self.published_date_edit.setText(article.published_date or "")
        self.body_edit.setPlainText(article.body)
        self.delete_btn.setEnabled(True)
        self._update_thumbnails(article.images)

    def on_body_changed(self) -> None:
        self.body_preview.setMarkdown(self.body_edit.toPlainText())

    def _update_thumbnails(self, image_paths: list[str]) -> None:
        while self.thumbnails_row.count():
            item = self.thumbnails_row.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for image_path in image_paths:
            label = QLabel()
            path = Path(image_path)
            if not path.is_absolute():
                path = Path(self.articles_dir) / path
            pixmap = QPixmap(str(path))
            if pixmap.isNull():
                label.setText(f"[missing: {image_path}]")
            else:
                label.setPixmap(
                    pixmap.scaled(
                        THUMBNAIL_SIZE,
                        THUMBNAIL_SIZE,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
            self.thumbnails_row.addWidget(label)

    # ---- save / delete / reindex ----
    def on_save(self) -> None:
        title = self.title_edit.text().strip()
        media_type = self.media_type_combo.currentText()
        summary = self.summary_edit.text().strip()
        tags = _split_list(self.tags_edit.text())
        references = _split_list(self.references_edit.text())
        images = _split_list(self.images_edit.text())
        published_date = self.published_date_edit.text().strip() or None
        body = self.body_edit.toPlainText()

        try:
            if self.current_id is None:
                article = core.add_article(
                    self.articles_dir,
                    self.conn,
                    title=title,
                    media_type=media_type,
                    summary=summary,
                    tags=tags,
                    references=references,
                    images=images,
                    published_date=published_date,
                    body=body,
                )
            else:
                article = core.edit_article(
                    self.articles_dir,
                    self.conn,
                    self.current_id,
                    title=title,
                    media_type=media_type,
                    summary=summary,
                    tags=tags,
                    references=references,
                    images=images,
                    published_date=published_date,
                    body=body,
                )
        except (storage.ValidationError, core.NotFoundError) as exc:
            QMessageBox.warning(self, "Save failed", str(exc))
            return

        self.refresh_list()
        self.load_article(article)

    def on_delete(self) -> None:
        if self.current_id is None:
            return
        confirm = QMessageBox.question(
            self,
            "Delete article",
            f"Delete article {self.current_id}? This cannot be undone.",
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        try:
            core.delete_article(self.articles_dir, self.conn, self.current_id)
        except core.NotFoundError as exc:
            QMessageBox.warning(self, "Delete failed", str(exc))
            return
        self.on_new()
        self.refresh_list()

    def on_reindex(self) -> None:
        count = core.reindex(self.conn, self.articles_dir)
        QMessageBox.information(self, "Reindex complete", f"Reindexed {count} article(s).")
        self.refresh_list()
