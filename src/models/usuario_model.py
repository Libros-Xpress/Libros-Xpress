"""
Módulo: usuario_model.py
Propósito: Gestión de usuarios (carga, registro, autenticación) usando JSON.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

import json
import os
from typing import List, Dict, Optional

class Usuario:
    """
    Representa un usuario del sistema.
    """
    def __init__(self, username: str, password: str, rol: str):
        self.username = username
        self.password = password
        self.rol = rol

    def __repr__(self):
        return f"Usuario({self.username}, {self.rol})"


class UsuarioModel:
    """
    Modelo de usuarios. Carga y guarda en data/database.json.
    """

    def __init__(self, ruta_json: str = "data/database.json"):
        """
        Args:
            ruta_json (str): Ruta al archivo JSON con los usuarios.
        Raises:
            FileNotFoundError: Si el archivo no existe.
            json.JSONDecodeError: Si el JSON está mal formado.
        """
        self.ruta_json = ruta_json
        self.usuarios: List[Usuario] = []
        self.cargar_usuarios()

    def cargar_usuarios(self):
        """
        Carga los usuarios desde el archivo JSON. Si hay errores, deja la lista vacía.
        """
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
                data = json.load(archivo)
                self.usuarios = [
                    Usuario(u['username'], u['password'], u['rol'])
                    for u in data.get('usuarios', [])
                ]
        except FileNotFoundError:
            print(f"Advertencia: Archivo no encontrado {self.ruta_json}. Se creará uno nuevo al guardar.")
            self.usuarios = []
        except json.JSONDecodeError:
            print(f"Error: El archivo {self.ruta_json} no es un JSON válido. Lista vacía.")
            self.usuarios = []
        except Exception as e:
            print(f"Error inesperado al cargar usuarios: {e}")
            self.usuarios = []

    def guardar_usuarios(self):
        """
        Guarda la lista de usuarios en el archivo JSON.
        Raises:
            IOError: Si no se puede escribir el archivo.
        """
        try:
            data = {
                "usuarios": [
                    {"username": u.username, "password": u.password, "rol": u.rol}
                    for u in self.usuarios
                ]
            }
            with open(self.ruta_json, 'w', encoding='utf-8') as archivo:
                json.dump(data, archivo, indent=4)
        except Exception as e:
            raise IOError(f"No se pudo guardar el archivo JSON: {e}")

    def autenticar(self, username: str, password: str) -> Optional[Usuario]:
        """
        Verifica credenciales y devuelve el usuario si son correctas.

        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña.

        Returns:
            Optional[Usuario]: Usuario autenticado o None si falla.
        """
        for usuario in self.usuarios:
            if usuario.username == username and usuario.password == password:
                return usuario
        return None

    def registrar(self, username: str, password: str, rol: str = "Cliente") -> bool:
        """
        Registra un nuevo usuario si el nombre no existe.

        Args:
            username (str): Nombre de usuario único.
            password (str): Contraseña.
            rol (str): Rol del usuario (por defecto "Cliente").

        Returns:
            bool: True si se registró correctamente, False si el usuario ya existe.
        Raises:
            IOError: Si falla al guardar el JSON.
        """
        # Verificar si ya existe
        if any(u.username == username for u in self.usuarios):
            return False
        nuevo = Usuario(username, password, rol)
        self.usuarios.append(nuevo)
        self.guardar_usuarios()
        return True

    def existe_usuario(self, username: str) -> bool:
        """Verifica si un nombre de usuario ya está registrado."""
        return any(u.username == username for u in self.usuarios)


# --- Pruebas Unitarias (AAA) ---
if __name__ == "__main__":
    import tempfile

    # Arrange
    datos_iniciales = {"usuarios": [{"username": "admin", "password": "123", "rol": "Admin"}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_iniciales, tmp)
        ruta_tmp = tmp.name

    modelo = UsuarioModel(ruta_tmp)

    # Act - autenticar admin
    usuario_admin = modelo.autenticar("admin", "123")
    # Act - autenticar con credenciales incorrectas
    usuario_falso = modelo.autenticar("admin", "incorrecta")
    # Act - registrar nuevo usuario
    ok = modelo.registrar("cliente1", "abc", "Cliente")
    # Act - intentar duplicado
    ok_dup = modelo.registrar("cliente1", "otra")
    # Act - verificar existencia
    existe = modelo.existe_usuario("cliente1")

    # Assert
    assert usuario_admin is not None, "Fallo autenticación admin correcta"
    assert usuario_admin.rol == "Admin"
    assert usuario_falso is None, "Fallo autenticación con contraseña incorrecta"
    assert ok, "Fallo registro nuevo usuario"
    assert not ok_dup, "Fallo: no debería permitir usuario duplicado"
    assert existe, "Fallo verificación existencia"

    # Verificar persistencia recargando el modelo
    modelo2 = UsuarioModel(ruta_tmp)
    assert len(modelo2.usuarios) == 2, "Fallo persistencia: debería haber 2 usuarios"
    assert modelo2.autenticar("cliente1", "abc") is not None

    # Limpiar archivo temporal
    os.unlink(ruta_tmp)
    print("✅ Todas las pruebas unitarias del modelo de usuarios pasaron correctamente.")