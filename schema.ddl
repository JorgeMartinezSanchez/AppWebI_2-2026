CREATE DATABASE madyumyum_restaurant_db;

\c madyumyum_restaurant_db;

CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE content.customer (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.employee (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    employee_role VARCHAR(50),
    shift_start TIME NOT NULL,
    shift_end TIME NOT NULL,
    available BOOLEAN,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.tables (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_number VARCHAR(10),
    capacity INT,
    occupied BOOLEAN,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.order (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    table_id UUID NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    order_date TIMESTAMP NOT NULL,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES content.customer(id),
    CONSTRAINT fk_table FOREIGN KEY (table_id) REFERENCES content.tables(id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.booking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    table_id UUID NOT NULL,
    booking_date TIMESTAMP NOT NULL,
    checkin_date TIMESTAMP NULL,
    booking_status VARCHAR(20) NOT NULL,
    CONSTRAINT fk_customer_booking FOREIGN KEY (customer_id) REFERENCES content.customer(id),
    CONSTRAINT fk_table_booking FOREIGN KEY (table_id) REFERENCES content.tables(id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.food_category(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.food(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_category_id UUID NOT NULL,
    name VARCHAR(100),
    description VARCHAR(255),
    price DECIMAL(10, 2),
    CONSTRAINT fk_food_category_booking FOREIGN KEY (food_category_id) REFERENCES content.food_category(id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.order_food(
    order_id UUID NOT NULL,
    food_id UUID NOT NULL,
    PRIMARY KEY (order_id, food_id),
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES content.order(id),
    CONSTRAINT fk_food FOREIGN KEY (food_id) REFERENCES content.food(id)
);

CREATE TABLE content.customer_order(
    order_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    PRIMARY KEY (order_id, customer_id),
    CONSTRAINT fk_order_cust FOREIGN KEY (order_id) REFERENCES content.order(id),
    CONSTRAINT fk_customer_cust FOREIGN KEY (customer_id) REFERENCES content.customer(id)
);


CREATE INDEX idx_customer_name ON content.customer(first_name);
CREATE INDEX idx_food_name ON content.food(name);
CREATE INDEX idx_food_category_name ON content.food_category(name);
CREATE INDEX idx_booking_date ON content.booking(booking_date);