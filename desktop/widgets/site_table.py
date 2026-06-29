from __future__ import annotations

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor

from desktop.models import SiteDTO


class SiteTableModel(QAbstractTableModel):
    HEADERS = ["Name", "Region", "Status", "CPU Capacity", "Storage (TB)", "Score"]

    def __init__(self, sites: list[SiteDTO] | None = None) -> None:
        super().__init__()
        self._sites = sites or []
        self._scores: dict[str, float] = {}

    def update_sites(self, sites: list[SiteDTO], scores: list[tuple[str, float]] | None = None,) -> None:
        self.beginResetModel()
        self._sites = sites
        self._scores = dict(scores) if scores else {}
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._sites)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self.HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return str(section + 1)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        site = self._sites[index.row()]
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:
                return site.name
            if column == 1:
                return site.region
            if column == 2:
                return site.status
            if column == 3:
                return f"{site.cpu_capacity:,}"
            if column == 4:
                return f"{site.storage_tb:,.1f}"
            if column == 5:
                sc = self._scores.get(site.name)
                return f"{sc:.3f}" if sc is not None else "—"


        if role == Qt.ItemDataRole.ForegroundRole:
            if column == 2:  # Status column
                if site.status == "offline":
                    return QColor("red")
                if site.status == "degraded":
                    return QColor("darkorange")
                if site.status == "online":
                    return QColor("darkgreen")
            if column == 5:
                sc = self._scores.get(site.name)
                if sc is not None and sc < 0:
                    return QColor("red")

        return None

    def site_at_row(self, row: int) -> SiteDTO:
        return self._sites[row]