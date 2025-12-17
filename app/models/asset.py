from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    ticker: Mapped[str] = mapped_column(
        String, nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id"),
        nullable=False
    )

    portfolio: Mapped["Portfolio"] = relationship(
        back_populates="assets"
    )