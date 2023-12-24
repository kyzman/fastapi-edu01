from datetime import datetime

from sqlalchemy import Integer, String, func, TIMESTAMP
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped

from datebase import Base


class Operation(Base):
    __tablename__ = "operation"
    id = mapped_column(Integer, primary_key=True)
    quantity: Mapped[str] = mapped_column(String)
    figi: Mapped[str] = mapped_column(String)
    instrument_type: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP)
    type: Mapped[str] = mapped_column(String)

