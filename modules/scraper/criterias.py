# atm we use the general politics.
# TODO: Swap forbidden_paths to accepted_paths.

# EL MOSTRADOR HANDLER.
# FORMATO DE SELECTOR.

ELMOSTRADOR_NEWS_SELECTOR = {
    "text_data": {
        "title": {"tag": "h1", "identifier_attrib": "class", "attrib_value": "d-the-single__title | common:margin-bottom-25"},
        "date": {"tag": "time", "identifier_attrib": "class", "attrib_value": "d-the-single__date | common:margin-bottom-20"},
        "subtitle": {"tag": "p", "identifier_attrib": "class", "attrib_value": "d-the-single__excerpt | u-fw-600"},
    },
    "image_url": {"tag": "img", "identifier_attrib": "class", "attrib_value": "d-the-single-media__image"},
    "content": {"tag": "div", "identifier_attrib": "class", "attrib_value": "d-the-single-wrapper__text"},
}

TVN_SELECTOR = {
    "text_data": {
        "title": {"tag": "h1", "identifier_attrib": "id", "attrib_value": "#contenido-ppal"},
        "date": {"tag": "p", "identifier_attrib": "class", "attrib_value": "fecha"},
        "subtitle": {"tag": "p", "identifier_attrib": "class", "attrib_value": "baj"},
    },
    "image_url": {
        "parent": {"tag": "div", "identifier_attrib": "class", "attrib_value": "img-wrap"},
        "tag": "img",
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
    "image_url": {"tag": "img", "identifier_attrib": "class", "attrib_value": "main-single-body__image js-img-single"},
    "content": {"tag": "div", "identifier_attrib": "class", "attrib_value": "main-single-body__content"},
    "news_tags": {"tag": "div", "identifier_attrib": "class", "attrib_value": "the-tags__list"}
}

LATERCERA_SELECTOR = {
    "text_data": {"title": {"tag": "div", "identifier_attrib": "class", "attrib_value": "hl"},
                  "date": {"tag": "time", "identifier_attrib": "class", "attrib_value": "p-left-10"},
                  "subtitle": {"tag": "p", "identifier_attrib": "class", "attrib_value": "excerpt"}},
    "image_url": {"parent": {"tag": "div", "identifier_attrib": "class", "attrib_value": "full-image"},
                  "tag": "img"},
    "content": {"tag": "div", "identifier_attrib": "class", "attrib_value": "single-content"},
    "common_irrelevant_tags": {"tags": ["aside", "div"], "classes": ["offer-content", "links | story_links"]},
    "news_tags": {"tag": "ul", "identifier_attrib": "class", "attrib_value": "list-cat-y-tags"},
}

TELETRECE_SELECTOR = {
    "text_data": {"title": {"tag": "h1", "identifier_attrib": "class", "attrib_value": "article-component__header-title"},
                  "subtitle": {"tag": "div", "identifier_attrib": "class", "attrib_value": "article-component__lead"},
                  "date": {"tag": "time", "identifier_attrib": "itemprop", "attrib_value": "datePublished"}},
    "image_url": {
        "parent": {
            "tag": "div", 
            "identifier_attrib": "class", 
            "attrib_value": "article-component__header-image-wrapper"
        }, 
        "tag": "img"
    },
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

    # watch me im different!!!!
    "image_url": {
        "parent": {
            "tag": "div",
            "identifier_attrib": "class",
            "attrib_value" : "post-image",
        },

        "tag": "a",
        "forced_src": "href",
    },

    "common_irrelevant_tags": {
        # we used the excerpt at this time so we can delete it easily.
        "tags": ["div", "div"],
        "classes": ["lee-tambien-bbcl", "post-excerpt"]
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
    "attrib_value": "clave",
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
    "forbidden_paths": ["/mundo/", "/temas/"]
}

TVN_NOTICIAS = {
    "url": "https://www.24horas.cl/actualidad/politica/",
    "tag": "div",
    "identifier_attrib": "class",
    "attrib_value": "row",
    "explore_path": "actualidad/politica/p/page_num",
    "forbidden_paths": ["/p/"],
    "news_selector": TVN_SELECTOR,
    "ignore_content_ids": ["prontus-card-content"]
}