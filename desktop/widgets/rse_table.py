# desktop/widgets/rse_table.py
from __future__ import annotations

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt

from desktop.rse_models import RseDTO

_HEADERS = ["ID", "Name", "Site", "Protocol", "Free TB", "Used TB", "Util %", "Enabled"]


class RseTableModel(QAbstractTableModel):
    def __init__(self, rses: list[RseDTO]) -> None:
        super().__init__()
        self._rses = rses

    # ------------------------------------------------------------------
    # QAbstractTableModel interface
    # ------------------------------------------------------------------

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._rses)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(_HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return _HEADERS[section]
        return None

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        rse = self._rses[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            match col:
                case 0: return rse.id
                case 1: return rse.name
                case 2: return rse.site_name
                case 3: return rse.protocol
                case 4: return f"{rse.free_tb:.1f}"
                case 5: return f"{rse.used_tb:.1f}"
                case 6: return f"{rse.utilisation_pct:.1f}%"
                case 7: return "Yes" if rse.enabled else "No"

        if role == Qt.ItemDataRole.ForegroundRole:
            from PyQt6.QtGui import QColor
            if col == 7 and not rse.enabled:
                return QColor("red")
            if col == 6 and rse.utilisation_pct > 90:
                return QColor("orange")

        return None

    # ------------------------------------------------------------------
    # Helpers called by the window
    # ------------------------------------------------------------------

    def update_rses(self, rses: list[RseDTO]) -> None:
        self.beginResetModel()
        self._rses = rses
        self.endResetModel()

    def rse_at_row(self, row: int) -> RseDTO:
        return self._rses[row]