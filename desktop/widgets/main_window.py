from __future__ import annotations

import asyncio

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt, QModelIndex

from desktop.api_client import SiteApiClient
from desktop.models import SiteDTO
from desktop.widgets.site_table import SiteTableModel
from desktop.widgets.status_panel import StatusPanel
from desktop.widgets.site_detail import SiteDetailDialog


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("CRIC Site Registry Desktop Client")
        self.resize(1100, 700)

        self.api = SiteApiClient()
        self.table_model = SiteTableModel([])
        self._tasks: set[asyncio.Task] = set()
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.setSortingEnabled(False)
        self.table_view.doubleClicked.connect(self.on_table_double_clicked)

        self.status_panel = StatusPanel()
        self.status_panel.setMinimumWidth(280)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.on_refresh_clicked)
        self.create_button = QPushButton("Create New Site")
        self.create_button.clicked.connect(self.on_create_clicked)
        self.delete_button = QPushButton("Delete Selected Site")
        self.delete_button.clicked.connect(self.on_delete_clicked)

        self.status_label = QLabel("Ready")

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addWidget(self.create_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addStretch()
        left_layout.addLayout(buttons_layout)
        left_layout.addWidget(self.table_view)
        left_layout.addWidget(self.status_label)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Alerts"))
        right_layout.addWidget(self.status_panel)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([800, 300])

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(splitter)
        self.setCentralWidget(container)

    def _track_task(self, coro) -> None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
        task = loop.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    def on_refresh_clicked(self, _checked: bool = False) -> None:
        self._track_task(self.load_sites())

    def on_create_clicked(self, _checked: bool = False) -> None:
        self._track_task(self.create_site())

    def on_delete_clicked(self, _checked: bool = False) -> None:
        self._track_task(self.delete_selected_site())

    def on_table_double_clicked(self, index: QModelIndex) -> None:
        self._track_task(self.open_selected_site(index))

    async def load_sites(self) -> None:
        self.status_label.setText("Loading...")
        try:
            sites = await self.api.list_sites()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "API Error",
                (
                    f"Cannot connect to API at {self.api.base_url}\n\n"
                    f"Details: {exc}\n\n"
                    "Start backend with:\n"
                    "uv run python manage.py runserver 127.0.0.1:8000"
                ),
            )
            self.status_label.setText("Load failed")
            return

        self.table_model.update_sites(sites)
        self.status_panel.update_from_sites(sites)
        self.status_label.setText(f"Loaded {len(sites)} sites")

    async def open_selected_site(self, index: QModelIndex) -> None:
        if not index.isValid():
            return

        site = self.table_model.site_at_row(index.row())
        dialog = SiteDetailDialog(site, self)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        try:
            await self.api.update_site(site.id, dialog.payload())
        except Exception as exc:
            QMessageBox.critical(self, "Update Error", str(exc))
            return

        await self.load_sites()

    async def create_site(self) -> None:
        template_site = SiteDTO(
            id=0,
            name="",
            region="",
            status="online",
            cpu_capacity=0,
            storage_tb=0.0,
        )
        dialog = SiteDetailDialog(template_site, self)
        dialog.setWindowTitle("Create New Site")
        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        try:
            await self.api.create_site(dialog.payload())
        except Exception as exc:
            QMessageBox.critical(self, "Creation Error", str(exc))
            return

        self.status_label.setText("Site created")
        await self.load_sites()

    async def delete_selected_site(self) -> None:
        index = self.table_view.currentIndex()
        if not index.isValid():
            QMessageBox.information(self, "Delete Site", "Select a site to delete.")
            return

        site = self.table_model.site_at_row(index.row())
        confirm = QMessageBox.question(
            self,
            "Delete Site",
            f"Delete '{site.name}'? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            await self.api.delete_site(site.id)
        except Exception as exc:
            QMessageBox.critical(self, "Delete Error", str(exc))
            return

        self.status_label.setText("Site deleted")
        await self.load_sites()