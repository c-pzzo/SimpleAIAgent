# SimpleAIAgent
Este consiste en crear un pequeño AI Agent que lea la información de cualquier página web, encuentre la opción de facturar, vaya a la página de facturación y llene automáticamente el primer formulario encontrado con información aleatoria.

# Pasos

## 1. El agente debe de Navegar a las tres páginas web (procesos separados):

- [https://www.dath.com.mx/](https://www.dath.com.mx/)
- [https://www.monparis.mx](https://www.monparis.mx)
- [https://www.alsea.com.mx/factura-electronica.html](https://www.alsea.com.mx/factura-electronica.html)

## 2. Extraer información con Computer Vision:

- Leer la información visible en la página.
- Navegar la página y encontrar el botón de facturación.
- Seguir las instrucciones de la página hasta llegar al formulario de facturación.

## 3. Llenar el formulario con datos aleatorios:

- Completar los campos requeridos en el sitio web con valores generados aleatoriamente.
  - Número de referencia
  - Monto
  - RFC
  - Información fiscal
  - Fecha

## 4. Enviar el formulario:

- Hacer clic en el botón **"Siguiente"** tras completar el formulario.

---

# Requerimientos

- La solución debe estar escrita en **Python 3.12** o superior.
- La ejecución debe realizarse dentro de un **contenedor de Docker**.
- La navegación web debe realizarse con **Playwright** ([documentación](https://playwright.dev/)).
- Se debe incluir **documentación clara** sobre cómo instalar, ejecutar y usar la solución.
- **No usar agentes de IA preconstruidos o bibliotecas que automaticen completamente la tarea** (como `browseruse` o `stagehand`).

# Google Services
- Gemini API
- Firestore
- Google Cloud Storage
- Secrets Manager
- Google Cloud Build
- Google Cloud Run