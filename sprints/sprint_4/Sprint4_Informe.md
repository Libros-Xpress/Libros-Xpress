# Documentación del Producto Construido – Sprint 4

## Información General
- **Sprint:** 4
- **Historias de Usuario implementadas:** HU7 – Sincronización de Stock entre Tienda Física y Web; HU8 – Generación y Descarga de Facturas Digitales
- **Objetivo:** Evitar la venta de productos agotados sincronizando el inventario entre canales y proporcionar a los clientes facturas digitales en PDF.
- **Fecha:** 06/05/2026 – 08/05/2026 (según planificación original)
- **Equipo:** Robert Cerón, David Solís, Juan Castro

## 1. Sprint Backlog

| Id | Como...      | Necesito...                              | Para...                                           | Prioridad | Sprint | Estado      |
|----|--------------|------------------------------------------|---------------------------------------------------|-----------|--------|-------------|
| 7  | Administrador| Sincronizar el stock entre tienda física y web | Evitar la venta de productos agotados y garantizar disponibilidad real | Media     | 4      | Completada  |
| 8  | Administrador| Generar y descargar facturas digitales    | Obtener un comprobante formal y detallado de la compra | Media     | 4      | Completada  |

## 2. Historias de Usuario Detalladas

### HU7 – Sincronización de Stock Físico y Virtual

**Código:** HU07N  
**Título:** Sincronización de Stock Físico y Virtual  
**Como:** Administrador  
**Necesito:** Una base de datos centralizada y actualizada en tiempo real  
**Para:** Evitar la venta de productos que ya no están disponibles físicamente  

#### Criterios de Aceptación
- Al registrar una venta física, el stock en la web debe disminuir automáticamente.
- Si un producto llega a stock cero, debe marcarse como "Agotado" en la plataforma online.
- El catálogo muestra la cantidad disponible actualizada en tiempo real.
- La venta física genera un pedido con estado "Venta Física" para trazabilidad.
- Solo los administradores pueden acceder a la funcionalidad de venta física.

### HU8 – Exportación de Factura en Formato PDF

**Código:** HU08N  
**Título:** Exportación de Factura en Formato PDF  
**Como:** Usuario (cliente o administrador)  
**Necesito:** Un motor de generación de documentos digitales  
**Para:** Obtener un respaldo legal de la compra realizada  

#### Criterios de Aceptación
- Tras cada compra exitosa (en línea o física), el sistema genera automáticamente un archivo PDF.
- El PDF incluye: número de factura, fecha, cliente, detalle de productos, subtotal, impuesto, descuento y total.
- Desde el historial de pedidos, el usuario puede descargar la factura de cualquier pedido anterior.
- El archivo se nombra como `factura_[id].pdf` y se guarda en la carpeta `facturas/`.

## 3. Arquitectura y Módulos Implementados

Se utilizó el patrón MVC. A continuación se detallan los nuevos componentes y modificaciones.

### 3.1 Modelos

**Nuevo modelo:** `src/models/factura_model.py`
- **Clase `FacturaModel`**: Genera facturas en PDF usando PySide6 (`QPrinter`, `QTextDocument`). Métodos:
  - `generar_factura_pdf(pedido)`: Construye un documento HTML con el detalle del pedido y lo exporta a PDF.
  - `_construir_html(pedido)`: Genera el contenido HTML con estilos, tabla de productos y totales.

**Modificado:** `src/models/producto_model.py`
- Se añadió el campo `stock` a la clase `Producto` con valor por defecto 0.
- Nuevos métodos:
  - `reducir_stock(id, cantidad)`: Descuenta unidades del inventario.
  - `incrementar_stock(id, cantidad)`: Incrementa las unidades disponibles.
- Los métodos `cargar_productos()` y `guardar_productos()` ahora incluyen el campo `stock`.

### 3.2 Vistas

**Nueva vista:** `src/views/venta_fisica_view.py`
- Ventana `QMainWindow` con:
  - `QComboBox` que lista todos los productos y su stock actual.
  - `QSpinBox` para indicar la cantidad vendida.
  - Etiqueta `lbl_stock` que muestra el stock disponible del producto seleccionado.
  - Botón "Registrar Venta".
- Métodos: `cargar_productos()`, `obtener_producto_seleccionado_id()`, `obtener_cantidad()`, `actualizar_stock_label()`.

**Modificada:** `src/views/catalogo_view.py`
- Se añadió el botón `btn_venta_fisica` (inicialmente oculto, solo para admin).
- En `mostrar_productos`, se agregó una etiqueta `lbl_stock` debajo del precio, visible para todos los usuarios.

**Modificada:** `src/views/historial_view.py`
- Se añadió el botón `btn_descargar_factura` en un layout inferior.
- Nuevo método `obtener_pedido_seleccionado()` para recuperar los datos del pedido activo en la tabla.

### 3.3 Controladores

**Nuevo controlador:** `src/controllers/venta_fisica_controller.py`
- Recibe `VentaFisicaView`, `ProductoModel`, `PedidoModel`, usuario actual y callback de refresco.
- Método `registrar_venta()`: Valida stock, lo reduce, crea un pedido con estado "Venta Física" y refresca el catálogo.
- `cargar_productos()`: Alimenta el combo de la vista con los productos actuales.

**Modificado:** `src/controllers/catalogo_controller.py`
- Se añadió el parámetro `venta_fisica_ctrl` en el constructor.
- Si el usuario es admin y se pasa el controlador, se muestra `btn_venta_fisica` y se conecta a `abrir_venta_fisica()`.
- `abrir_venta_fisica()`: Muestra la ventana correspondiente y recarga la lista de productos.

**Modificado:** `src/controllers/historial_controller.py`
- Se añadió `FacturaModel` como parámetro opcional en el constructor.
- `_configurar_senales()`: Conecta el botón `btn_descargar_factura` con el método `descargar_factura()`.
- `descargar_factura()`: Obtiene el pedido seleccionado, busca sus datos completos, genera el PDF e informa al usuario.

**Modificado:** `src/controllers/carrito_controller.py`
- Se añadieron los parámetros `modelo_productos` y `factura_model` en el constructor.
- En `procesar_pago()`: después de crear el pedido, se reduce el stock de cada ítem comprado y se genera la factura automáticamente.
- El mensaje de confirmación ahora incluye la ruta del PDF generado.

### 3.4 Integración en `main.py`
- Se instancia `FacturaModel` con la carpeta `"facturas"`.
- Se pasa `modelo_productos` y `factura_model` al `CarritoController`.
- Se pasa `factura_model` al `HistorialController`.
- Si el rol es Admin, se instancia `VentaFisicaView` y `VentaFisicaController`, y se pasan al `CatalogoController`.
- Se asignan los callbacks de refresco (`mostrar_todos`) a los controladores de administración y venta física.

## 4. Diagrama de Clases y Procesos

- **Diagrama de clases:** Se referencia el diagrama `media/image10.png` de la plantilla del Sprint 4, que muestra las nuevas entidades (`FacturaModel`, `VentaFisicaView`, `VentaFisicaController`) y sus relaciones con `Producto`, `Pedido` y los controladores existentes.
- **Diagrama de procesos:** Se referencia el diagrama `media/image11.png`. Flujos implementados:
  1. Venta física: Admin abre ventana → selecciona producto y cantidad → el controlador valida y reduce stock → crea pedido "Venta Física" → actualiza catálogo.
  2. Facturación: Al finalizar compra (en línea o física) → se genera PDF → se puede descargar desde el historial.

## 5. Persistencia de Datos

- **`data/productos.json`**: Se añadió el campo `"stock"` a cada producto. Estructura actualizada:
  ```json
  {
    "productos": [
      {
        "id": 1,
        "titulo": "Cien años de soledad",
        "autor": "Gabriel García Márquez",
        "categoria": "Novela",
        "precio": 19.99,
        "portada": "assets/img/cien_anios.jpg",
        "stock": 10
      }
    ]
  }


