# atm we use the general politics.
# TODO: Swap forbidden_paths to accepted_paths.

# EL MOSTRADOR HANDLER.
ELMOSTRADOR_NEWS_SELECTOR = {
    "text_data": {
        "title": {
            "tag": "h1",
            "class": "d-the-single__title | common:margin-bottom-25"
        },

        "date": {
            "tag": "time",
            "class": "d-the-single__date | common:margin-bottom-20",
        },

        "subtitle": {
            "tag": "p",
            "class": "d-the-single__excerpt | u-fw-600",
        },
    },

    "image_url" : {
        "tag": "img",
        "class": "d-the-single-media__image"
    },

    "content": {
        "tag": "div",
        "class": "d-the-single-wrapper__text"
    },

    # there are some tags that should be ignored.
    # el primero es "te puede interesar".
    "ignore_content_ids": ["the-single-cards"]
}

ELMOSTRADOR = {
    # reverted this guy again.
    "url": "https://www.elmostrador.cl/categoria/pais/",
    "tag": "section",
    "id": "claves",
    # num goes here.
    "explore_path": "categoria/pais/page/page_num/",
    "forbidden_paths": ["/autores/", "/autor/", "/page/", "/multimedia/", "/opinion/"],

    "news_selector": ELMOSTRADOR_NEWS_SELECTOR
}

# this lad from here has ID.
BIOBIOCHILE = {
    # how...
    "url": "https://www.biobiochile.cl/lista/tag/politica",
    "tag": "div",
    # should be only one.
    "class": "section-body",
    "forbidden_paths" : ["/autores/", "/biobiotv/", "/opinion/", "/especial/"],
}

LATERCERA = {
    "url": "https://www.latercera.com/categoria/politica/page/1",
    "tag": "section",
    # like the one before.
    "class": "top-mainy",
    # this differs
    "explore_path": "categoria/politica/page/page_num/",
}

# i should guess biobio and cnn are somewhat kinda similar.
CNNCHILE = {
    "url": "https://www.cnnchile.com/tag/politica/",
    "tag": "div",
    "class": "inner-list",
    "explore_path": "tag/politica/page/page_num/",
    "forbidden_paths": ["/lodijeronencnn/", "/opinion/", "/programas-completos/", "/mundo/", "/tag/"]
}

MEGANOTICIAS = {
    "url": "https://www.meganoticias.cl/temas/politica/",
    "tag": "div",
    "class": "notas",
    "explore_path": "temas/politica/?page=page_num",
    "forbidden_paths": ["/mundo/", "/temas/"]
}

TVN_SELECTOR = {
    "text_data": {
        "title": {
            "tag": "h1",
            "id": "#contenido-ppal"
        },

        "date": {
            "tag": "p",
            "class": "fecha",
        },

        "subtitle": {
            "tag": "p",
            "class": "baj",
        },
    },

    "image_url" : {
        "parent" : {
            "tag": "div",
            "class": "img-wrap"
        },

        "tag": "img",
    },

    "content": {
        "tag": "div",
        "class": "CUERPO"
    },

    # there are some tags that should be ignored.
    # el primero es "te puede interesar".
    "ignore_content_ids": ["prontus-card-container"]
}

# it doesn't let me put 24HORAS for some reason goofy ahh moment.
TVN_NOTICIAS = {
    "url": "https://www.24horas.cl/actualidad/politica/",
    "tag": "div",
    # FIXME: This can be changed in the future.
    "class": "row",
    "explore_path": "actualidad/politica/p/page_num",
    "forbidden_paths": ["/p/"],
    "news_selector": TVN_SELECTOR,
    "ignore_content_ids": ["prontus-card-content"]
}