# coding: UTF-8
import requests
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import csv
from jaNameSearch import get_from_weblio
import json_dumper as dumper
import translator

class Scraper():

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }
    url = ""

    def __init__(self, url=""):
        self.url = url

    def getRequest(self):
        request = urllib.request.Request(self.url, headers=self.headers)
        html = urllib.request.urlopen(request)
        soup = BeautifulSoup(html, 'html.parser')
        return soup


    def getText(self, tag):
        soup = self.getRequest()
        text = soup.findAll(tag)
        return text


    def load_csv(self, csvPath):
        with open(csvPath, "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            return [row for row in reader]

    def get_jp_names(self, csvPath, savePath):
        csvData = self.load_csv(csvPath)
        del csvData[0][0]
        with open(savePath, "w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            for i, line in enumerate(csvData):
                if (len(line) > 0):
                    raw_name = line[0]
                    ja_names = get_from_weblio(raw_name)
                    print(i, "-", raw_name, ":", ja_names)
                    writer.writerow([ja_names])

    def get_reliable_name(self, country, csvPath, jaNames, savePath):
        raw_data = self.load_csv(csvPath)
        del raw_data[0]
        jp_data = self.load_csv(jaNames)
        try:
            with open(savePath, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                count = 0
                for raw, jps in zip(raw_data, jp_data):
                    count += 1
                    raw_name = raw[0]
                    google_jp_name = ""
                    reliable_jp_name = ""
                    google_jp_name = translator.get(text=raw_name, country=country)
                    if len(jps) > 0:
                        jp_names_list = jps[0].split(",")
                        if google_jp_name in jp_names_list:
                            index = jp_names_list.index(google_jp_name)
                            reliable_jp_name = jp_names_list[index]
                        elif len(jp_names_list) > 0:
                            reliable_jp_name = jp_names_list[0]
                    elif len(google_jp_name) > 0:
                        reliable_jp_name = google_jp_name

                    list = []
                    list.append(raw_name)
                    list.append(reliable_jp_name)
                    print(count, ":", list)
                    writer.writerow(list)

                    #if count > 10: break

        except EnvironmentError:
            print("error occuered!")


    def scrapeTabel(self, csvPath, is_add_jpName=False):
        soup = self.getRequest()
        table = soup.findAll("table")[0]
        rows = table.findAll("tr")
        with open(csvPath, "w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in rows:
                csvRow = []
                for cell in row.findAll(['td', 'th']):
                    text = cell.get_text().replace(" ", "").replace("%", "")
                    csvRow.append(text)
                if len(csvRow) > 0:
                    if is_add_jpName:
                        enName = csvRow[0]
                        jaName = ""
                        if len(enName) > 0:
                            jaName = get_from_weblio(enName)
                        csvRow.insert(1, jaName)
                    writer.writerow(csvRow)
