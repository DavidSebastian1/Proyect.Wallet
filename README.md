# 🇪🇸 Proyecto Wallet Online

¡Hola! Bienvenid@ a mi mayor proyecto personal hasta ahora, creado **100% desde 0**.

Este programa simula un **Wallet online** donde puedes:
* Agregar y/o retirar la cantidad de USD que desees.
* Consultar tu saldo total en tiempo real.
* Comparar su valor con cualquier moneda del mundo mediante una API (ej: VES, COP, CNY, EUR).

## Fundamentos de Python Aplicados

* **API Privada:** Uso de `exchangerate-api` integrada mediante las librerías `config` (para seguridad de la API_KEY) y `requests`.
* **Programación Orientada a Objetos (OOP):** Clase `Coin` para simplificar funciones y manejo de variables mediante un constructor `__init__(self, ...)`.
* **Control de Flujo:** Bucles `while` y condicionales que permiten el uso indefinido del programa hasta que el usuario decida salir.

## 🛠️ ¿Cómo usar el programa?

1. Accede a [exchangerate-api.com](https://www.exchangerate-api.com/) para obtener tu llave gratuita.
2. Crea un archivo `config.py` con tu `API_KEY`.
3. ¡Ejecuta `proyect.py` y disfruta!

