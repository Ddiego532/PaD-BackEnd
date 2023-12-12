# PaD-BackEnd
BackEnd del sistema de recuperacion de informacion Politica al Dia

## Urls
```/all_news/```
```/get_by_polarity/{polarity}```

Siendo Positivo, Neutro y Negativo las 3 posibles polaridades.

Vez inciado y corriendo el proyecto es necesario añadir a la url esta direccion para obtener los resultados de la api.

## Para el desarrollo del proyecto
Para la realizacion del proyecto estaremos desarrollando una api rest con FastApi. 

Es necesario clonar el repositorio ya sea con Git o con GitHub Desktop y abrir el directorio con su editor de texto favorito.

## Creación del Virtualenv

Para mantener un entorno de desarrollo aislado, se recomienda el uso de un entorno virtual. Si no tienes `virtualenv` instalado, puedes hacerlo con el siguiente comando:

```bash
pip install virtualenv
```
Una vez ya instalado debemos de crear un entorno virtual con el siguiente comando

```bash
virtualenv venv
```
Ya teniendo creado el entorno virtual de trabajo podemos acceder con el siguiente comando

```bash
.\venv\Scripts\activate
```
En algunos casos es posible que se presente un mensaje de error relacionado a las politicas de ejecucion de scripts, por lo que en caso de presentarse este problema debemos introducir este comando en la misma terminal.

```bash
Set-ExecutionPolicy Unrestricted -Scope Process
```
Este comando nos permite ejecutar bypassear la seguridad unicamente dentro de la misma terminal, por lo que en situaciones futuras es necesario ingresar el comando nuevamente para ingresar al venv. Pero si se desea ingresar una sola vez simplemente remover ```-Scope Process```.

Ya una vez dentro del entorno virtual debería aparecer ``(venv)`` en la consola de comandos. Solo continuar en caso de que ese sea el caso.

## Instalación de librerías y paquetes necesarios para el desarrollo de la aplicacion*
En una consola de comandos, ejecutar:
```
pip install -r requirements.txt
```
Con esto ya tendriamos todo lo necesario para trabajar en el proyecto.

## Correr el proyecto
Para correr el proyecto es necesario introducir lo siguiente en la terminal de comandos:
```
uvicorn api.main_api:app
```
Se le comunicara por la misma terminal la direccion local para ingresar.


