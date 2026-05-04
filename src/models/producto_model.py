"""
Módulo: producto_model.py
Propósito: Gestionar la carga, filtrado y CRUD del catálogo de productos desde/hacia un archivo JSON.
Autor: [Robert Cerón, David Solís, Juan Castro]
Versión: 1.1.0 - Sprint 2 (CRUD para panel de administración)
"""

import json
import os
from typing import List, Optional

class Producto:
    """Representa un producto del catálogo."""
    def __init__(self, id: int, titulo: str, autor: str, categoria: str, precio: float, portada: str):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.precio = precio
        self.portada = portada

    def __repr__(self):
        return f"Producto({self.id}, {self.titulo}, {self.autor})"


class ProductoModel:
    """
    Modelo de productos. Carga desde data/productos.json y permite búsqueda y operaciones CRUD.
    """

    def __init__(self, ruta_json: str = "data/productos.json"):
        """
        Args:
            ruta_json (str): Ruta al archivo JSON.
        """
        self.ruta_json = ruta_json
        self.productos: List[Producto] = []
        self.cargar_productos()

    # -------------------- Carga y guardado --------------------
    def cargar_productos(self):
        """Carga los productos desde JSON."""
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
                data = json.load(archivo)
                self.productos = [
                    Producto(**p) for p in data.get('productos', [])
                ]
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            print(f"Error al cargar productos: {e}")
            self.productos = []

    def guardar_productos(self):
        """Guarda la lista actual de productos en el archivo JSON."""
        try:
            data = {"productos": [p.__dict__ for p in self.productos]}
            with open(self.ruta_json, 'w', encoding='utf-8') as archivo:
                json.dump(data, archivo, indent=4)
        except Exception as e:
            raise IOError(f"No se pudo guardar productos.json: {e}")

    # -------------------- Búsqueda y filtros --------------------
    def buscar(self, texto: str = "", autor: Optional[str] = None, categoria: Optional[str] = None) -> List[Producto]:
        """Busca productos según filtros."""
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
    def agregar_producto(self, titulo: str, autor: str, categoria: str, precio: float, portada: str) -> Producto:
        """Agrega un nuevo producto con ID autoincremental y guarda."""
        if not titulo or not autor or not categoria:
            raise ValueError("Título, autor y categoría son obligatorios.")
        nuevo_id = max([p.id for p in self.productos], default=0) + 1
        nuevo = Producto(nuevo_id, titulo, autor, categoria, precio, portada)
        self.productos.append(nuevo)
        self.guardar_productos()
        return nuevo

    def actualizar_producto(self, id: int, titulo: str, autor: str, categoria: str, precio: float, portada: str) -> bool:
        """Actualiza los datos de un producto existente. Retorna True si se realizó, False si no existe."""
        for p in self.productos:
            if p.id == id:
                p.titulo = titulo
                p.autor = autor
                p.categoria = categoria
                p.precio = precio
                p.portada = portada
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


# --- Pruebas Unitarias (AAA) del CRUD ---
if __name__ == "__main__":
    import tempfile

    # Arrange
    datos = {"productos": [{"id": 1, "titulo": "Libro A", "autor": "Autor A", "categoria": "Cat A", "precio": 10.0, "portada": ""}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    modelo = ProductoModel(ruta_tmp)

    # Act - Agregar
    nuevo = modelo.agregar_producto("Libro B", "Autor B", "Cat B", 15.0, "")
    assert nuevo.id == 2
    assert len(modelo.productos) == 2

    # Act - Actualizar
    ok = modelo.actualizar_producto(1, "Libro A Mod", "Autor A", "Cat A", 12.0, "")
    assert ok
    assert modelo.productos[0].titulo == "Libro A Mod"

    # Act - Eliminar
    ok = modelo.eliminar_producto(2)
    assert ok
    assert len(modelo.productos) == 1

    # Verificar persistencia recargando
    modelo2 = ProductoModel(ruta_tmp)
    assert len(modelo2.productos) == 1
    assert modelo2.productos[0].titulo == "Libro A Mod"

    os.unlink(ruta_tmp)
    print("✅ Pruebas CRUD del modelo de productos pasaron correctamente.")