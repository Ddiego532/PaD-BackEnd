# atm we use the general politics.
ELMOSTRADOR = {
    # reverted this guy again.
    "url": "https://www.elmostrador.cl/categoria/pais/",
    "tag": "section",
    "id": "claves",
    # num goes here.
    "explore_path": "categoria/pais/page/",

    "news_body": {
        
    }
}

BIOBIOCHILE = {
    # how...
    "url": "https://www.biobiochile.cl/lista/tag/politica",
    "tag": "div",
    # should be only one.
    "class": "section-body",
    "forbidden_paths" : ["/autores/", "/biobiotv/", "/opinion/", "/especial/"],
}

LATERCERA = {
    # workaround be like
    # will redirect if we use the category path.
    # will reuse the page 1.
    "url": "https://www.latercera.com/categoria/politica/page/1",
    "tag": "section",
    # like the one before.
    "class": "top-mainy",
    # this differs
    "explore_path": "categoria/politica/page/",
}

# i should guess biobio and cnn are somewhat kinda similar.
CNNCHILE = {
    "url": "https://www.cnnchile.com/tag/politica/",
    "tag": "div",
    "class": "inner-list",
    "explore_path": "tag/politica/page/",
    "forbidden_paths": ["lodijeronencnn", "opinion/", "programas-completos", "mundo/"]
}