# Documentación del Producto Construido – Sprint 3 (Primera Mitad)

## Información General
- **Sprint:** 3
- **Historias de Usuario implementadas:** HU5 – Sistema de Descuentos y Fidelización; HU6 – Registro Histórico de Compras
- **Objetivo:** Permitir a los usuarios aplicar códigos de descuento durante el checkout y consultar el historial detallado de sus pedidos anteriores.
- **Fecha:** 03/05/2026 – 05/05/2026 (según planificación original)
- **Equipo:** Robert Cerón, David Solís, Juan Castro

## 1. Sprint Backlog (Primera Mitad)

| Id | Como...      | Necesito...                              | Para...                                           | Prioridad | Sprint | Estado      |
|----|--------------|------------------------------------------|---------------------------------------------------|-----------|--------|-------------|
| 5  | Administrador| Aplicar cupones de descuento y promociones| Obtener beneficios económicos y fidelizar clientes| Baja      | 3      | Completada  |
| 6  | Administrador| Consultar el historial detallado de pedidos| Revisar transacciones pasadas y estado de envíos | Baja      | 3      | Completada  |

## 2. Historias de Usuario Detalladas

### HU5 – Sistema de Descuentos y Fidelización

**Código:** HU05N  
**Título:** Sistema de Descuentos y Fidelización  
**Como:** Administrador (o cliente autenticado)  
**Necesito:** Un campo de validación de códigos promocionales  
**Para:** Aplicar rebajas al monto total de la compra de forma automática  

#### Criterios de Aceptación
- El sistema debe verificar en tiempo real si el cupón está vigente y activo.
- Aplicar el descuento (porcentaje o monto fijo) al total antes de proceder al pago.
- Mostrar un mensaje de error si el código expiró o no existe.
- El descuento aplicado debe reflejarse en el resumen de totales del carrito.
- El pedido final debe registrar el descuento aplicado y el total final.

### HU6 – Registro Histórico de Compras

**Código:** HU06N  
**Título:** Registro Histórico de Compras  
**Como:** Administrador (o cliente autenticado)  
**Necesito:** Un panel con el listado de todas las órdenes realizadas  
**Para:** Tener control sobre los gastos y el estado de los envíos  

#### Criterios de Aceptación
- El panel de usuario debe listar las compras con fecha, ID, total y estado.
- Debe permitir visualizar el detalle de productos de cada orden pasada (en esta versión se muestra el listado general).
- Accesible desde un botón "Historial" en la barra del catálogo.
- Si no hay pedidos, se muestra un mensaje informativo.

## 3. Arquitectura y Módulos Implementados

Se utilizó el patrón MVC. A continuación se detallan los nuevos componentes y modificaciones.

### 3.1 Modelos

**Nuevo modelo:** `src/models/cupon_model.py`
- **Clase `CuponModel`**: Carga y valida cupones desde `data/cupones.json`. Métodos:
  - `cargar_cupones()`: Lee el archivo JSON.
  - `validar_cupon(codigo)`: Retorna el cupón si existe y está activo, o `None`.
  - `aplicar_descuento(cupon, total)`: Calcula el nuevo total según el tipo de descuento (porcentaje o fijo).

**Modificado:** `src/models/carrito_model.py`
- **Método `crear_pedido`**: Se añadió el parámetro opcional `descuento` y el campo `"estado": "Pendiente"` en el pedido generado.

### 3.2 Vistas

**Nueva vista:** `src/views/historial_view.py`
- Ventana `QMainWindow` con tabla de pedidos (ID, Fecha, Total, Estado).
- Botón "Cerrar".
- Método `cargar_historial(pedidos)` que recibe una lista de diccionarios y llena la tabla.

**Modificada:** `src/views/carrito_view.py`
- Se añadió un campo `QLineEdit` para el código promocional y un botón "Aplicar".
- Se añadió un label `lbl_descuento` (inicialmente oculto) en el resumen de totales.
- El método `actualizar_totales` ahora recibe un parámetro opcional `descuento` y lo muestra si es mayor que 0.
- Nuevo método `obtener_codigo_cupon()`.

**Modificada:** `src/views/catalogo_view.py`
- Se añadió el botón "Historial" (`btn_historial`) en la barra de herramientas, visible para todos los usuarios.

### 3.3 Controladores

**Nuevo controlador:** `src/controllers/historial_controller.py`
- Recibe `HistorialView` y `PedidoModel`.
- Método `cargar_historial(usuario)`: Obtiene los pedidos del cliente desde el modelo y los pasa a la vista.

**Modificado:** `src/controllers/carrito_controller.py`
- Se añadió el parámetro `cupon_model` en el constructor.
- Se añadieron los atributos `descuento_aplicado` y `cupon_aplicado`.
- Nuevo método `aplicar_cupon()`: Valida el código ingresado, calcula el descuento y actualiza la vista.
- El método `actualizar_vista()` ahora calcula y muestra el total final restando el descuento.
- El método `procesar_pago()` envía el descuento al crear el pedido.

**Modificado:** `src/controllers/catalogo_controller.py`
- Se añadieron los parámetros `usuario_actual` e `historial_ctrl` en el constructor.
- Se conectó el botón "Historial" (si existe) al nuevo método `abrir_historial()`.
- `abrir_historial()`: Muestra la ventana de historial y carga los pedidos del usuario actual.

### 3.4 Integración en `main.py`
- Se instancian `CuponModel`, `HistorialView` e `HistorialController`.
- Se pasan al `CarritoController` (cupon_model) y al `CatalogoController` (usuario_actual, historial_ctrl).
- Flujo completo: Login → Catálogo (con botones Carrito, Panel Admin e Historial) → Carrito (con cupones) → Checkout (con descuento) → Pedido guardado con estado y descuento → Historial disponible.

## 4. Diagrama de Clases y Procesos

- **Diagrama de clases:** Se referencia el diagrama `media/image8.png` de la plantilla del Sprint 3, que muestra las nuevas entidades (`Cupon`, `CuponModel`, `HistorialView`, `HistorialController`) y sus relaciones con `Carrito`, `Pedido` y los controladores existentes.
- **Diagrama de procesos:** Se referencia el diagrama `media/image9.png`. Flujos implementados:
  1. Aplicación de cupón: Usuario ingresa código → Controlador valida con CuponModel → Calcula descuento → Actualiza totales en la vista.
  2. Consulta de historial: Usuario presiona "Historial" → Controlador obtiene pedidos del modelo → Muestra en tabla.

## 5. Persistencia de Datos

- **`data/cupones.json`**: Creado con estructura:
  ```json
  {
    "cupones": [
      {
        "codigo": "DESC10",
        "tipo": "porcentaje",
        "valor": 10,
        "activo": true
      }
    ]
  }