from django.db import models

from sites.models import Site


class RSE(models.Model):
    """
    Rucio Storage Element — a named storage resource attached to a computing site.

    Mirrors the essential subset of fields that the real CRIC RSE catalogue exposes.
    The FK to Site enforces that every RSE belongs to a registered site.
    """

    PROTOCOL_CHOICES = [
        ("davs",    "WebDAV/TLS"),
        ("srm",     "SRM"),
        ("gsiftp",  "GridFTP"),
        ("xrootd",  "XRootD"),
        ("posix",   "POSIX/local"),
    ]

    name: models.CharField = models.CharField(
        max_length=200, 
        unique=True,
        help_text="Rucio RSE name, e.g. CERN-PROD_DATADISK"
    )

    site: models.ForeignKey = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="rses",
        help_text="Parent computing site",
    )
    
    protocol: models.CharField = models.CharField(
        max_length=20, 
        choices=PROTOCOL_CHOICES,
        default="davs"
    )

    deterministic: models.BooleanField = models.BooleanField(
        default=True,
        help_text="Whether LFN→PFN mapping is deterministic",
    )
    
    free_tb: models.FloatField = models.FloatField(default=0.0, help_text="Free space in TB")
    used_tb: models.FloatField = models.FloatField(default=0.0, help_text="Used space in TB")
    enabled: models.BooleanField = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "RSE"
        verbose_name_plural = "RSEs"

    def __str__(self) -> str:
        return self.name

    @property
    def total_tb(self) -> float:
        return self.free_tb + self.used_tb

    @property
    def utilisation_pct(self) -> float:
        """Percentage of storage used (0–100). Returns 0 if total is zero."""
        total = self.total_tb
        return round(self.used_tb / total * 100, 1) if total else 0.0