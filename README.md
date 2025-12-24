# Inventory Panel – Django CRUD App

Inventory Panel es una aplicación web desarrollada con Django que permite gestionar:

- Productos  
- Categorías  
- Usuarios (rol administrador)  
- Autenticación (login y logout)
- Panel principal (dashboard)

Este proyecto forma parte de un portafolio profesional para Upwork.

---

## 🚀 Tecnologías utilizadas

- Python 3
- Django 5
- SQLite (modo desarrollo)
- HTML + CSS (diseño estilo Admin Panel)
- Bootstrap básico

---

## 🧩 Funcionalidades

- Login / Logout
- CRUD completo de Productos (crear, listar, editar, eliminar)
- CRUD de Categorías  
- Gestión de usuarios (solo admin)
- Panel visual limpio en tonos oscuros/grises
- Restricción de acceso usando decoradores `@login_required`

---

## 🛠️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/inventory_panel.git
cd inventory_panel
```

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
```

Linux / Mac:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor

```bash
python manage.py runserver
```

### La app estará disponible en:

```bash
http://127.0.0.1:8000/
```
📷 Capturas

(Se agregarán capturas cuando el proyecto esté publicado en GitHub)

📄 Licencia

MIT License

