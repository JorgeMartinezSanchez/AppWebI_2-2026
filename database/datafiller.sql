-- Configurar el search_path para no escribir "content." en cada inserción
SET search_path TO content, public;
-- ============================================================================
-- 1. INSERTAR CLIENTES (CUSTOMER)
-- ============================================================================
INSERT INTO customer (id, first_name, last_name, email, phone_number) VALUES
('a1111111-1111-1111-1111-111111111111', 'Jorge', 'Mendoza', 'jorge.mendoza@email.com', '5551234567'),
('a2222222-2222-2222-2222-222222222222', 'Maria', 'Santos', 'maria.santos@email.com', '5559876543'),
('a3333333-3333-3333-3333-333333333333', 'Carlos', 'Lopez', 'carlos.lopez@email.com', '5555554433');

-- ============================================================================
-- 2. INSERTAR EMPLEADOS (EMPLOYEE)
-- ============================================================================
INSERT INTO employee (id, first_name, last_name, email, phone_number, employee_role, shift_start, shift_end, available) VALUES
('b1111111-1111-1111-1111-111111111111', 'Ana', 'Gomez', 'ana.gomez@restaurant.com', '5551112233', 'Mesero', '08:00:00', '16:00:00', true),
('b2222222-2222-2222-2222-222222222222', 'Luis', 'Torres', 'luis.torres@restaurant.com', '5554445566', 'Chef', '12:00:00', '22:00:00', true);

-- ============================================================================
-- 3. INSERTAR MESAS (TABLES)
-- ============================================================================
INSERT INTO tables (id, table_number, capacity, occupied) VALUES
('c1111111-1111-1111-1111-111111111111', 'Mesa 1', 2, false),
('c2222222-2222-2222-2222-222222222222', 'Mesa 2', 4, true),
('c3333333-3333-3333-3333-333333333333', 'Mesa 3', 6, false);

-- ============================================================================
-- 4. INSERTAR MENÚ / COMIDA (FOOD)
-- ============================================================================
INSERT INTO food (id, name, description, price, category) VALUES
('d1111111-1111-1111-1111-111111111111', 'Hamburguesa Especial', 'Carne res 200g, queso, tocino y papas fritas', 12.50, 'Plato Fuerte'),
('d2222222-2222-2222-2222-222222222222', 'Pizza Pepperoni', 'Masa artesanal con salsa de tomate y abundante pepperoni', 15.00, 'Plato Fuerte'),
('d3333333-3333-3333-3333-333333333333', 'Ensalada Cesar', 'Lechuga fresca, crotones, queso parmesano y aderezo', 8.50, 'Entrada'),
('d4444444-4444-4444-4444-444444444444', 'Refresco de la Casa', 'Bebida fría natural de temporada', 3.00, 'Bebidas');

-- ============================================================================
-- 5. INSERTAR ORDENES (ORDER)
-- ============================================================================
INSERT INTO "order" (id, customer_id, table_id, total_amount, order_date) VALUES
('e1111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111', 'c1111111-1111-1111-1111-111111111111', 15.50, NOW()),
('e2222222-2222-2222-2222-222222222222', 'a2222222-2222-2222-2222-222222222222', 'c2222222-2222-2222-2222-222222222222', 23.50, NOW());

-- ============================================================================
-- 6. INSERTAR RESERVACIONES (BOOKING)
-- ============================================================================
INSERT INTO booking (id, customer_id, table_id, booking_date, checkin_date, booking_status) VALUES
('f1111111-1111-1111-1111-111111111111', 'a3333333-3333-3333-3333-333333333333', 'c3333333-3333-3333-3333-333333333333', NOW() + INTERVAL '1 day', NULL, 'Confirmada');

-- ============================================================================
-- 7. INSERTAR DETALLE DE COMIDA POR ORDEN (ORDER_FOOD)
-- ============================================================================
INSERT INTO order_food (order_id, food_id) VALUES
-- Orden 1: Hamburguesa Especial + Refresco
('e1111111-1111-1111-1111-111111111111', 'd1111111-1111-1111-1111-111111111111'),
('e1111111-1111-1111-1111-111111111111', 'd4444444-4444-4444-4444-444444444444'),
-- Orden 2: Pizza Pepperoni + Ensalada Cesar
('e2222222-2222-2222-2222-222222222222', 'd2222222-2222-2222-2222-222222222222'),
('e2222222-2222-2222-2222-222222222222', 'd3333333-3333-3333-3333-333333333333');

-- ============================================================================
-- 8. RELACIONAR CLIENTES CON SUS ORDENES (CUSTOMER_ORDER)
-- ============================================================================
INSERT INTO customer_order (order_id, customer_id) VALUES
('e1111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111'),
('e2222222-2222-2222-2222-222222222222', 'a2222222-2222-2222-2222-222222222222');