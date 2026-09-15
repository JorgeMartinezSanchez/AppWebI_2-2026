import uuid
from datetime import datetime, time
from decimal import Decimal
 
from sqlalchemy import ForeignKey, Integer, Numeric, String, Time, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
 
 
class Base(DeclarativeBase):
    pass