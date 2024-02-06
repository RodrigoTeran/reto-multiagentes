# Multiagentes y Gráficas Computacionales

Este repositorio contiene nuestro proyecto final de Multiagentes y Gráficas Computacionales, dónde buscamos simular un caso real de una intersección cuyo flujo no es siempre constante, por lo que usamos multiagentes para ayudar a mejorar el flujo en dicha intersección.

## Instalación del proyecto

Para poder correr este proyecto se necesita al menos `python 3.10`. Puedes descargarlo [aquí](https://www.python.org/downloads/). Comenzamos instalando las dependencias necesarias:

```console
pip install -r requirements.txt
```

Después, para poder correr la simulación basta con ejecutar el siguiente comando:

```console
python reto/main.py
```

## Configuración de la simulación

La simulación ofrece una API pequeña que permite configurar ciertos parametros. Estos parametros se encuentran dentro del objeto `parameters` en el archivo `reto/simulation.py`. La configuración tiene los siguientes parámetros

- `steps`: La cantidad de pasos en la simulación
- `vehicles`: El rango de carros que se generan en cada oleada (1 - vehicles)
- `vehicle_rate`: La distribución de los carros en cada una de las direcciones
- `cooldown`: Tiempo entre cada oleada de generación de carros (mejor mantener en 0)
