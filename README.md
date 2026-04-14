

---

# Proyecto de Ciencia de Datos

## Limpieza y Transformación de Datos de Actividad Física

---

## Integrantes

Viente Castro

Julian Martínez

Lucas Fernandez

---

## Descripción del Proyecto

El presente proyecto tiene como objetivo transformar un dataset en estado "crudo" en un conjunto de datos limpio, estructurado y listo para su análisis.

Se aplicaron técnicas fundamentales de ciencia de datos, incluyendo limpieza, transformación mediante pipelines y generación de nuevas variables (feature engineering).

---

## Dataset

* **Tipo de datos:** Actividad física (cantidad de pasos por hora)
* **Formato:** CSV
* **Origen:** Dataset obtenido de plataformas abiertas como Kaggle

### Modificación del Dataset

El dataset original se encontraba en condiciones limpias, por lo que se decidió introducir artificialmente:

* Valores nulos
* Registros duplicados

**Justificación:**
Esto permitió simular un escenario real de trabajo en ciencia de datos, donde los datos suelen presentar inconsistencias.

---

## Objetivos

* Limpiar el dataset eliminando errores e inconsistencias
* Transformar los datos utilizando herramientas automatizadas
* Generar nuevas variables relevantes
* Obtener un dataset final listo para análisis o modelamiento

---

## Metodología

El desarrollo del proyecto se estructuró en las siguientes etapas:

### 1. Diagnóstico Inicial

Se realizó un análisis exploratorio para identificar problemas en los datos:

* Detección de valores nulos
* Identificación de duplicados
* Revisión de tipos de datos

---

### 2. Limpieza de Datos

#### Eliminación de duplicados

Se utilizó la función `drop_duplicates()` para eliminar registros repetidos.

**Justificación:**
Los duplicados pueden generar sesgos en el análisis y afectar los resultados.

---

#### Eliminación de valores nulos

Se aplicó `dropna()` para eliminar filas con datos faltantes.

**Justificación técnica:**
El tamaño del dataset permitió eliminar registros sin afectar su representatividad.

---

### 3. Feature Engineering (Ingeniería de Variables)

Se crearon nuevas variables a partir de la columna temporal:

* **Hora:** permite analizar patrones diarios
* **Día:** permite analizar comportamiento semanal
* **FinDeSemana:** variable binaria para identificar fines de semana

**Justificación:**
Estas variables enriquecen el dataset y permiten detectar patrones más complejos.

---

### 4. Transformación de Datos (Pipeline)

Se implementó un pipeline utilizando `scikit-learn`, que incluye:

* `SimpleImputer` (imputación de valores faltantes)
* `StandardScaler` (normalización de datos)

**Justificación técnica:**

* Automatiza el proceso de transformación
* Asegura reproducibilidad
* Sigue buenas prácticas de la industria

---

### 5. Visualización

Se generaron gráficos para analizar el comportamiento de los datos:

* Promedio de pasos por hora
* Promedio de pasos por día

**Justificación:**
Las visualizaciones permiten identificar patrones que no son evidentes mediante estadísticas descriptivas.

---

## Resultados

### Antes

* Dataset con valores nulos y duplicados
* Variables limitadas

### Después

* Dataset limpio y consistente
* Nuevas variables creadas
* Datos escalados
* Listo para análisis o machine learning

---

## Tecnologías Utilizadas

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Google Colab

---

## Justificación del Entorno

Se utilizó **Google Colab** como entorno de desarrollo debido a:

* No requiere instalación local
* Permite trabajar en la nube
* Facilita la colaboración
* Integración directa con GitHub

---

## Estructura del Proyecto

```
data/
 |-- raw/
 |   `-- hourlySteps_sucio.csv
 |-- processed/
 |   `-- hourlySteps_clean.csv

README.md
informe_tecnico_defi.docx
proyecto_cd_final.ipynb
```

---

## Reproducibilidad

El proyecto está diseñado para ser completamente reproducible:

1. Clonar el repositorio
2. Abrir el notebook en Google Colab
3. Ejecutar todas las celdas

---

## Conclusión

Se logró transformar un dataset en estado crudo en uno limpio y estructurado, aplicando técnicas fundamentales de ciencia de datos.

El proceso desarrollado sigue un flujo real de trabajo en la industria, asegurando calidad, reproducibilidad y valor analítico en los datos.

---

## Autor

Proyecto desarrollado como parte del curso de Programación para la Ciencia de Datos.
