from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, text, func, Boolean

from sqlalchemy.orm import mapped_column, Mapped

from datebase import Base, metadata

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

# user = Table(
#     "user",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, nullable=False),
#     Column("username", String, nullable=False),
#     Column("registered_at", TIMESTAMP, default=datetime.utcnow),
#     Column("role_id", Integer, ForeignKey(role.c.id)),
#     Column("hashed_password", String, nullable=False),
#     Column("is_active", Boolean, default=False, nullable=False),
#     Column("is_superuser", Boolean, default=False, nullable=False),
#     Column("is_verified", Boolean, default=False, nullable=False),
# )


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    role_id = mapped_column(ForeignKey(role.c.id))
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )



# class Base(DeclarativeBase):
#     pass
#
#
# class Roles(Base):
#     __tablename__ = "roles"
#     id = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     permissions: Mapped[JSON] = mapped_column(JSON)
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = mapped_column(Integer, primary_key=True)
#     email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
#     username: Mapped[str] = mapped_column(String, nullable=False)
#     password: Mapped[str] = mapped_column(String, nullable=False)
#     registered_at: Mapped[datetime] = mapped_column(insert_default=func.now())
#     role_id = mapped_column(ForeignKey("roles.id"))


# class Roles(Base):
#     __tablename__ = "roles"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     permissions = Column(JSON, nullable=False)
#
#
# class Users(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False)
#     username = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     registered_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
#     role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"))
