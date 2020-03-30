import json

from lib.app import NewScrapper


def get_all_news(event, context):
    scrapper = NewScrapper("all")
    data = scrapper.get_news()
    body = {
        "data": data
    }

    # ss = json.dumps(data)
    # with open('test.json', 'w') as f:
    #     print(ss, file=f)  # Python 3.x

    response = {
        "statusCode": 200,
        "body": json.dumps(body, ensure_ascii=False)
    }

    return response

def get_news_from(event, context):
    diary = event['queryStringParameters']['diary']
    scrapper = NewScrapper(diary)
    data = scrapper.get_news()
    body = {
        "data": data
    }

    # ss = json.dumps(data)
    # with open('test.json', 'w') as f:
    #     print(ss, file=f)  # Python 3.x
    response = {
        "statusCode": 200,
        "body": json.dumps(body, ensure_ascii=False)
    }

    return response

# if __name__ == "__main__":
#     event = []
#     context = []
#     get_news_from(event, context)
