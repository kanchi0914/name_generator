import requests
from bs4 import BeautifulSoup

def get_examples(word):
    base_url = "http://eow.alc.co.jp/search"
    query = {}
    query["q"] = word
    query["ref"] = "sa"
    ret = requests.get(base_url, params=query)
    texts = ""
    soup = BeautifulSoup(ret.content,"lxml")
    for l in soup.findAll("div",{"id":"resultsList"})[0]:
        try:
            text = l.text
            if ("ファミリーネーム" in text):
                texts += text
        except:
            pass

    # for s in list:
    #     if ("【人名】" in s):
    #         #name = s.replace("◆", " ").split(" ")[0].replace("")
    #         first = s.find("【人名】") + len("【人名】")
    #         last = s.find("◆")
    #         name = s[first:last]
    #         print(s)
    #         print(name)
    #         break

    return texts


def get_from_weblio(word="", is_multi=True):
    base_url = "https://www.weblio.jp/content/" + word
    ret = requests.get(base_url)
    soup = BeautifulSoup(ret.content,"lxml")
    res = soup.find(class_='Gkjyj', reversed=False)
    if res != None:
        res2 = res.findAll(class_='crosslink')
        if is_multi:
            texts = ""
            for s in res2:
                texts += s.contents[0] + ","
            return texts.rstrip(",")
        else:
            return res2[0].contents[0]
    else: return ""

if __name__ == "__main__":
    result = get_from_weblio("HOFFMAN", True)
    print(result)

