# Documentación del Producto Construido – Sprint 2 (Completo)

## Información General
- **Sprint:** 2
- **Historias de Usuario implementadas:** HU3 – Carrito de Compras y Pasarela de Pagos; HU4 – Panel de Gestión de Stock y Precios.
- **Objetivo:** Dotar a la plataforma de un carrito de compras funcional con checkout simulado y un panel de administración que permita a los administradores mantener actualizado el catálogo de productos y precios.
- **Fecha:** 29/04/2026 – 02/05/2026 (primera mitad) y 03/05/2026 – 05/05/2026 (segunda mitad) según planificación.
- **Equipo:** Robert Cerón, David Solís, Juan Castro

## 1. Sprint Backlog (Completo)

| Id | Como...      | Necesito...                                | Para...                                           | Prioridad | Sprint | Estado      |
|----|--------------|--------------------------------------------|---------------------------------------------------|-----------|--------|-------------|
| 3  | Administrador| Gestionar el carrito de compras y pago     | Finalizar la adquisición de productos mediante un flujo de pago seguro | Alta      | 2      | Completada  |
| 4  | Administrador| Acceder al panel de administración de inventario | Mantener actualizada la base de datos de productos y precios | Media     | 2      | Completada  |

## 2. Historias de Usuario Detalladas

### HU3 – Carrito de Compras y Pasarela de Pagos

**Código:** HU03N  
**Título:** Carrito de Compras y Pasarela de Pagos  
**Como:** Administrador (o cliente autenticado)  
**Necesito:** Un sistema de selección de productos y un checkout seguro  
**Para:** Consolidar mis compras y generar una orden de pedido  

#### Criterios de Aceptación
- El carrito debe permitir agregar productos desde el catálogo con un solo clic.
- Se debe visualizar una lista de ítems con título, precio unitario, cantidad (editable) y subtotal.
- El sistema debe calcular automáticamente subtotal, impuesto (13%) y total.
- La pasarela de pago simulada debe solicitar nombre del titular y número de tarjeta, validar que no estén vacíos y simular la confirmación.
- Al confirmar el pago, se generará un pedido con ID único, fecha, cliente, ítems y total, guardado en `data/pedidos.json`.
- El carrito se vacía después de una compra exitosa.
- Debe ser posible modificar cantidades y eliminar productos del carrito.

### HU4 – Panel de Gestión de Stock y Precios

**Código:** HU04N  
**Título:** Panel de Gestión de Stock y Precios  
**Como:** Administrador  
**Necesito:** Una interfaz para añadir, editar o eliminar productos  
**Para:** Reflejar la disponibilidad real de la librería y actualizar precios  

#### Criterios de Aceptación
- Solo usuarios con rol Admin pueden acceder al panel.
- El panel lista todos los productos con ID, título, autor, categoría, precio y ruta de portada.
- Permite agregar un nuevo producto (título, autor, categoría, precio, portada) mediante un formulario.
- Permite editar los datos de un producto existente.
- Permite eliminar un producto.
- Todos los cambios se guardan inmediatamente en `data/productos.json` y actualizan el catálogo público.

## 3. Arquitectura y Módulos Implementados

Se utilizó el patrón MVC con PySide6 y persistencia en archivos JSON.

### 3.1 Módulos del Carrito y Pagos (HU3)

**Modelo:** `src/models/carrito_model.py`
- **Clase `ItemCarrito`**: título, precio, cantidad, subtotal.
- **Clase `Carrito`**: agrega, elimina, actualiza cantidades, calcula total, impuesto y total con impuesto; vaciar, verificar vacío.
- **Clase `PedidoModel`**: carga/guarda pedidos desde `data/pedidos.json`. Método `crear_pedido(cliente, carrito)` que genera un pedido con ID, fecha, cliente, ítems y total. Método `obtener_pedidos_cliente(cliente)`.

**Vista:** `src/views/carrito_view.py`
- Ventana independiente con tabla de productos (título, precio, cantidad con `QSpinBox`, subtotal).
- Sección de resumen de subtotal, impuesto y total.
- Botones: Seguir Comprando, Actualizar, Eliminar Seleccionado, Finalizar Compra.
- Grupo de pago (`QGroupBox`) oculto inicialmente, con campos para titular y número de tarjeta, y botón Confirmar Pago.
- Métodos: `cargar_items()`, `obtener_cantidades_actualizadas()`, `mostrar_seccion_pago()`, `actualizar_totales()`.

**Controlador:** `src/controllers/carrito_controller.py`
- Conecta la vista con el modelo de carrito y pedidos.
- Métodos: `actualizar_vista()`, `actualizar_cantidades()`, `eliminar_seleccionado()`, `mostrar_checkout()`, `procesar_pago()`, `agregar_al_carrito()`.

### 3.2 Módulos del Panel de Administración (HU4)

**Modelo:** `src/models/producto_model.py` (extendido)
- Métodos CRUD añadidos:
  - `guardar_productos()`: Persiste la lista en JSON.
  - `agregar_producto(...)`: Genera nuevo ID y guarda.
  - `actualizar_producto(id, ...)`: Modifica un producto existente.
  - `eliminar_producto(id)`: Elimina un producto por ID.

**Vista:** `src/views/admin_productos_view.py`
- Ventana con `QTableWidget` de 6 columnas: ID, Título, Autor, Categoría, Precio, Portada.
- Botones: Nuevo, Editar, Eliminar, Refrescar, Cerrar.
- `ProductoDialog` (QDialog) con formulario para agregar/editar (título, autor, categoría, precio con QDoubleSpinBox, ruta de portada).
- Métodos: `cargar_productos()`, `obtener_producto_seleccionado()`.

**Controlador:** `src/controllers/admin_productos_controller.py`
- Lógica para CRUD conectando la vista y el modelo.
- Recibe un callback `refresh_callback` para actualizar el catálogo tras cada operación.
- Métodos: `nuevo_producto()`, `editar_producto()`, `eliminar_producto()`, `cargar_tabla()`.

### 3.3 Integración en Catálogo y Flujo Principal

**Modificaciones en `catalogo_view.py`:**
- Se añadió botón "🛒 Carrito" en la barra de herramientas.
- Se añadió botón "Panel Admin" (oculto inicialmente, mostrado por el controlador si el usuario es admin).
- En `mostrar_productos` se agregó parámetro opcional `on_agregar`. Cada producto tiene un botón "Agregar" conectado al callback del carrito.

**Modificaciones en `catalogo_controller.py`:**
- Constructor recibe parámetros `carrito_ctrl`, `admin_ctrl` y `es_admin`.
- Se conecta el botón "Panel Admin" al método `abrir_admin()` que muestra la ventana de administración.
- Búsquedas e inicialización pasan `self.carrito_ctrl.agregar_al_carrito` como callback de "Agregar".

**Actualización de `main.py`:**
- Tras el login, se instancian `Carrito`, `PedidoModel`, `CarritoView`, `CarritoController`.
- Se comparte `ProductoModel` con el catálogo y el panel admin.
- Si el rol es Admin, se instancia `AdminProductosView` y `AdminProductosController`, y se pasa al constructor del catálogo.
- Se asigna el callback `catalogo_ctrl.mostrar_todos` al panel admin para refrescar el catálogo tras cambios.

## 4. Diagrama de Clases y Procesos

- **Diagrama de clases (HU3):** Referencia `media/image6.png`. Muestra las nuevas entidades (`ItemCarrito`, `Carrito`, `Pedido`, `PedidoModel`) y sus relaciones.
- **Diagrama de procesos (HU3):** Referencia `media/image7.png`. Flujo: seleccionar producto → agregar al carrito → abrir carrito → gestionar ítems → checkout → pago simulado → pedido registrado.
- **Diagrama de clases (HU4):** Referencia `media/image6.png` (misma plantilla, extendida con `AdminProductosView`, `AdminProductosController` y sus relaciones con `ProductoModel`).
- **Diagrama de procesos (HU4):** Administrador hace clic en "Panel Admin" → se abre la ventana con la tabla de productos → Agregar/Editar/Eliminar → cambios guardados en `productos.json` → catálogo público se refresca.

## 5. Persistencia de Datos

- **`data/pedidos.json`**: Creado para HU3. Contiene array de pedidos con:
  ```json
  {
    "id": 1,
    "fecha": "2026-04-29",
    "cliente": "admin",
    "items": [
      {"titulo": "Cien años de soledad", "cantidad": 2, "precio_unitario": 19.99}
    ],
    "total": 45.17,
    "descuento": 0.0,
    "estado": "Pendiente"
  }
  ```
- **`data/productos.json`**: Utilizado por el panel admin para modificar el catálogo en tiempo real. Estructura sin cambios respecto a Sprint 1.
- **`data/database.json`** y **`data/pedidos.json`** mantienen su forma anterior.