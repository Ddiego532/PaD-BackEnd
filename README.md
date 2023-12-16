# PaD-BackEnd
BackEnd del sistema de recuperacion de informacion Politica al Dia

## Correr el proyecto

Desde la carpeta correr:

```
python api/main_api.py
```
```
python ranking/answer_server.py
```

Se le comunicara por la misma terminal la direccion local para ingresar.


## Urls
```/all_news/```
```/get_by_polarity/{polarity}```
```/search/{query}```

Siendo Positivo, Neutro y Negativo las 3 posibles polaridades.

Para la query, se debe ingresar el string de busqueda. Ej: /search/boric. 

```/search/{query}``` retorna una lista con todas las noticias que resultan de la busqueda.

Vez inciado y corriendo el proyecto es necesario añadir a la url esta direccion para obtener los resultados de la api.
