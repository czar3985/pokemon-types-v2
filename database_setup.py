# DATABASE_SETUP.PY creates the database and the tables to be used

import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import create_engine, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


# Description of the table and their columns
class User(Base):
    """User table"""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Category(Base):
    """Pokemon categories table"""

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    @property
    def serialize(self):
        """For JSON API endpoint showing category entries in the database"""

        return {
            'name': self.name,
            'id': self.id
            }


class Type(Base):
    """Pokemon types table"""

    __tablename__ = 'type'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    @property
    def serialize(self):
        """For JSON API endpoint showing the type entries in the database"""

        return {
            'name': self.name,
            'id': self.id
            }


class Move(Base):
    """Pokemon moves table"""

    __tablename__ = 'move'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    @property
    def serialize(self):
        """For JSON API endpoint showing the move entries in the database"""

        return {
            'name': self.name,
            'id': self.id
            }


class Pokemon(Base):
    """Pokemon entries table"""

    __tablename__ = 'pokemon'

    id = Column(Integer, nullable=False, primary_key=True)
    pokedex_id = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    is_mythical = Column(Boolean, nullable=False)
    is_legendary = Column(Boolean, nullable=False)
    evolution_before = Column(Integer, nullable=True)
    evolution_after_list = Column(PickleType, nullable=True)
    type_list = Column(PickleType, nullable=False)
    weakness_list = Column(PickleType, nullable=False)
    move_list = Column(PickleType, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


# Create the database
engine = create_engine('sqlite:///pokemon.db')
Base.metadata.create_all(engine)
