from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player: Mapped[str] = mapped_column(String(160), index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    set_name: Mapped[str] = mapped_column(String(200), index=True)
    card_number: Mapped[str] = mapped_column(String(80), index=True)
    parallel: Mapped[str | None] = mapped_column(String(160), nullable=True)
    rookie: Mapped[bool] = mapped_column(Boolean, default=False)
    autograph: Mapped[bool] = mapped_column(Boolean, default=False)
    memorabilia: Mapped[bool] = mapped_column(Boolean, default=False)
    serial_total: Mapped[int | None] = mapped_column(Integer, nullable=True)

    sales = relationship("Sale", back_populates="card", cascade="all, delete-orphan")

class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), index=True)
    sale_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    marketplace: Mapped[str] = mapped_column(String(100), index=True)
    grade: Mapped[str | None] = mapped_column(String(50), nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=True)
    seller: Mapped[str | None] = mapped_column(String(160), nullable=True)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    card = relationship("Card", back_populates="sales")

class ResearchQueue(Base):
    __tablename__ = "research_queue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"), index=True)
    priority: Mapped[int] = mapped_column(Integer, default=50)
    reason: Mapped[str] = mapped_column(String(240))
    status: Mapped[str] = mapped_column(String(30), default="pending", index=True)
