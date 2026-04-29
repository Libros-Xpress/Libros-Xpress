# Documentación del Producto Construido – Sprint 1 (ID: Catálogo y Buscador)

## 1. Módulo: Catálogo de Productos
**Propósito:** Permitir al administrador visualizar el catálogo de libros y papelería, buscar por título, autor y categoría, viendo portadas y precios.

## 2. Diagrama de clases
Referencia: `media/image4.png` (incluido en la plantilla del sprint).

Clases implementadas:
- `Producto` (entidad)
- `ProductoModel` (carga JSON, filtrado)
- `CatalogoView` (interfaz con QScrollArea, QGridLayout)
- `CatalogoController` (conexión vista-modelo)

## 3. Diagrama de procesos
Referencia: `media/image5.png`. Flujo implementado:
1. Usuario ingresa texto o selecciona filtros.
2. Señal `clicked` o `returnPressed` dispara `realizar_busqueda()`.
3. Controlador obtiene valores y llama a `modelo.buscar()`.
4. Modelo filtra y retorna lista de `Producto`.
5. Controlador envía la lista a `vista.mostrar_productos()`.

## 4. Instrucciones de ejecución
- Instalar dependencias: `pip install -r requirements.txt`
- Asegurar que `data/productos.json` existe.
- Ejecutar: `python src/main.py`

## 5. Pruebas unitarias
- Modelo: AAA en `producto_model.py` (cobertura de búsqueda por texto, autor, categoría y combinados).
- Controlador: simulación de búsqueda y verificación de actualización de vista.
- Vista: prueba visual estática.

Resultado: Todas las pruebas unitarias pasaron correctamente.