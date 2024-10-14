# Informe: Instalación de Python y Ejecución de un Script con PyInstaller

## 1. Instalación de Python
1. **Descargar Python**:
   - Visitar la página oficial de Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Descargar la última versión de Python 3.x.

2. **Instalar Python**:
   - Ejecutar el instalador descargado.
   - Seleccionar la opción `Add Python to PATH` para facilitar el uso de Python desde la terminal.
   - Completar la instalación siguiendo las instrucciones del asistente.

3. **Verificar la instalación**:
   - Abrir la terminal (CMD en Windows).
   - Ejecutar el siguiente comando para verificar la versión instalada:
     ```bash
     python --version
     ```
   - Para verificar `pip` (el administrador de paquetes de Python):
     ```bash
     pip --version
     ```

## 2. Instalación de Paquetes Requeridos
1. **Navegar al directorio del proyecto**:
   - Abrir la terminal y cambiar al directorio donde se encuentra el archivo `initpdf.py`:

2. **Instalar las dependencias**:
   - Ejecutar los siguientes comandos para instalar los paquetes requeridos:
     ```bash
     pip install pandas fpdf PyQt5 mplcursors
     ```

3. **Solucionar problemas de instalación de PyQt5**:
   - Si aparece un error relacionado con `Microsoft Visual C++ 14.0`, instalar las herramientas de construcción desde:
     [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)


## 3. Empaquetar el Script con PyInstaller

1. **Instalar PyInstaller**:
   - Si aún no lo has hecho, instala `PyInstaller` ejecutando:
     ```bash
     pip install pyinstaller
     ```

2. **Crear el ejecutable**:
   - Navegar al directorio donde se encuentra tu script `initpdf.py`:
   - Ejecutar `PyInstaller` para crear un ejecutable en modo de archivo único:
     ```bash
     pyinstaller --onefile initpdf.py
     ```
   - Esto generará una carpeta `dist` dentro de la cual encontrarás el archivo ejecutable `initpdf.exe`.

3. **Opciones adicionales de PyInstaller**:
   - **Incluir el modo ventana** (sin mostrar la consola, útil para aplicaciones con GUI):
     ```bash
     pyinstaller --onefile --windowed initpdf.py
     ```
   - **Incluir un ícono personalizado** para el ejecutable:
     ```bash
     pyinstaller --onefile --icon=icono.ico initpdf.py
     ```
   - **Incluir el modo de depuración** para ver mensajes de error y logs durante la ejecución:
     ```bash
     pyinstaller --onefile --debug initpdf.py
     ```

4. **Archivos generados por PyInstaller**:
   - Al ejecutar `PyInstaller`, se crean varias carpetas y archivos:
     - `dist/`: Contiene el archivo ejecutable (`initpdf.exe`).
     - `build/`: Archivos temporales utilizados durante el proceso de empaquetado.
     - `initpdf.spec`: Archivo de especificaciones que define cómo se empaquetó el script. Puede ser útil para personalizar el empaquetado en futuras ejecuciones.

5. **Probar el ejecutable**:
   - Ir a la carpeta `dist` donde se generó el ejecutable:
     ```bash
     cd dist
     ```
   - Ejecutar el archivo `initpdf.exe`:
     ```bash
     ./initpdf.exe
     ```
   - Si el programa se cierra de inmediato, ejecutarlo desde la terminal para ver los mensajes de error:
     ```bash
     initpdf.exe
     ```

   - Si hay errores, puedes redirigir la salida a un archivo de texto para revisarlos:
     ```bash
     initpdf.exe > salida.txt 2>&1
     ```

6. **Ejemplos de uso**:
   - **Crear un ejecutable con ícono y sin consola**:
     ```bash
     pyinstaller --onefile --windowed --icon=icono.ico initpdf.py
     ```
   - **Crear un ejecutable con depuración habilitada**:
     ```bash
     pyinstaller --onefile --debug all initpdf.py
     ```



## 4. Solución de Problemas Comunes
1. **Error: `ModuleNotFoundError`**:
   - Si se muestra un error como `ModuleNotFoundError: No module named 'pandas'`, asegúrate de que `pandas` esté instalado:
     ```bash
     pip install pandas
     ```

2. **Error: `pip` no es reconocido**:
   - Asegúrate de que Python esté agregado al `PATH`:
     - Ir a `Sistema > Configuración avanzada del sistema > Variables de entorno`.
     - Asegurarse de que el directorio de `python` y `Scripts` estén en la variable `PATH`.

3. **Problemas al ejecutar el ejecutable**:
   - Si el ejecutable se cierra inmediatamente, puedes redirigir la salida a un archivo de texto para revisar errores:
     ```bash
     initpdf.exe > salida.txt 2>&1
     ```

## 5. Referencias
- [Página de Descarga de Python](https://www.python.org/downloads/)
- [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- [Documentación de PyInstaller](https://pyinstaller.readthedocs.io/)

