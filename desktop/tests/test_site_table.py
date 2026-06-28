from desktop.models import SiteDTO
from desktop.widgets.site_table import SiteTableModel


def test_site_table_model_row_and_column_counts():
    sites = [
        SiteDTO(1, "CERN-T0", "Geneva", "online", 25000, 8200.0),
        SiteDTO(2, "PIC", "Spain", "offline", 9000, 2800.0),
    ]
    model = SiteTableModel(sites)

    assert model.rowCount() == 2
    assert model.columnCount() == 5