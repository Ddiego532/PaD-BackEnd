import json

def get_news_dict():
    json_path = r"scraper/output_data/all_news.json"
    with open(json_path, 'r',  encoding='utf-8') as f:
        data = json.load(f)

    news_dict = {i+1: news for i, news in enumerate(data)}

    return news_dict

    #for key, value in news_dict.items():
    #    print(f"{key}: {value}\n")

    #print(f"{1}: {news_dict[1]}\n")