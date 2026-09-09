import app.models  # noqa: E402, F401 # pyright: ignore[reportUnusedImport]
from app.db.base import Base

print(Base.metadata.tables.keys())
