# desktop/tests/test_rse_table.py
import pytest
from desktop.rse_models import RseDTO
from desktop.widgets.rse_table import RseTableModel


def _make_rse(**kwargs) -> RseDTO:
    defaults = dict(
        id=1, name="TEST_RSE", site=1, site_name="CERN-PROD",
        protocol="davs", deterministic=True,
        free_tb=300.0, used_tb=700.0,
        total_tb=1000.0, utilisation_pct=70.0,
        enabled=True,
    )
    defaults.update(kwargs)
    return RseDTO(**defaults) # type: ignore


def test_row_and_column_count(qtbot):
    rses  = [_make_rse(id=i, name=f"RSE-{i}") for i in range(5)]
    model = RseTableModel(rses)
    assert model.rowCount()    == 5
    assert model.columnCount() == 8


def test_display_data(qtbot):
    from PyQt6.QtCore import Qt, QModelIndex
    rse   = _make_rse()
    model = RseTableModel([rse])
    idx   = model.index(0, 1)   # Name column
    assert model.data(idx, Qt.ItemDataRole.DisplayRole) == "TEST_RSE"


def test_update_rses_resets_model(qtbot):
    model = RseTableModel([_make_rse(id=1, name="A")])
    model.update_rses([_make_rse(id=2, name="B"), _make_rse(id=3, name="C")])
    assert model.rowCount() == 2


def test_disabled_rse_colour(qtbot):
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QColor
    rse   = _make_rse(enabled=False)
    model = RseTableModel([rse])
    idx   = model.index(0, 7)   # Enabled column
    colour = model.data(idx, Qt.ItemDataRole.ForegroundRole)
    assert colour == QColor("red")