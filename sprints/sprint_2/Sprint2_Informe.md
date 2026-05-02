# Documentación del Producto Construido – Sprint 2 (Primera Mitad)

## Información General
- **Sprint:** 2 (primera mitad)
- **Historias de Usuario implementadas:** HU3 – Carrito de Compras y Pasarela de Pagos
- **Objetivo:** Permitir a los usuarios autenticados agregar productos desde el catálogo a un carrito de compras, gestionar las cantidades, visualizar totales y realizar un pago simulado que genere un pedido persistente.
- **Fecha:** 29/04/2026 – 02/05/2026 (según planificación original)
- **Equipo:** Robert Cerón, David Solís, Juan Castro

## 1. Sprint Backlog (Primera Mitad)

| Id | Como...      | Necesito...                              | Para...                                           | Prioridad | Sprint | Estado      |
|----|--------------|------------------------------------------|---------------------------------------------------|-----------|--------|-------------|
| 3  | Administrador| Gestionar el carrito de compras y pago   | Finalizar la adquisición de productos mediante un flujo de pago seguro | Alta      | 2      | Completada  |

## 2. Historia de Usuario Detallada (HU3)

**Código:** HU03N  
**Título:** Carrito de Compras y Pasarela de Pagos  
**Como:** Administrador (o cliente autenticado)  
**Necesito:** Un sistema de selección de productos y un checkout seguro  
**Para:** Consolidar mis compras y generar una orden de pedido  

### Criterios de Aceptación
- El carrito debe permitir agregar productos desde el catálogo con un solo clic.
- Se debe visualizar una lista de ítems con título, precio unitario, cantidad (editable) y subtotal.
- El sistema debe calcular automáticamente subtotal, impuesto (13%) y total.
- La pasarela de pago simulada debe solicitar nombre del titular y número de tarjeta, validar que no estén vacíos y simular la confirmación.
- Al confirmar el pago, se generará un pedido con ID único, fecha, cliente, ítems y total, guardado en `data/pedidos.json`.
- El carrito se vacía después de una compra exitosa.
- Debe ser posible modificar cantidades y eliminar productos del carrito.

## 3. Arquitectura y Módulos Implementados

Se utilizó el patrón MVC. A continuación se detallan los nuevos componentes y modificaciones.

### 3.1 Modelos (`src/models/carrito_model.py`)
- **Clase `ItemCarrito`**: Representa un producto en el carrito (título, precio, cantidad). Calcula subtotal.
- **Clase `Carrito`**: Almacena en memoria una lista de `ItemCarrito`. Métodos:
  - `agregar_item(titulo, precio, cantidad)`: Agrega un producto o incrementa su cantidad.
  - `eliminar_item(titulo)`: Quita un producto.
  - `actualizar_cantidad(titulo, cantidad)`: Cambia la cantidad; si es 0, elimina.
  - `total()`, `impuesto(tasa)`, `total_con_impuesto()`, `vaciar()`, `esta_vacio()`.
- **Clase `PedidoModel`**: Persiste los pedidos en `data/pedidos.json`. Métodos:
  - `cargar_pedidos()`, `guardar_pedidos()`
  - `crear_pedido(cliente, carrito)`: Crea un nuevo pedido, lo guarda y retorna un diccionario.
  - `obtener_pedidos_cliente(cliente)`: Lista pedidos de un cliente.

### 3.2 Vista (`src/views/carrito_view.py`)
- Ventana independiente (`QMainWindow`) con:
  - Tabla (`QTableWidget`) de 4 columnas: Producto, Precio, Cantidad (con `QSpinBox`), Subtotal.
  - Sección de resumen: subtotal, impuesto (13%), total.
  - Botones: "Seguir Comprando" (cierra ventana), "Actualizar" (recalcula cantidades), "Eliminar Seleccionado", "Finalizar Compra".
  - Grupo de pago (`QGroupBox`) inicialmente oculto que contiene:
    - Campos `QLineEdit` para titular y número de tarjeta.
    - Botón "Confirmar Pago".
  - Métodos clave:
    - `cargar_items(items)`: Llena la tabla con items del carrito.
    - `obtener_cantidades_actualizadas()`: Retorna diccionario {título: cantidad} desde los spinboxes.
    - `mostrar_seccion_pago(mostrar)`: Muestra/oculta el formulario de pago.
    - `mostrar_mensaje()`, `mostrar_error()`: Notificaciones con `QMessageBox`.

### 3.3 Controlador (`src/controllers/carrito_controller.py`)
- Conecta la vista del carrito con el modelo.
- Métodos principales:
  - `actualizar_vista()`: Refresca la tabla y totales.
  - `actualizar_cantidades()`: Lee los spinboxes y actualiza el carrito.
  - `eliminar_seleccionado()`: Elimina el producto seleccionado.
  - `mostrar_checkout()`: Valida que el carrito no esté vacío y muestra el formulario de pago.
  - `procesar_pago()`: Valida datos de pago, llama a `PedidoModel.crear_pedido()`, vacía el carrito y muestra confirmación.
  - `agregar_al_carrito(titulo, precio)`: Recibe desde el catálogo y añade al carrito.

### 3.4 Integración en Catálogo y Flujo Principal

**Modificaciones en `catalogo_view.py`:**
- Se añadió botón "🛒 Carrito" en la barra de herramientas.
- En `mostrar_productos` se agregó un parámetro opcional `on_agregar`. Por cada producto se crea un botón "Agregar" que, si hay callback, se conecta al mismo pasando título y precio.

**Modificaciones en `catalogo_controller.py`:**
- El constructor ahora recibe un parámetro `carrito_ctrl` (instancia de `CarritoController`).
- Se conectó el botón Carrito a un nuevo método `abrir_carrito()` que muestra la ventana del carrito y actualiza su contenido.
- `realizar_busqueda` y `mostrar_todos` pasan el callback `self.carrito_ctrl.agregar_al_carrito` a la vista.

**Actualización de `main.py`:**
- Después de la autenticación exitosa, se instancian `Carrito`, `PedidoModel`, `CarritoView`, `CarritoController`.
- Se pasa el controlador del carrito al constructor de `CatalogoController`.
- Flujo completo: Login → Catálogo (con carrito integrado) → Ventana del carrito → Checkout simulado.

## 4. Diagrama de Clases y Procesos

- **Diagrama de clases:** Se referencia el diagrama `media/image6.png` de la plantilla del Sprint 2, que muestra las nuevas entidades (`ItemCarrito`, `Carrito`, `Pedido`, `PedidoModel`) y sus relaciones con `Producto` y los controladores/vistas.
- **Diagrama de procesos:** Se referencia el diagrama `media/image7.png`. El flujo implementado cubre exactamente: selección de producto → añadir al carrito → abrir carrito → gestionar items → checkout → confirmación de pago → generación de pedido.

## 5. Persistencia de Datos
- **`data/pedidos.json`**: Estructura inicial vacía `{"pedidos": []}`. Cada pedido confirmado añade un objeto con:
  ```json
  {
    "id": 1,
    "fecha": "2026-04-29",
    "cliente": "admin",
    "items": [
      {"titulo": "Cien años de soledad", "cantidad": 2, "precio_unitario": 19.99}
    ],
    "total": 45.17
  }