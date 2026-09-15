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
