"""
Módulo: producto_model.py
Propósito: Gestionar la carga, filtrado, CRUD y stock del catálogo de productos desde/hacia un archivo JSON.
Autor: [Robert Cerón, David Solís, Juan Castro]
Versión: 1.2.0 - Sprint 4 (Sincronización de stock)
"""

import json
import os
from typing import List, Optional

class Producto:
    """Representa un producto del catálogo (incluye stock)."""
    def __init__(self, id: int, titulo: str, autor: str, categoria: str, precio: float, portada: str, stock: int = 0):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.precio = precio
        self.portada = portada
        self.stock = stock

    def __repr__(self):
        return f"Producto({self.id}, {self.titulo}, {self.autor}, stock={self.stock})"


class ProductoModel:
    """
    Modelo de productos. Carga desde data/productos.json y permite búsqueda, operaciones CRUD y gestión de stock.
    """

    def __init__(self, ruta_json: str = "data/productos.json"):
        self.ruta_json = ruta_json
        self.productos: List[Producto] = []
        self.cargar_productos()

    # -------------------- Carga y guardado --------------------
    def cargar_productos(self):
        """Carga los productos desde JSON. Si falta el campo 'stock', lo inicializa en 0."""
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
                data = json.load(archivo)
                self.productos = []
                for p in data.get('productos', []):
                    # Retrocompatibilidad: si no tiene 'stock', se agrega 0
                    if 'stock' not in p:
                        p['stock'] = 0
                    self.productos.append(Producto(**p))
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            print(f"Error al cargar productos: {e}")
            self.productos = []

    def guardar_productos(self):
        """Guarda la lista actual de productos en el archivo JSON, incluyendo stock."""
        try:
            data = {
                "productos": [
                    {
                        "id": p.id,
                        "titulo": p.titulo,
                        "autor": p.autor,
                        "categoria": p.categoria,
                        "precio": p.precio,
                        "portada": p.portada,
                        "stock": p.stock
                    } for p in self.productos
                ]
            }
            with open(self.ruta_json, 'w', encoding='utf-8') as archivo:
                json.dump(data, archivo, indent=4)
        except Exception as e:
            raise IOError(f"No se pudo guardar productos.json: {e}")

    # -------------------- Búsqueda y filtros --------------------
    def buscar(self, texto: str = "", autor: Optional[str] = None, categoria: Optional[str] = None) -> List[Producto]:
        resultados = self.productos
        if texto:
            texto_lower = texto.lower()
            resultados = [p for p in resultados if texto_lower in p.titulo.lower()]
        if autor:
            resultados = [p for p in resultados if p.autor == autor]
        if categoria:
            resultados = [p for p in resultados if p.categoria == categoria]
        return resultados

    def obtener_autores(self) -> List[str]:
        return sorted({p.autor for p in self.productos})

    def obtener_categorias(self) -> List[str]:
        return sorted({p.categoria for p in self.productos})

    # -------------------- CRUD --------------------
    def agregar_producto(self, titulo: str, autor: str, categoria: str, precio: float, portada: str, stock: int = 0) -> Producto:
        """Agrega un nuevo producto con ID autoincremental y guarda."""
        if not titulo or not autor or not categoria:
            raise ValueError("Título, autor y categoría son obligatorios.")
        nuevo_id = max([p.id for p in self.productos], default=0) + 1
        nuevo = Producto(nuevo_id, titulo, autor, categoria, precio, portada, stock)
        self.productos.append(nuevo)
        self.guardar_productos()
        return nuevo

    def actualizar_producto(self, id: int, titulo: str, autor: str, categoria: str, precio: float, portada: str, stock: int = None) -> bool:
        """Actualiza los datos de un producto existente. Si se pasa stock, lo actualiza también."""
        for p in self.productos:
            if p.id == id:
                p.titulo = titulo
                p.autor = autor
                p.categoria = categoria
                p.precio = precio
                p.portada = portada
                if stock is not None:
                    p.stock = stock
                self.guardar_productos()
                return True
        return False

    def eliminar_producto(self, id: int) -> bool:
        """Elimina un producto por ID. Retorna True si se eliminó, False si no existe."""
        for i, p in enumerate(self.productos):
            if p.id == id:
                del self.productos[i]
                self.guardar_productos()
                return True
        return False

    # -------------------- Gestión de stock (NUEVO Sprint 4) --------------------
    def reducir_stock(self, id_producto: int, cantidad: int) -> bool:
        """Reduce el stock de un producto en la cantidad indicada. Retorna True si se pudo, False si no hay suficiente stock."""
        for p in self.productos:
            if p.id == id_producto:
                if p.stock >= cantidad:
                    p.stock -= cantidad
                    self.guardar_productos()
                    return True
                else:
                    return False
        return False

    def incrementar_stock(self, id_producto: int, cantidad: int) -> bool:
        """Incrementa el stock de un producto. Retorna True si se realizó."""
        for p in self.productos:
            if p.id == id_producto:
                p.stock += cantidad
                self.guardar_productos()
                return True
        return False


# --- Pruebas Unitarias (AAA) del CRUD y stock ---
if __name__ == "__main__":
    import tempfile

    # Arrange
    datos = {"productos": [{"id": 1, "titulo": "Libro A", "autor": "Autor A", "categoria": "Cat A", "precio": 10.0, "portada": "", "stock": 5}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    modelo = ProductoModel(ruta_tmp)

    # --- Pruebas CRUD (sprint 2) ---
    nuevo = modelo.agregar_producto("Libro B", "Autor B", "Cat B", 15.0, "", stock=10)
    assert nuevo.id == 2
    assert len(modelo.productos) == 2
    assert nuevo.stock == 10

    ok = modelo.actualizar_producto(1, "Libro A Mod", "Autor A", "Cat A", 12.0, "")
    assert ok
    assert modelo.productos[0].titulo == "Libro A Mod"

    ok = modelo.eliminar_producto(2)
    assert ok
    assert len(modelo.productos) == 1

    # --- Pruebas de stock (sprint 4) ---
    ok = modelo.reducir_stock(1, 2)
    assert ok
    assert modelo.productos[0].stock == 3

    ok = modelo.reducir_stock(1, 10)
    assert not ok
    assert modelo.productos[0].stock == 3  # no cambió

    ok = modelo.incrementar_stock(1, 4)
    assert ok
    assert modelo.productos[0].stock == 7

    # Verificar persistencia recargando
    modelo2 = ProductoModel(ruta_tmp)
    assert len(modelo2.productos) == 1
    assert modelo2.productos[0].titulo == "Libro A Mod"
    assert modelo2.productos[0].stock == 7

    os.unlink(ruta_tmp)
    print("✅ Pruebas CRUD y de stock del modelo de productos pasaron correctamente.")