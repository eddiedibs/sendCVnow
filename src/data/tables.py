from . import constants as const

from sqlalchemy.dialects.postgresql import JSONB  # Use JSON for MySQL or other databases
from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint, MetaData, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

#### DATABASE MODELS ####
database_url = const.DATABASE_URL
engine = create_engine(database_url, echo=True, implicit_returning=True)

DeclarativeBaseIns = declarative_base()
DeclarativeBaseIns.metadata.bind = engine
declarative_base_metadata = DeclarativeBaseIns.metadata

# Users
class User(DeclarativeBaseIns):
   __tablename__ = 'users'

   id = Column(Integer, primary_key=True, index=True)
   cv_name_id = Column(String)
   firstName = Column(String)
   lastName = Column(String)
   username = Column(String, unique=True)
   email = Column(String, unique=True)
   phoneNumber = Column(String, unique=True)
   country = Column(String)
   hashed_password = Column(String)
   userType = Column(String)
   isActive = Column(Boolean, default=True)
   session = relationship("AiRequest", back_populates="user", uselist=False)

class AiRequest(DeclarativeBaseIns):
   __tablename__ = 'ai_requests'

   id = Column(Integer, primary_key=True, index=True)
   ai_request = Column(String)
   userId = Column(Integer, ForeignKey("users.id"), unique=True)
   user = relationship("User", back_populates="session", uselist=False)