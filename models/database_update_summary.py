from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DatabaseUpdateSummary:
    statistics_loaded: int
    recent_forms_loaded: int
    teams_exported: int
    backup_path: Path | None