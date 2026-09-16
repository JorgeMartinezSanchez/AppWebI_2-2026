import uuid
from datetime import datetime, time
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String, Time, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(100))
    phone_number: Mapped[str | None] = mapped_column(String(15))
    modified_at: Mapped[datetime | None] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    orders: Mapped[list["Order"]] = relationship(back_populates="customer")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="customer")
    customer_orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="customer")


class Employee(Base):
    __tablename__ = "employee"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(100))
    phone_number: Mapped[str | None] = mapped_column(String(15))
    employee_role: Mapped[str | None] = mapped_column(String(50))
    shift_start: Mapped[time] = mapped_column(Time, nullable=False)
    shift_end: Mapped[time] = mapped_column(Time, nullable=False)
    available: Mapped[bool | None] = mapped_column()
    modified_at: Mapped[datetime | None] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))


# Nombrada RestaurantTable para no chocar con sqlalchemy.Table
class RestaurantTable(Base):
    __tablename__ = "tables"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    table_number: Mapped[str | None] = mapped_column(String(10))
    capacity: Mapped[int | None] = mapped_column(Integer)
    occupied: Mapped[bool | None] = mapped_column()
    modified_at: Mapped[datetime | None] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    orders: Mapped[list["Order"]] = relationship(back_populates="table")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="table")


# "order" es palabra reservada en SQL; SQLAlchemy la cita automáticamente
class Order(Base):
    __tablename__ = "order"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.customer.id"), nullable=False)
    table_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.tables.id"), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    order_date: Mapped[datetime] = mapped_column(nullable=False)
    modified_at: Mapped[datetime | None] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    customer: Mapped["Customer"] = relationship(back_populates="orders")
    table: Mapped["RestaurantTable"] = relationship(back_populates="orders")
    order_foods: Mapped[list["OrderFood"]] = relationship(back_populates="order")
    customer_orders: Mapped[list["CustomerOrder"]] = relationship(back_populates="order")


class Booking(Base):
    __tablename__ = "booking"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.customer.id"), nullable=False)
    table_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.tables.id"), nullable=False)
    booking_date: Mapped[datetime] = mapped_column(nullable=False)
    checkin_date: Mapped[datetime | None] = mapped_column()
    booking_status: Mapped[str] = mapped_column(String(20), nullable=False)
    modified_at: Mapped[datetime | None] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    customer: Mapped["Customer"] = relationship(back_populates="bookings")
    table: Mapped["RestaurantTable"] = relationship(back_populates="bookings")


class FoodCategory(Base):
    __tablename__ = "food_category"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str | None] = mapped_column(String(100))
    modified_at: Mapped[datetime | None] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    foods: Mapped[list["Food"]] = relationship(back_populates="category")


class Food(Base):
    __tablename__ = "food"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    food_category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.food_category.id"), nullable=False)
    name: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(255))
    price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    modified_at: Mapped[datetime | None] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    category: Mapped["FoodCategory"] = relationship(back_populates="foods")
    order_foods: Mapped[list["OrderFood"]] = relationship(back_populates="food")


class OrderFood(Base):
    __tablename__ = "order_food"
    __table_args__ = {"schema": "content"}

    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.order.id"), primary_key=True)
    food_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.food.id"), primary_key=True)

    order: Mapped["Order"] = relationship(back_populates="order_foods")
    food: Mapped["Food"] = relationship(back_populates="order_foods")


class CustomerOrder(Base):
    __tablename__ = "customer_order"
    __table_args__ = {"schema": "content"}

    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.order.id"), primary_key=True)
    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.customer.id"), primary_key=True)

    order: Mapped["Order"] = relationship(back_populates="customer_orders")
    customer: Mapped["Customer"] = relationship(back_populates="customer_orders")