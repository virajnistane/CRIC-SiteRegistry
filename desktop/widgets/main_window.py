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
    QTabWidget
)
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtWidgets import QLineEdit

from desktop.api_client import SiteApiClient
from desktop.models import SiteDTO
from desktop.widgets.site_table import SiteTableModel
from desktop.widgets.status_panel import StatusPanel
from desktop.widgets.site_detail import SiteDetailDialog
from desktop.scorer import rank_sites as cpp_rank_sites

from desktop.rse_client import RseApiClient
from desktop.rse_models import RseDTO
from desktop.widgets.rse_table import RseTableModel
from desktop.widgets.rse_detail import RseDetailDialog as RseDialog

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


        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Filter by name, region, or status")

        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.table_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1)
        self.table_view.setModel(self.proxy_model)
        self.search_box.textChanged.connect(self.proxy_model.setFilterFixedString)

        self.status_label = QLabel("Ready")

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addWidget(self.create_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addStretch()
        left_layout.addWidget(self.search_box)
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

        # RSE tab widgets
        self.rse_api         = RseApiClient()
        self.rse_table_model = RseTableModel([])

        self.rse_table_view = QTableView()
        self.rse_table_view.setModel(self.rse_table_model)
        self.rse_table_view.doubleClicked.connect(self.on_rse_double_clicked)

        self.rse_refresh_btn = QPushButton("Refresh RSEs")
        self.rse_refresh_btn.clicked.connect(self.on_rse_refresh_clicked)
        self.rse_create_btn  = QPushButton("Create RSE")
        self.rse_create_btn.clicked.connect(self.on_rse_create_clicked)
        self.rse_delete_btn  = QPushButton("Delete RSE")
        self.rse_delete_btn.clicked.connect(self.on_rse_delete_clicked)

        self.rse_status_label = QLabel("RSEs not loaded")

        rse_btns = QHBoxLayout()
        rse_btns.addWidget(self.rse_refresh_btn)
        rse_btns.addWidget(self.rse_create_btn)
        rse_btns.addWidget(self.rse_delete_btn)
        rse_btns.addStretch()

        rse_panel = QWidget()
        rse_layout = QVBoxLayout(rse_panel)
        rse_layout.addLayout(rse_btns)
        rse_layout.addWidget(self.rse_table_view)
        rse_layout.addWidget(self.rse_status_label)

        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(splitter, "Sites")   # existing splitter becomes tab 0
        tabs.addTab(rse_panel, "RSEs")   # new RSE panel is tab 1

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(tabs)
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

        # Run C++ scorer (falls back to Python if .so not compiled)
        scores = cpp_rank_sites(sites)

        self.table_model.update_sites(sites, scores)
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


    def on_rse_refresh_clicked(self, _=False) -> None:
        self._track_task(self.load_rses())

    def on_rse_create_clicked(self, _=False) -> None:
        self._track_task(self.create_rse())

    def on_rse_delete_clicked(self, _=False) -> None:
        self._track_task(self.delete_selected_rse())

    def on_rse_double_clicked(self, index: QModelIndex) -> None:
        self._track_task(self.open_selected_rse(index))

    async def load_rses(self) -> None:
        self.rse_status_label.setText("Loading RSEs...")
        try:
            rses = await self.rse_api.list_rses()
        except Exception as exc:
            QMessageBox.critical(self, "RSE API Error", str(exc))
            self.rse_status_label.setText("Load failed")
            return
        self.rse_table_model.update_rses(rses)
        self.rse_status_label.setText(f"Loaded {len(rses)} RSEs")

    async def open_selected_rse(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        rse = self.rse_table_model.rse_at_row(index.row())
        dialog = RseDialog(rse, self)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        try:
            await self.rse_api.update_rse(rse.id, dialog.payload())
        except Exception as exc:
            QMessageBox.critical(self, "RSE Update Error", str(exc))
            return
        await self.load_rses()

    async def create_rse(self) -> None:
        template = RseDTO(id=0, name="", site=1, site_name="",
                        protocol="davs", deterministic=True,
                        free_tb=0.0, used_tb=0.0,
                        total_tb=0.0, utilisation_pct=0.0, enabled=True)
        dialog = RseDialog(template, self)
        dialog.setWindowTitle("Create RSE")
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        try:
            await self.rse_api.create_rse(dialog.payload())
        except Exception as exc:
            QMessageBox.critical(self, "RSE Create Error", str(exc))
            return
        await self.load_rses()

    async def delete_selected_rse(self) -> None:
        index = self.rse_table_view.currentIndex()
        if not index.isValid():
            QMessageBox.information(self, "Delete RSE", "Select an RSE to delete.")
            return
        rse = self.rse_table_model.rse_at_row(index.row())
        confirm = QMessageBox.question(
            self, "Delete RSE",
            f"Delete '{rse.name}'? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        try:
            await self.rse_api.delete_rse(rse.id)
        except Exception as exc:
            QMessageBox.critical(self, "RSE Delete Error", str(exc))
            return
        await self.load_rses()