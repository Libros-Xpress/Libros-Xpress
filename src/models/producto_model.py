"""
Módulo: producto_model.py
Propósito: Gestionar la carga y filtrado del catálogo de productos desde un archivo JSON.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

import json
import os
from typing import List, Dict, Optional

class Producto:
    """
    Representa un producto del catálogo.
    """
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
    Modelo de productos. Carga los datos desde data/productos.json y proporciona métodos de búsqueda avanzada.
    """

    def __init__(self, ruta_json: str = "data/productos.json"):
        """
        Args:
            ruta_json (str): Ruta al archivo JSON con los productos.
        Raises:
            FileNotFoundError: Si el archivo no existe.
            json.JSONDecodeError: Si el JSON está mal formado.
        """
        self.ruta_json = ruta_json
        self.productos: List[Producto] = []
        self.cargar_productos()

    def cargar_productos(self):
        """
        Carga los productos desde el archivo JSON. Si hay errores, muestra un mensaje y deja la lista vacía.
        """
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
                data = json.load(archivo)
                self.productos = [
                    Producto(
                        id=p['id'],
                        titulo=p['titulo'],
                        autor=p['autor'],
                        categoria=p['categoria'],
                        precio=p['precio'],
                        portada=p['portada']
                    )
                    for p in data.get('productos', [])
                ]
        except FileNotFoundError:
            print(f"Advertencia: Archivo no encontrado {self.ruta_json}. Catálogo vacío.")
            self.productos = []
        except json.JSONDecodeError:
            print(f"Error: El archivo {self.ruta_json} no es un JSON válido. Catálogo vacío.")
            self.productos = []
        except Exception as e:
            print(f"Error inesperado al cargar productos: {e}")
            self.productos = []

    def buscar(self, texto: str = "", autor: Optional[str] = None, categoria: Optional[str] = None) -> List[Producto]:
        """
        Busca productos filtrando por título, autor y/o categoría.

        Args:
            texto (str): Texto a buscar en el título (insensible a mayúsculas).
            autor (Optional[str]): Filtro exacto por autor.
            categoria (Optional[str]): Filtro exacto por categoría.

        Returns:
            List[Producto]: Lista de productos que cumplen los criterios.
        """
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
        """Devuelve la lista de autores únicos."""
        return sorted({p.autor for p in self.productos})

    def obtener_categorias(self) -> List[str]:
        """Devuelve la lista de categorías únicas."""
        return sorted({p.categoria for p in self.productos})


# --- Pruebas Unitarias (AAA) ---
if __name__ == "__main__":
    import tempfile

    # Arrange
    datos = {
        "productos": [
            {"id": 1, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "categoria": "Novela", "precio": 19.99, "portada": "assets/img/cien_anios.jpg"},
            {"id": 2, "titulo": "El principito", "autor": "Antoine de Saint-Exupéry", "categoria": "Infantil", "precio": 12.50, "portada": "assets/img/principito.jpg"},
            {"id": 3, "titulo": "1984", "autor": "George Orwell", "categoria": "Ciencia ficción", "precio": 15.00, "portada": "assets/img/1984.jpg"}
        ]
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    # Act
    modelo = ProductoModel(ruta_tmp)
    # Buscar por texto "soled"
    res1 = modelo.buscar(texto="soled")
    # Filtrar por autor exacto
    res2 = modelo.buscar(autor="George Orwell")
    # Filtrar por categoría
    res3 = modelo.buscar(categoria="Infantil")
    # Criterio combinado
    res4 = modelo.buscar(texto="el", autor="Antoine de Saint-Exupéry")

    # Assert
    assert len(res1) == 1 and res1[0].titulo == "Cien años de soledad", "Fallo búsqueda por texto"
    assert len(res2) == 1 and res2[0].titulo == "1984", "Fallo búsqueda por autor"
    assert len(res3) == 1 and res3[0].titulo == "El principito", "Fallo búsqueda por categoría"
    assert len(res4) == 1 and res4[0].titulo == "El principito", "Fallo búsqueda combinada"
    assert modelo.obtener_autores() == ['Antoine de Saint-Exupéry', 'Gabriel García Márquez', 'George Orwell']
    assert modelo.obtener_categorias() == ['Ciencia ficción', 'Infantil', 'Novela']

    # Limpiar archivo temporal
    os.unlink(ruta_tmp)
    print("✅ Todas las pruebas unitarias del modelo pasaron correctamente.")