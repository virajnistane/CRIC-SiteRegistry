from __future__ import annotations

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
)

from desktop.models import SiteDTO


class SiteDetailDialog(QDialog):
    def __init__(self, site: SiteDTO, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Edit Site: {site.name}")
        self.site = site

        self.name_edit = QLineEdit(site.name)
        self.region_edit = QLineEdit(site.region)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["online", "offline", "degraded"])
        self.status_combo.setCurrentText(site.status)

        self.cpu_spin = QSpinBox()
        self.cpu_spin.setMaximum(10_000_000)
        self.cpu_spin.setValue(site.cpu_capacity)

        self.storage_spin = QDoubleSpinBox()
        self.storage_spin.setMaximum(1_000_000.0)
        self.storage_spin.setDecimals(1)
        self.storage_spin.setValue(site.storage_tb)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QFormLayout(self)
        layout.addRow("Name", self.name_edit)
        layout.addRow("Region", self.region_edit)
        layout.addRow("Status", self.status_combo)
        layout.addRow("CPU Capacity", self.cpu_spin)
        layout.addRow("Storage (TB)", self.storage_spin)
        layout.addWidget(buttons)

    def payload(self) -> dict:
        return {
            "name": self.name_edit.text().strip(),
            "region": self.region_edit.text().strip(),
            "status": self.status_combo.currentText(),
            "cpu_capacity": self.cpu_spin.value(),
            "storage_tb": self.storage_spin.value(),
        }