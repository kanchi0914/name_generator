import  requests


def get(text, country):
    url = "https://script.google.com/macros/s/AKfycbzMG4a7tI6iPgaahHT5XCssX6CweRyD8Ag6KGf74SRE4AmH454m/" \
          "exec?text="
    url += text
    url += "&source" + country
    url += "&target=ja"
    result = requests.get(url)
    return result.text
