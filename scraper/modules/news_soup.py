from collections.abc import Sequence
# from typing import Any
from bs4 import BeautifulSoup, Tag
from bs4.builder import TreeBuilder
from bs4.element import PageElement as PageElement, SoupStrainer as SoupStrainer
from .constants import PARSE_MODE, GOOD_JSON, MALFORMED_JSON
from .helpers import get_kv_by_string, get_tags_from_str
import json

class NewsSoup(BeautifulSoup):
    """
    Clase heredada de BeautifulSoup que permite poder realizar más operaciones  

    como obtener los esquemas JSON y encontrar elementos por criterios.
    """
    def __init__(self, markup: str | bytes = "", builder: TreeBuilder | type[TreeBuilder] | None = None, parse_only: SoupStrainer | None = None, from_encoding: str | None = None, exclude_encodings: Sequence[str] | None = None, element_classes: dict[type[PageElement], type] | None = None, **kwargs) -> None:
        """
        Constructor del parseador de noticias.

        params:
            markup : str | bytes : El contenido HTML para poder parsearlo.
            from_encoding : str | None: El encoding a utilizar en el parsing.
        """
        super().__init__(markup=markup, features=PARSE_MODE, builder=builder, parse_only=parse_only,
                        from_encoding=from_encoding, exclude_encodings=exclude_encodings, element_classes=element_classes, **kwargs)

    def get_schema(self):
        """
        Obtiene el schema utilizado por los motores de búsqueda en formato JSON o texto.

        :returns:
            - esquema : dict | str - El esquema de la pagina.
            - estado : int - El codigo de estado de la obtención de esquema, -1 si es malformado, 1 si está ok.
        """
        json_app = self.find("script", {"type": "application/ld+json"})
        data : dict = None

        if json_app:
            text = json_app.text

            try:
                data = json.loads(text)
                return data, GOOD_JSON
            except json.JSONDecodeError as e:
                print(f"Can't decode JSON because its malformed. Returning in string value.\nReason: {e}")

        return text, MALFORMED_JSON
    def get_schema_attribute(self, attrib : str):
        """
        Obtiene un atributo del esquema de la pagina.

        :params:
            attrib : str - El atributo a buscar.

        :returns:
            atributo : str | None - El valor del atributo.
        """
        schema, status = self.get_schema()

        if status == MALFORMED_JSON:
            return get_kv_by_string(attrib, schema)

        return schema.get(attrib, None)
    
    def find_element_by_identifier_attribute(self, data : dict):
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

        if id is None:
            raise ValueError("Identifier can't be null.")
        
        id_value = data.get("attrib_value")
        return self.find(data["tag"], {id : id_value})

    # TODO: Document it.
    def find_tag_by_criteria(self, data : dict):
        curr_tag : str = data["tag"]

        if curr_tag == "script":
            return self.get_schema_attribute(data["schema_attrib"])

        # parents can give the way we retrieve the data.
        parent_data = data.get("parent", None)

        if parent_data is None:
            return self.find_element_by_identifier_attribute(data)

        parent_element = self.find_element_by_identifier_attribute(parent_data)

        # nested ahh thing
        if parent_element:
            first = parent_element.find(curr_tag)

            if first is not None:
                return first
            
        # no parent so use fallback.
        fallback_data : dict = data.get("fallback", None)

        if fallback_data:
            fallback_tag = self.find_element_by_identifier_attribute(fallback_data)

            return fallback_tag.find(curr_tag)
        
        # worst case.
        return None
    
    def get_meta_content(self, key : str, val : str) -> list[PageElement] | None:
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


        

        

    