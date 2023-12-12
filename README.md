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
```/query/{query}```
```/json/{query}```

Siendo Positivo, Neutro y Negativo las 3 posibles polaridades.

Para la query, se debe ingresar el string de busqueda entre los corchetes. 

"/query/{query}" retorna el index del documento y el ranking
"json/{query}" retorna las noticias segun el ranking.

Vez inciado y corriendo el proyecto es necesario añadir a la url esta direccion para obtener los resultados de la api.
