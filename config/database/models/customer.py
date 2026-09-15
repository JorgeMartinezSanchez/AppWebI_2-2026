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
