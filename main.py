from scraper import  Scraper
#from googletrans import Translator
import requests

# translator = Translator(service_urls=[
#       'translate.google.co.jp',
#     ])
#
# # result = translator.translate("We must respect will of the indivisual.", dest="ja")
# # print(result)
#
#



scraper = Scraper()
#scraper.scrapeTabel("csv/names.csv")
#scraper.get_reliable_name()
#scraper.get_jp_names(csvPath="csv/Italian.csv", savePath="jp_italian_names.csv")
scraper.get_reliable_name(country="it", csvPath="csv/Italian.csv", jaNames="csv/jp_italian_names.csv",
                          savePath="csv/jp_italy_names.csv")

#scraper.get_jp_names("csv/names.csv", "csv/jaNames.csv")
# print (scraper.load_csv("csv/names.csv"))

# scraper = Scraper("https://script.google.com/macros/s/AKfycbzMG4a7tI6iPgaahHT5XCssX6CweRyD8Ag6KGf74SRE4AmH454m/exec?text=Smith&source=en&target=ja")
# text = scraper.getText("pre")
# print(text)
# # scraper.scrape("")

# import json
import urllib.request
#
# url = 'https://script.google.com/macros/s/AKfycbzMG4a7tI6iPgaahHT5XCssX6CweRyD8Ag6KGf74SRE4AmH454m/' \
#       'exec?text=Smith&source=en&target=ja'
# result = requests.get(url)
# print(result.text)

# req = urllib.request.Request(url)
# with urllib.request.urlopen(req) as res:
#     print(req)
