# Documentación del Producto Construido – Sprint 1

## Información General
- **Sprint:** 1
- **Historias de Usuario implementadas:** HU1 – Visualización de Catálogo y Buscador; HU2 – Registro y Autenticación de Usuarios
- **Objetivo:** Establecer la base del sistema Libros-Xpress permitiendo a los usuarios registrarse, iniciar sesión y visualizar un catálogo de productos con búsqueda avanzada.
- **Fecha:** 27/04/2026 – 28/04/2026 (según planificación)
- **Equipo:** Robert Cerón, David Solís, Juan Castro

## 1. Sprint Backlog

| Id | Como...      | Necesito...                                      | Para...                                                       | Prioridad | Sprint | Estado      |
|----|--------------|--------------------------------------------------|---------------------------------------------------------------|-----------|--------|-------------|
| 1  | Administrador| Visualizar y buscar productos en el catálogo     | Explorar la oferta de libros y papelería antes de comprar     | Alta      | 1      | Completada  |
| 2  | Administrador| Registrarme e iniciar sesión en la plataforma    | Acceder a las funciones de gestión y proteger mis datos       | Alta      | 1      | Completada  |

## 2. Historias de Usuario Detalladas

### HU1 – Visualización de Catálogo y Buscador

**Código:** HU01N  
**Título:** Visualización de Catálogo y Buscador  
**Como:** Administrador (o usuario autenticado)  
**Necesito:** Un catálogo digital con filtros de búsqueda  
**Para:** Localizar libros por título, autor o categoría de forma inmediata  

#### Criterios de Aceptación
- Dado que el usuario está en la página de inicio, cuando ingresa un término en la barra de búsqueda y presiona Enter, el sistema muestra los productos que coinciden con el título, incluyendo portada y precio.
- El sistema debe permitir filtrar por autor y categoría mediante listas desplegables.
- Si no hay resultados, se debe mostrar un mensaje informativo.
- Las imágenes de las portadas deben cargarse correctamente; si no existen, se mostrará una imagen gris por defecto.

### HU2 – Registro y Autenticación de Usuarios

**Código:** HU02N  
**Título:** Registro y Autenticación de Usuarios  
**Como:** Usuario nuevo o existente  
**Necesito:** Un sistema de acceso seguro con correo (nombre de usuario) y contraseña  
**Para:** Proteger mi información personal y gestionar mis pedidos  

#### Criterios de Aceptación
- Dado que un usuario no tiene cuenta, cuando completa el formulario de registro con datos válidos y confirma, el sistema crea el perfil y permite el ingreso a las áreas restringidas.
- El formulario de registro debe validar que el nombre de usuario no exista previamente, que las contraseñas coincidan y que tengan al menos 3 caracteres.
- En el inicio de sesión, si las credenciales son correctas, se muestra un mensaje de bienvenida y se accede al catálogo; si son incorrectas, se notifica el error.
- Debe existir un enlace funcional para recuperar contraseña (simulado).

## 3. Arquitectura y Módulos Implementados

Se utilizó el patrón MVC (Modelo-Vista-Controlador) con interfaz PySide6 y persistencia en archivos JSON.

### 3.1 Módulo de Catálogo (HU1)

**Modelo:** `src/models/producto_model.py`
- **Clase `Producto`**: Representa un producto (id, título, autor, categoría, precio, portada).
- **Clase `ProductoModel`**:
  - Carga productos desde `data/productos.json`.
  - Método `buscar(texto, autor, categoria)`: Filtra productos por coincidencia de texto en título (insensible a mayúsculas), autor exacto y categoría exacta.
  - Métodos `obtener_autores()` y `obtener_categorias()`: Devuelven listas únicas para los combos.

**Vista:** `src/views/catalogo_view.py`
- Ventana principal (`QMainWindow`) con barra de búsqueda (`QLineEdit`), combos de autor y categoría (`QComboBox`), botón "Buscar" y área de resultados con `QScrollArea` y `QGridLayout`.
- Método `mostrar_productos(productos, on_agregar)`: Renderiza los productos en tarjetas con portada, título y precio. Si se proporciona el callback `on_agregar`, añade un botón "Agregar" (integrado en Sprint 2).

**Controlador:** `src/controllers/catalogo_controller.py`
- Conecta las señales de la vista con el modelo.
- `realizar_busqueda()`: Obtiene filtros de la vista, llama al modelo y actualiza la vista.
- `mostrar_todos()`: Carga todos los productos al inicio.
- (En Sprint 2 se añadió la integración con el carrito.)

### 3.2 Módulo de Autenticación (HU2)

**Modelo:** `src/models/usuario_model.py`
- **Clase `Usuario`**: username, password, rol.
- **Clase `UsuarioModel`**:
  - Carga y guarda usuarios en `data/database.json`.
  - `autenticar(username, password)`: Retorna el `Usuario` si las credenciales son correctas.
  - `registrar(username, password, rol)`: Añade un nuevo usuario si el nombre no existe, y guarda el archivo.
  - `existe_usuario(username)`: Verifica disponibilidad del nombre.

**Vista:** `src/views/login_view.py`
- Ventana (`QMainWindow`) con tamaño fijo.
- `QStackedWidget` que alterna entre página de **Login** (campos usuario, contraseña, botones "Entrar", "Regístrate aquí", "Olvidaste tu contraseña") y **Registro** (usuario, contraseña, confirmar, combo de rol, botón "Crear Cuenta", enlace "Ya tengo cuenta").
- Estilos modernos y centrado en pantalla.
- Métodos `mostrar_login()` y `mostrar_registro()` para navegar entre páginas.

**Controlador:** `src/controllers/auth_controller.py`
- Conecta botones y campos de la vista con la lógica.
- `iniciar_sesion()`: Valida campos, llama a `modelo.autenticar()`, guarda el usuario logueado en `self.usuario_actual` y cierra la ventana de login.
- `registrar_usuario()`: Valida campos, coincidencia de contraseñas, longitud y registra al usuario.
- `recuperar_contrasena()`: Muestra mensaje informativo.

### 3.3 Integración en `main.py`
- Se inicia la aplicación con la ventana de login.
- Tras autenticación exitosa (la ventana de login se cierra), se instancian los módulos de catálogo y se muestra la ventana principal.
- Flujo: Login → Catálogo (con búsqueda y visualización de productos).

## 4. Diagrama de Clases y Procesos

- **Diagrama de clases:** Referencia `media/image4.png` de la plantilla del Sprint 1. Clases implementadas:
  - `Producto`, `ProductoModel`, `CatalogoView`, `CatalogoController`
  - `Usuario`, `UsuarioModel`, `LoginView`, `AuthController`
- **Diagrama de procesos:** Referencia `media/image5.png`. Flujos implementados:
  1. Búsqueda en catálogo: el usuario ingresa filtros → el controlador los envía al modelo → el modelo retorna resultados → la vista los muestra.
  2. Autenticación: el usuario ingresa credenciales → el controlador valida con el modelo → si es exitoso, se cierra la ventana y se abre el catálogo.
  3. Registro: el usuario llena el formulario → el controlador valida y registra → redirige al login.

## 5. Persistencia de Datos

- **`data/productos.json`**: Almacena el catálogo de productos. Estructura:
  ```json
  {
    "productos": [
      {
        "id": 1,
        "titulo": "Cien años de soledad",
        "autor": "Gabriel García Márquez",
        "categoria": "Novela",
        "precio": 19.99,
        "portada": "assets/img/cien_anios.jpg"
      }
    ]
  }
  ```
- **`data/database.json`**: Almacena los usuarios registrados. Estructura:
  ```json
  {
    "usuarios": [
      {
        "username": "admin",
        "password": "123",
        "rol": "Admin"
      }
    ]
  }
  ```
