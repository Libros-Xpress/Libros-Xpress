# Resultado de las Pruebas Automatizadas (Robot GUI v2.0.0)

## Fecha
12 de mayo de 2026

## Robot utilizado
`tests/test_robot_gui_v2.py` (pytest-qt)

## Resultado global
4 de 4 pruebas pasaron correctamente.

---

### 1. `test_flujo_admin` – ✅ PASÓ
- **Objetivo:** Verificar que un administrador puede iniciar sesión y acceder a sus funciones exclusivas.
- **Resultado:** El usuario `admin` inicia sesión correctamente. El catálogo muestra los botones **"Panel Admin"** y **"Venta Física"**.

### 2. `test_flujo_cliente` – ✅ PASÓ
- **Objetivo:** Verificar que un cliente NO tiene acceso a funciones de administrador, pero sí puede comprar.
- **Resultado:** El usuario `cliente` inicia sesión. Los botones **"Panel Admin"** y **"Venta Física"** NO están visibles. El cliente agrega un producto al carrito y puede verlo.

### 3. `test_carrito_y_cupon` – ✅ PASÓ
- **Objetivo:** Verificar el carrito de compras y la aplicación de cupones de descuento.
- **Resultado:** Se agregan 2 productos al carrito. El código `DESC10` se aplica correctamente y el total se reduce (de $45.20 a $40.68).

### 4. `test_historial` – ✅ PASÓ
- **Objetivo:** Verificar que los pedidos quedan registrados y asociados al usuario.
- **Resultado:** Se crea un pedido de prueba para el usuario `admin` y se confirma que aparece en el historial.

---

## Observaciones
- Todas las ventanas (login, catálogo, carrito) se abren y cierran automáticamente.
- Los mensajes de éxito/error se imprimen en consola para no bloquear la automatización.
- El robot cubre los flujos principales de administrador y cliente.

## Autoría
Robert Cerón