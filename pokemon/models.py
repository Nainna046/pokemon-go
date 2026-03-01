from pokemon.extensions import db, login_manager
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, func, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime
from flask_login import UserMixin


# ================= USER LOADER =================
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ================= USER =================
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    firstname: Mapped[str] = mapped_column(String(30), nullable=True)
    lastname: Mapped[str] = mapped_column(String(30), nullable=True)
    avatar: Mapped[str] = mapped_column(String(25), nullable=True, default='avatar.png')

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # 🔥 one-to-many
    pokemons: Mapped[List['Pokemon']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User: {self.username}>'


# ================= MANY-TO-MANY TABLE =================
pokedex = Table(
    "pokedex",
    db.metadata,
    Column("type_id", Integer, ForeignKey("type.id"), primary_key=True),
    Column("pokemon_id", Integer, ForeignKey("pokemon.id"), primary_key=True),
)


# ================= TYPE =================
class Type(db.Model):
    __tablename__ = 'type'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    pokemons: Mapped[List['Pokemon']] = relationship(
        back_populates='types',
        secondary=pokedex
    )

    def __repr__(self):
        return f'<Type: {self.name}>'


# ================= POKEMON =================
class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=False)
    weight: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(Text, nullable=False)

    # 🔥 สำคัญ — ใช้ string FK
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # 🔥 relationships
    user: Mapped['User'] = relationship(back_populates='pokemons')

    types: Mapped[List['Type']] = relationship(
        back_populates='pokemons',
        secondary=pokedex
    )

    def __repr__(self):
        return f'<Pokemon: {self.name}>'