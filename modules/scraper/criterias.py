# atm we use the general politics.
# TODO: Swap forbidden_paths to accepted_paths.

# EL MOSTRADOR HANDLER.
# FORMATO DE SELECTOR.

MEGANOTICIAS_SELECTOR = {
    "text_data": {
        "title": {
            # considering use the meta tag.
            "parent": {
                "tag": "div",
                "identifier_attrib": "class",
                "attrib_value": "contenedor-contenido",
            },

            "tag": "h1",
        },

        "date": {
            "parent": {
                "tag": "div",
                "identifier_attrib": "class",
                "attrib_value": "fechaHora",
            },

            "tag": "time",
        }
    },

    "content": {"tag": "div", "identifier_attrib": "class", "attrib_value": "contenido-nota"},
    "news_tags": {"tag": "div", "identifier_attrib": "class", "attrib_value": "contenedor-temas"},

    "common_irrelevant_tags": {
        "tags": ["div", "a"],
        "classes": ["relacionados", "btn-temas evento-TodoSobre"]
    }
}

ELMOSTRADOR_NEWS_SELECTOR = {
    "text_data": {
        "title": {"tag": "h1", "identifier_attrib": "class", "attrib_value": "d-the-single__title | common:margin-bottom-25"},
        "date": {"tag": "time", "identifier_attrib": "class", "attrib_value": "d-the-single__date | common:margin-bottom-20"},
        "subtitle": {"tag": "p", "identifier_attrib": "class", "attrib_value": "d-the-single__excerpt | u-fw-600"},
    },

    # i have an idea.
    "content": {"tag": "div", "identifier_attrib": "class", "attrib_value": "d-the-single-wrapper__text"},
    # so different!!!!!!!!!
    "news_tags": {"tag": "div", "identifier_attrib": "class", "attrib_value": "the-section__body | common:margin-top-30"}
}

TVN_SELECTOR = {
    "text_data": {
        "title": {"tag": "h1", "identifier_attrib": "id", "attrib_value": "#contenido-ppal"},
        "date": {"tag": "p", "identifier_attrib": "class", "attrib_value": "fecha"},
        "subtitle": {"tag": "p", "identifier_attrib": "class", "attrib_value": "baj"},
    },

    "content": {"tag": "div", "identifier_attrib": "class", "attrib_value": "CUERPO"},
    "common_irrelevant_tags": {"tags": ["div"], "classes": ["prontus-card-container"]},
    "news_tags": {"tag": "ul", "identifier_attrib": "class", "attrib_value": "tags"},
}

CNN_SELECTOR = {
    "text_data": {
        "title": {"tag": "h1", "identifier_attrib": "class", "attrib_value": "main-single-header__title"},
        "date": {"tag": "span", "identifier_attrib": "class", "attrib_value": "main-single-about__item main-single__date"},
        "subtitle": {"tag": "div", "identifier_attrib": "class", "attrib_value": "main-single-header__excerpt"}
    },

    "content": {"tag": "div", "identifier_attrib": "class", "attrib_value": "main-single-body__content"},
    "news_tags": {"tag": "div", "identifier_attrib": "class", "attrib_value": "the-tags__list"}
}

LATERCERA_SELECTOR = {
    "text_data": {"title": {"tag": "div", "identifier_attrib": "class", "attrib_value": "hl"},
                  "date": {"tag": "time", "identifier_attrib": "class", "attrib_value": "p-left-10"},
                  "subtitle": {"tag": "p", "identifier_attrib": "class", "attrib_value": "excerpt"}},
    "content": {"tag": "div", "identifier_attrib": "class", "attrib_value": "single-content"},
    "common_irrelevant_tags": {"tags": ["aside", "div"], "classes": ["offer-content", "links | story_links"]},
    "news_tags": {"tag": "ul", "identifier_attrib": "class", "attrib_value": "list-cat-y-tags"},
}

TELETRECE_SELECTOR = {
    "text_data": {"title": {"tag": "h1", "identifier_attrib": "class", "attrib_value": "article-component__header-title"},
                  "subtitle": {"tag": "div", "identifier_attrib": "class", "attrib_value": "article-component__lead"},
                  "date": {"tag": "time", "identifier_attrib": "itemprop", "attrib_value": "datePublished"}},

    "content": {"tag": "div", "identifier_attrib": "id", "attrib_value": "article-body-wrapper"},

    "common_irrelevant_tags": {
        "tags": ["div"],
        "classes": ["article-component__read"],
    },

    "news_tags": {
        "parent": {
            "tag": "div", 
            "identifier_attrib": "class", 
            "attrib_value": "tag-list__wrapper"
        },

        "tag": "ul",
    }
}

BIOBIOCHILE_SELECTOR = {
    "text_data": {
        "title" : {"tag": "h1", "identifier_attrib": "class", "attrib_value": "post-title"},
        "subtitle": {"tag": "div", "identifier_attrib": "class", "attrib_value": "post-excerpt"},
        "date": {"tag": "div", "identifier_attrib": "class", "attrib_value": "post-date"}
    },

    "content": {
        "tag": "div",
        "identifier_attrib": "class",
        "attrib_value": "post-content clearfix",
    },

    "common_irrelevant_tags": {
        # we used the excerpt at this time so we can delete it easily.
        "tags": ["div", "div"],
        "classes": ["lee-tambien-bbcl", "post-excerpt"]
    }
}

COOPERATIVA_SELECTOR = {
    "text_data": {
        "title": {"tag": "h1", "identifier_attrib": "class", "attrib_value": "titular titular-audio"},
        "subtitle": {"tag": "div", "identifier_attrib": "class", "attrib_value": "texto-bajada"},
        "date": {
            "parent": {
                "tag": "div",
                "identifier_attrib": "class",
                "attrib_value": "fecha-publicacion"
            },

            "tag": "time",
        }
    },

    "content": {
        "tag": "div",
        "identifier_attrib": "id",
        "attrib_value": "cuerpo-ad",
    },

    "common_irrelevant_tags": {
        "tags" : ["div"],
        "classes": ["modulo-lee"],
    },

    "news_tags": {
        "tag": "div",
        "identifier_attrib": "class",
        "attrib_value": "rotulo-topicos",
    }
}

ELDINAMO_SELECTOR = {
    "text_data": {
        "title": {
            "parent": {
                "tag": "article",
                "identifier_attrib": "class",
                "attrib_value": "principal",
            },
            "tag": "h1",
        },

        "subtitle": {
            "tag": "p",
            "identifier_attrib": "class",
            "attrib_value": "bajada",
        },

        "date": {
            "tag": "span",
            "identifier_attrib": "class",
            "attrib_value": "fecha",
        },
    },

    "content": {
        "tag": "div",
        "identifier_attrib": "class",
        "attrib_value": "the-content",
    },

    "common_irrelevant_tags": {
        "tags": ["aside"],
        "classes": ["bloque-tc-tres-recomendados"]
    },

    "news_tags": {
        "tag": "div",
        "identifier_attrib": "class",
        "attrib_value": "tags",
    }
}

ASCOM_SELECTOR = {
    "text_data": {
        "title": {
            "tag": "h1",
            "identifier_attrib": "class",
            "attrib_value": "art__hdl__tl",
        },

        "subtitle": {
            "tag": "h2",
            "identifier_attrib": "class",
            "attrib_value": "art__hdl__opn",
        },

        "date": {
            "parent": {
                "tag": "div",
                "identifier_attrib": "class",
                "attrib_value": "art__by__aux"
            },

            "tag": "time",
        }
    },

    "content": {
        "tag": "div",
        "identifier_attrib": "class",
        "attrib_value": "art__m-cnt",
    },

    "news_tags": {
        "tag": "nav",
        "identifier_attrib": "class",
        "attrib_value": "art__tags",
    },

    "common_irrelevant_tags": {
        "tags": ["div", "figcaption"],
        "classes": ["ext ext-embed", "mm__cap"]
    }
}

TELETRECE = {
    "url": "https://www.t13.cl/politica",
    "tag": "div",
    "identifier_attrib": "class",
    "attrib_value": "topic-landing-news__list view-content",
    "forbidden_paths": ["/videos/"],
    "news_selector": TELETRECE_SELECTOR,
}

ELMOSTRADOR = {
    # reverted this guy again.
    "url": "https://www.elmostrador.cl/categoria/pais/",
    "tag": "section",
    "identifier_attrib": "id",
    "attrib_value": "claves",
    # num goes here.
    "explore_path": "categoria/pais/page/page_num/",
    "forbidden_paths": ["/autores/", "/autor/", "/page/", "/multimedia/", "/opinion/"],

    "news_selector": ELMOSTRADOR_NEWS_SELECTOR
}

BIOBIOCHILE = {
    # politica esta lleno de cosas random xd
    "url": "https://www.biobiochile.cl/lista/categorias/nacional",
    "tag": "div",
    "identifier_attrib": "class",
    "attrib_value": "section-body",
    "forbidden_paths": ["/autores/", "/biobiotv/", "/opinion/", "/especial/"],
    "news_selector": BIOBIOCHILE_SELECTOR
}

LATERCERA = {
    "url": "https://www.latercera.com/categoria/politica/page/1",
    "tag": "section",
    "identifier_attrib": "class",
    "attrib_value": "top-mainy",
    "explore_path": "categoria/politica/page/page_num/",
    "news_selector": LATERCERA_SELECTOR,
    "forbidden_paths": ["/autor/", "/categoria/"]
}

CNNCHILE = {
    "url": "https://www.cnnchile.com/tag/politica/",
    "tag": "div",
    "identifier_attrib": "class",
    "attrib_value": "inner-list",
    "explore_path": "tag/politica/page/page_num/",
    "forbidden_paths": ["/lodijeronencnn/", "/opinion/", "/programas-completos/", "/mundo/", "/tag/"],
    "news_selector": CNN_SELECTOR
}

MEGANOTICIAS = {
    "url": "https://www.meganoticias.cl/temas/politica/",
    "tag": "div",
    "identifier_attrib": "class",
    "attrib_value": "notas",
    "explore_path": "temas/politica/?page=page_num",
    "forbidden_paths": ["/mundo/", "/temas/"],
    "news_selector": MEGANOTICIAS_SELECTOR
}

TVN_NOTICIAS = {
    "url": "https://www.24horas.cl/actualidad/politica/",
    "tag": "div",
    "identifier_attrib": "class",
    "attrib_value": "row",
    "explore_path": "actualidad/politica/p/page_num",
    "forbidden_paths": ["/p/"],
    "news_selector": TVN_SELECTOR,
}

COOPERATIVA = {
    "url": "https://www.cooperativa.cl/noticias/site/tax/port/all/cooperativataxport_3_156__1.html",
    "tag": "section",
    # damn....
    # pls fix
    "identifier_attrib": "style",
    "attrib_value": "display:table;margin: 35px 0;",
    "forbidden_paths": ["/tax/"],
    "news_selector": COOPERATIVA_SELECTOR,
}

ELDINAMO = {
    "url": "https://www.eldinamo.cl/politica/",
    "tag": "section",
    "identifier_attrib": "class",
    "attrib_value": "listado",
    "explore_path": "politica/page/page_num/",
    "news_selector": ELDINAMO_SELECTOR,
    # we don't care about these links.
    "forbidden_paths": ["/page/"]
}

ASCOM = {
    "url": "https://chile.as.com/noticias/politica/",
    "tag": "div",
    "identifier_attrib": "class",
    "attrib_value": "area-gr g-double-col",
    "explore_path": "noticias/politica/page_num",
    "force_spec_url" : True,
    "forbidden_paths": ["/?omnil=mpal", "/videos/"],
    "news_selector": ASCOM_SELECTOR,
}