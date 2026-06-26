from __future__ import annotations

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QListWidget, QListWidgetItem

from desktop.models import SiteDTO


class StatusPanel(QListWidget):
    def update_from_sites(self, sites: list[SiteDTO]) -> None:
        self.clear()
        for site in sites:
            if site.status == "online":
                continue

            item = QListWidgetItem(f"{site.name} ({site.region}) — {site.status}")
            if site.status == "offline":
                item.setForeground(QColor("red"))
            elif site.status == "degraded":
                item.setForeground(QColor("darkorange"))
            self.addItem(item)