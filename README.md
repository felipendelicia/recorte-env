# Recorte-Env - Document Scanner

Una aplicación de escritorio para escaneo de documentos construida con Python y OpenCV. Permite detectar automáticamente documentos en imágenes, aplicar corrección de perspectiva y guardar los resultados.

## Características

- **Detección automática de documentos**: Utiliza contornos y transformación de perspectiva para detectar y enderezar documentos
- **Interfaz interactiva**: Ventana maximizada para visualización cómoda de resultados
- **Ajustes manuales**: 
  - Selección de región de interés (ROI)
  - Corrección de perspectiva mediante selección de 4 puntos
  - Rotación libre (incrementos de 1°)
  - Volteo horizontal y vertical
  - Rotaciones de 90° en cualquiera de las direcciones
- **Procesamiento por lotes**: Procesa todas las imágenes de una carpeta seleccionada
- **Guardado selectivo**: Guarda solo las imágenes que el usuario elija

## Requisitos

- Python 3.x
- Bibliotecas de Python:
  - OpenCV (`opencv-python`)
  - NumPy (`numpy`)
  - Pillow (`pillow`)

Instale las dependencias con:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecute la aplicación:
   ```bash
   python main.py
   ```
   o alternativamente:
   ```bash
   python scripts/run_scanner.py
   ```

2. Seleccione una carpeta que contenga imágenes (JPG, JPEG, PNG)

3. Para cada imagen:
   - La aplicación mostrará el resultado del escaneo automático
   - Controles disponibles:
     - `a`: Guardar la imagen procesada en la subcarpeta "salida"
     - `r`: Abrir modo de ajuste manual
     - `s`: Saltar a la siguiente imagen
     - `q`: Salir de la aplicación

4. En el modo de ajuste manual:
   - `c`: Seleccionar región de interés (ROI) rectangular
   - `p`: Corregir perspectiva seleccionando 4 puntos
   - `l`: Rotar 90° en sentido horario
   - `j`: Rotar 90° en sentido antihorario
   - `f`: Voltear horizontalmente
   - `v`: Voltear verticalmente
   - `i`: Incrementar ángulo de rotación (+1°)
   - `u`: Decrementar ángulo de rotación (-1°)
   - `q`: Aceptar cambios y volver al menú principal

## Estructura del proyecto

```
recorte-env/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Este archivo
├── scanner/                # Módulos principales
│   ├── core.py             # Funciones de detección y transformación
│   └── gui.py              # Componentes de interfaz de usuario
└── scripts/
    └── run_scanner.py      # Punto de entrada alternativo
```

## Funcionamiento interno

1. **Detección de documentos**:
   - Conversión a escala de grises y desenfoque gaussiano
   - Detección de bordes con algoritmo Canny
   - Operación morfológica de cierre para conectar componentes
   - Búsqueda de contornos y filtrado por área mínima
   - Aproximación poligonal para detectar cuadriláteros
   - Ordenamiento de puntos y transformación de perspectiva

2. **Interfaz de usuario**:
   - Built with OpenCV's highgui and Tkinter para diálogos de archivos
   - Ventanas maximizadas para mejor experiencia de usuario
   - Manejo de eventos de mouse para selección interactiva de puntos

## Contribuir

Si deseas contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Felipe - [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)

Enlace del proyecto: [https://github.com/tu-usuario/recorte-env](https://github.com/tu-usuario/recorte-env)