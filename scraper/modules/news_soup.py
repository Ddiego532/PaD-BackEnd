from collections.abc import Sequence
# from typing import Any
from bs4 import BeautifulSoup, Tag
from bs4.builder import TreeBuilder
from bs4.element import PageElement as PageElement, SoupStrainer as SoupStrainer
from .helpers import get_kv_by_string
import json

# JSON handling for schemas.
MALFORMED_JSON = -1
GOOD_JSON = 1

# parsing mode for news.
PARSE_MODE = "lxml"

class NewsSoup(BeautifulSoup):
    """
    Clase heredada de BeautifulSoup que permite poder realizar más operaciones  

    como obtener los esquemas JSON y encontrar elementos por criterios.
    """
    def __init__(self, markup: str | bytes = "", builder: TreeBuilder | type[TreeBuilder] | None = None, 
                parse_only: SoupStrainer | None = None, from_encoding: str | None = None, exclude_encodings: Sequence[str] | None = None, 
                element_classes: dict[type[PageElement], type] | None = None, **kwargs) -> None:
        """
        Constructor del parseador de noticias.

        params:
            markup : str | bytes : El contenido HTML para poder parsearlo.
            from_encoding : str | None: El encoding a utilizar en el parsing.
        """
        super().__init__(markup=markup, features=PARSE_MODE, builder=builder, parse_only=parse_only,
                        from_encoding=from_encoding, exclude_encodings=exclude_encodings, element_classes=element_classes, **kwargs)

    def get_schema(self) -> tuple[dict | str, int]:
        """
        Obtiene el schema utilizado por los motores de búsqueda en formato JSON o texto.

        :returns:
            - esquema : dict | str - El esquema de la pagina.
            - estado : int - El codigo de estado de la obtención de esquema, -1 si es malformado, 1 si está ok.
        """
        json_app = self.find("script", {"type": "application/ld+json"})
        data : dict = None
        
        text = ""

        if json_app:
            text = json_app.text

            try:
                data = json.loads(text)
                return data, GOOD_JSON
            except json.JSONDecodeError as e:
                print(f"Can't decode JSON because its malformed. Returning in string value.\nReason: {e}")

        return text, MALFORMED_JSON
    def get_schema_attribute(self, attrib : str) -> str:
        """
        Obtiene un atributo del esquema de la pagina.

        :params:
            attrib : str - El atributo a buscar.

        :returns:
            atributo : str | None - El valor del atributo.
        """
        schema, status = self.get_schema()
        
        if isinstance(schema, list):
            schema = schema[0]

        if status == MALFORMED_JSON:
            return get_kv_by_string(attrib, schema)

        return schema.get(attrib, None)
    
    def find_element_by_identifier_attribute(self, data : dict) -> Tag:
        """
        Busca elementos en la pagina con el atributo que lo identifica, pueden ser ids, clases, entre otros.

        :params:
            data : dict - El diccionario de los datos del elemento a buscar, el diccionario debe tener las siguientes keys

            "tag": La etiqueta del elemento.

            "identifier_attrib": El atributo que identifica al elemento. Ya sea una clase o una id.

            "attrib_value": El valor del atributo.

        :returns:
            nodo : Tag | NavigableString | None: El nodo que corresponde al elemento buscado.
        """
        id = data.get("identifier_attrib", None)

        #if id is None:
            #raise ValueError("Identifier can't be null.")
        
        id_value = data.get("attrib_value")
        return self.find(data["tag"], {id : id_value})

    def __find_tag_by_parent(self, data : dict) -> Tag:
        """
        Obtiene un tag usando los datos de su padre.

        :params:
            data : dict - El diccionario que contiene los datos del padre y el tag del hijo.

        :returns:
            found_elem : Tag | NavigableString | None - El nodo que contiene al elemento buscado.
        """
        parent_data = data.get("parent", None)
        found_elem = None
    
        if parent_data:
            parent_elem = self.find_element_by_identifier_attribute(parent_data)
            found_elem = parent_elem and parent_elem.find(data["tag"])

        return found_elem

    def find_tag_by_criteria(self, data : dict) -> Tag:
        """
        Busca un nodo en la página con un criterio especifico.

        Ya sea por una etiqueta especial o por el padre.

        :params:
            data : dict - El diccionario que contiene el criterio.

            Es necesario especificar el "tag" ya que de lo contrario podría arrojar errores.

            Si el tag especificado es un script, entonces se tendrá que especificar un atributo asociado al esquema de la página (schema_attrib).

            Si lo que se busca es un padre, solamente hay que especificar el tag.

        :returns:
            html_tag : Tag - La etiqueta solicitada.
        """
        curr_tag : str = data["tag"]

        if curr_tag == "script":
            return self.get_schema_attribute(data["schema_attrib"])
        
        parent_elem = self.__find_tag_by_parent(data)

        # no parent so use directly the attribute.
        if parent_elem is None:
            return self.find_element_by_identifier_attribute(data)
        
        return parent_elem

    def get_meta_content(self, key : str, val : str) -> str | list[str] | None:
        """
        Obtiene el contenido de una etiqueta <meta> a través de su llave-valor.

        :params:
            key : str - La llave a buscar.
            val : str - El valor que contiene esa llave.

        :returns:
            content : str | list[str] - Los contenidos.
        """
        meta = self.find("meta", {key : val})
        return meta.get("content") if meta else None

    def get_meta_og_content(self, prop : str):
        """
        Busca en las etiquetas meta que posean una propiedad de tipo "og".

        :params:
            property : str - La propiedad a buscar.
        returns:
            content : str | None - El contenido de la etiqueta meta seleccionada.
        """
        return self.get_meta_content("property", f"og:{prop}")
    
    def get_meta_article_content(self, prop : str):
        """
        Busca en las etiquetas meta que posean una propiedad de tipo "article".

        :params:
            property : str - La propiedad a buscar.
        returns:
            content : str | None - El contenido de la etiqueta meta seleccionada.
        """
        return self.get_meta_content("property", f"article:{prop}")