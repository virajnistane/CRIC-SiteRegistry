# desktop/widgets/rse_detail.py
from __future__ import annotations
from typing import Any

from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
)

from desktop.rse_models import RseDTO

_PROTOCOLS = ["davs", "srm", "gsiftp", "xrootd", "posix"]


class RseDetailDialog(QDialog):
    """
    Edit/Create dialog for a single RSE.
    Call dialog.payload() after Accepted to get the dict to POST/PATCH.
    """

    def __init__(self, rse: RseDTO, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"RSE — {rse.name or 'New'}")
        self.resize(420, 300)

        self._name = QLineEdit(rse.name)
        self._site_id = QSpinBox()
        self._site_id.setRange(1, 99_999)
        self._site_id.setValue(rse.site or 1)

        self._protocol = QComboBox()
        self._protocol.addItems(_PROTOCOLS)
        if rse.protocol in _PROTOCOLS:
            self._protocol.setCurrentText(rse.protocol)

        self._deterministic = QCheckBox("Deterministic LFN→PFN mapping")
        self._deterministic.setChecked(rse.deterministic)

        self._free_tb = QDoubleSpinBox()
        self._free_tb.setRange(0, 1_000_000)
        self._free_tb.setDecimals(1)
        self._free_tb.setValue(rse.free_tb)

        self._used_tb = QDoubleSpinBox()
        self._used_tb.setRange(0, 1_000_000)
        self._used_tb.setDecimals(1)
        self._used_tb.setValue(rse.used_tb)

        self._enabled = QCheckBox("Enabled")
        self._enabled.setChecked(rse.enabled)

        form = QFormLayout()
        form.addRow("Name",          self._name)
        form.addRow("Site ID",       self._site_id)
        form.addRow("Protocol",      self._protocol)
        form.addRow("",              self._deterministic)
        form.addRow("Free TB",       self._free_tb)
        form.addRow("Used TB",       self._used_tb)
        form.addRow("",              self._enabled)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def payload(self) -> dict[str, Any]:
        return {
            "name":          self._name.text().strip(),
            "site":          self._site_id.value(),
            "protocol":      self._protocol.currentText(),
            "deterministic": self._deterministic.isChecked(),
            "free_tb":       self._free_tb.value(),
            "used_tb":       self._used_tb.value(),
            "enabled":       self._enabled.isChecked(),
        }