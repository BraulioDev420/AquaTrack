# AquaTrack
AquaTrack

AquaTrack es una aplicación web desarrollada en Flask + MySQL para la gestión de acueductos en Colombia, enfocada en el control de calidad del agua y administración de funcionarios responsables.

La plataforma permite registrar, visualizar y administrar acueductos a nivel nacional, asociando información relevante como indicadores de análisis (pH, cloro, bacterias), departamentos y responsables. Además, incluye un mapa interactivo en SVG de Colombia que muestra la cantidad de acueductos y funcionarios en cada departamento.
---
Características principales

Autenticación de usuarios

Registro, inicio de sesión y restablecimiento de contraseña.

Gestión de sesiones con seguridad (hash de contraseñas con Werkzeug).

Gestión de Funcionarios

Agregar, editar y eliminar funcionarios.

Validación de funcionarios asociados a acueductos.

Gestión de Acueductos

Registrar acueductos con ubicación, fecha de análisis, pH, cloro, bacterias, descripción y funcionario responsable.

Editar o eliminar registros existentes.

Asociación de cada acueducto a un funcionario y un departamento.

Mapa interactivo SVG de Colombia

Visualización de los departamentos.

Al hacer clic en un departamento se muestran estadísticas:

Cantidad de acueductos.

Número de funcionarios registrados.

Promedios de pH, cloro y bacterias.

Consultas estadísticas en tiempo real (JSON)

Número de acueductos por departamento.

Promedios de calidad del agua (pH, cloro, bacterias) por departamento.

---

Tecnologías utilizadas

Backend: Flask (Python)

Base de datos: MySQL con flask-mysqldb

Seguridad: werkzeug.security (hash de contraseñas)

Frontend: HTML, CSS, Jinja2 Templates

Interactividad: JavaScript + SVG map

Otros: Flask Sessions, Flash messages

---

Próximas mejoras

Geolocalización real de acueductos en mapas dinámicos (Leaflet o Mapbox).

Sistema de roles (administrador, analista, usuario básico).

Diseño responsive con un framework frontend (Bootstrap / TailwindCSS).

Exportación de reportes en PDF/Excel.

---

Autores

Braulio Castro (BraulioDev420)

Proyecto académico orientado a la gestión de recursos hídricos y control de calidad del agua.

---
