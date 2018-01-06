# -*- coding: utf-8 -*-
import requests
import datetime
import os
import re
import difflib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# requests might throw connection error
from requests.exceptions import ConnectionError

# Count is updated every timeout-seconds
global COUNT
global MAX_COUNT
global TIMEOUT
MAX_COUNT = 960
TIMEOUT = 30
COUNT = 0

class VakiokoneHandler:
    VAKIOKONE_WINNING_ROW_LIST = ""
    VAKIOKONE_LATEST_PAGE_CONTENT = ""
    VAKIOKONE_LATEST_PAGE_NUMBER = "671"

    def __init__(self, username, password):
        current_year = str(datetime.datetime.now().isocalendar()[0])
        current_week = str(datetime.datetime.now().isocalendar()[1])
        payload = {'user': username, 'password': password}
        url = 'http://vakiokone.appspot.com/kierros/' + current_year + '/' + current_week + '/?action=export_txt'
        print "Vakiokonepage url:" + url
        r = requests.post(url, data=payload)
        print "Vakiokonepage export_txt:" + r.content
        self.VAKIOKONE_WINNING_ROW_LIST = r.content.split(" ")

    def get_winning_row(self):
        return self.VAKIOKONE_WINNING_ROW_LIST

    def convert_goals_into_1X2(self, line):
        correct_mark = ""
        found_goals = re.search('([0-9]+-[0-9]+)', line)
        found_lottery = re.search('rvottu.*([1xX2]+)', line)
        if found_goals is not None:
            home_and_away_list = found_goals.group(1).split("-")
            if home_and_away_list[0] == home_and_away_list[1]:
               correct_mark = "X"
            if home_and_away_list[0] > home_and_away_list[1]:
               correct_mark = "1"
            if home_and_away_list[0] < home_and_away_list[1]:
               correct_mark = "2"
            _print(correct_mark)
            return correct_mark
        elif found_lottery is not None:
            return found_lottery.group(1).upper()
        else:
            return ""

    def return_status_on_page(self, page_content):
        page_content_lines = page_content.splitlines()
        page_content = ""
        line_number = 0
        hits_number = 0
        games_started = 0
        hits_text = "_"
        winning_row_list = self.get_winning_row()
        for line in page_content_lines:
            if line.find(" - ") != -1:
                _print(line)
                winning_marks = winning_row_list[line_number]
                line_number += 1
                correct_mark = self.convert_goals_into_1X2(line)
                line = line.replace(" ", "")
                line = line.replace("rvottu", "rv.")
                if correct_mark != "":
                    games_started += 1
                    if winning_marks.find(correct_mark) != -1:
                        hits_number += 1
                        hits_text = "v"
                    else:
                        hits_text = "_"
                else:
                    hits_text = "_"

                page_content = page_content + hits_text + str(line_number) + "." + line + " " + winning_marks + "\n"

        page_content = str(hits_number) + "/" + str(games_started) + " osumaa:\n" + page_content
        return page_content

class TekstiTvHandler:
    TEKSTITV_WRONG_PAGE_NUMBER = "Sivunro voi olla esim 100 tai 47102 (toinen alasivu)."
    TEKSTITV_PAGE_NOT_FOUND = "Sivua ei löytynyt!"
    TEKSTITV_LATEST_PAGE_CONTENT = ""
    TEKSTITV_LATEST_PAGE_NUMBER = ""
    TEKSTITV_MONITOR_PAGE_CONTENTS = []
    TEKSTITV_MONITOR_PAGE_NUMBERS = []

    def __init__(self, browser_name):
        if browser_name == "phantomjs":
            os.system('pwd')
            os.system('echo $PATH')
            os.system('ls -la ~/vendor/phantomjs/bin/phantomjs')
            os.system('phantomjs --version')
            self.driver = webdriver.PhantomJS()
        else:
            self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def trim_page(self, page_content):
        page_content = page_content.replace("---------------------------------------", "--------------------------------")
        page_content = page_content.replace("    ", " ")
        page_content = page_content.replace("   ", " ")
        page_content = page_content.replace("  ", " ")
        page_content = page_content.replace("Aston Villa", "Villans")
        page_content = page_content.replace("Bournemouth", "Cherries")
        page_content = page_content.replace("Bolton", "Trotters")
        page_content = page_content.replace("Barnsley", "Tykes")
        page_content = page_content.replace("Burton Albion", "Brewers")
        page_content = page_content.replace("Burnley", "Clarets")
        page_content = page_content.replace("Bristol City", "Robins")
        page_content = page_content.replace("Brentford", "Bees")
        page_content = page_content.replace("Birmingham", "Blues")
        page_content = page_content.replace("CrystalP", "Eagles")
        page_content = page_content.replace("Chelsea", "Pensioners")
        page_content = page_content.replace("Coventry", "SkyBlues")
        page_content = page_content.replace("Exeter", "Grecians")
        page_content = page_content.replace("Ipswich", "TractorBoys")
        page_content = page_content.replace("Fulham", "Cottagers")
        page_content = page_content.replace("Huddersfield", "Terriers")
        page_content = page_content.replace("Leicester", "Foxes")
        page_content = page_content.replace("Liverpool", "Reds")
        page_content = page_content.replace("Luton", "Hatters")
        page_content = page_content.replace("Man United", "RedDevils")
        page_content = page_content.replace("Man City", "Citizens")
        page_content = page_content.replace("Millwall", "Lions")
        page_content = page_content.replace("Middlesbrough", "Smoggies")
        page_content = page_content.replace("Newcastle", "Toon")
        page_content = page_content.replace("Norwich", "Canaries")
        page_content = page_content.replace("Nottingham", "TrickyTrees")
        page_content = page_content.replace("Southampton", "Saints")
        page_content = page_content.replace("Sheff U", "Blades")
        page_content = page_content.replace("Sheff W", "Owls")
        page_content = page_content.replace("Sunderland", "BlackCats")
        page_content = page_content.replace("Stoke", "Potters")
        page_content = page_content.replace("Swansea", "Swans")
        page_content = page_content.replace("Tottenham", "Yids")
        page_content = page_content.replace("Watford", "Hornets")
        page_content = page_content.replace("West Bromwich", "Baggies")
        page_content = page_content.replace("Wigan", "Tics")
        return page_content

    def get_latest_page_content(self):
        return self.get_page_content(self.TEKSTITV_LATEST_PAGE_NUMBER)

    def get_page_content(self, page_number):
        print "get_page_content: page_number = " + str(page_number)
        try:
            if len(page_number) < 3:
                return self.TEKSTITV_WRONG_PAGE_NUMBER
            elif len(page_number) > 5:
                return self.TEKSTITV_WRONG_PAGE_NUMBER
            elif len(page_number) == 3:
                page_number = page_number + "_01"
            else:
                slice_offset = 3
                page_number_str = str(page_number)
                main_page_number = page_number_str[:slice_offset]
                sub_page_number = page_number_str[slice_offset:]
                page_number = main_page_number + "_" + sub_page_number
                print page_number
        except:
            return self.TEKSTITV_WRONG_PAGE_NUMBER

        try:
            self.driver.get("https://www.yle.fi/tekstitv/txt/P{}.html".format(page_number))
            self.driver.set_page_load_timeout(45)
            page_content = self.driver.find_element_by_xpath("(//pre)[2]").text
            page_content = self.trim_page(page_content)
            page_number = page_number.replace("_", "")
            self.TEKSTITV_LATEST_PAGE_NUMBER = str(page_number)
            self.TEKSTITV_LATEST_PAGE_CONTENT = page_content
            return page_content
        except:
            return self.TEKSTITV_PAGE_NOT_FOUND


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=TIMEOUT):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_html_message(self, chat_id, text):
        params = {'parse_mode': 'HTML', 'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self, offset=None, timeout=TIMEOUT):
        get_result = self.get_updates(offset, timeout)

        if len(get_result) > 0:
            last_update = get_result[-1]
            print "get_last_update in if {}".format(last_update)
        else:
            last_update = ""

        return last_update

def _print(line):
    print line

def main():
    browser_name = os.environ.get('BROWSER_NAME')
    bot_token = os.environ.get('BOT_TOKEN')
    vakiokone_user = os.environ.get('VAKIOKONE_USER')
    vakiokone_pass = os.environ.get('VAKIOKONE_PASS')

    greet_bot = BotHandler(bot_token)
    browser = TekstiTvHandler(browser_name)
    vakiokone = VakiokoneHandler(vakiokone_user, vakiokone_pass)
    new_offset = None
    page_content = ""

    global COUNT
    global MAX_COUNT

    while (COUNT < MAX_COUNT):
        #greet_bot.get_updates(new_offset)
        try:
            last_update = greet_bot.get_last_update(new_offset)
        except ConnectionError:
            last_update = ""
            greet_bot = BotHandler(bot_token)

        if len(last_update) > 0:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            print "'" + last_chat_text + "'"

            last_chat_text = last_chat_text.replace("/", "")
            last_chat_text = last_chat_text.lower()
            if last_chat_text.isdigit():
                page_content = browser.get_page_content(last_chat_text)
            elif last_chat_text.find("vakio1") != -1:
                vakiokone = VakiokoneHandler(vakiokone_user, vakiokone_pass)
                page_content = browser.get_page_content(browser.TEKSTITV_LATEST_PAGE_NUMBER)
                page_content = vakiokone.return_status_on_page(page_content)
                vakiokone.VAKIOKONE_LATEST_PAGE_NUMBER = browser.TEKSTITV_LATEST_PAGE_NUMBER
                vakiokone.VAKIOKONE_LATEST_PAGE_CONTENT = page_content
            elif last_chat_text.find("timeout") != -1:
                timeout = last_chat_text.replace("timeout", "")
                if timeout.isdigit():
                    TIMEOUT = timeout
                    page_content = "Timeout käytössä. Tarkistan seuratut sivut " + timeout + " sekunnin välein."
                else:
                    page_content = "Antamasi timeout-arvo ei ole numeroarvo!"
            elif last_chat_text.find("seuraa") != -1:
                browser.TEKSTITV_MONITOR_PAGE_CONTENTS.append(browser.TEKSTITV_LATEST_PAGE_CONTENT)
                browser.TEKSTITV_MONITOR_PAGE_NUMBERS.append(browser.TEKSTITV_LATEST_PAGE_NUMBER)
                page_content = "Seuraan nyt sivua " + browser.TEKSTITV_LATEST_PAGE_NUMBER + "."
            else:
                page_content = "En tunnista tätä: " + last_chat_text

            try:
                greet_bot.send_message(last_chat_id, page_content)
            except ConnectionError:
                last_update = ""
                greet_bot = BotHandler(bot_token)
            new_offset = last_update_id + 1

        else:
            if vakiokone.VAKIOKONE_LATEST_PAGE_NUMBER != "":
                page_content = browser.get_page_content(vakiokone.VAKIOKONE_LATEST_PAGE_NUMBER)
                page_content = vakiokone.return_status_on_page(page_content)
                if page_content.find(vakiokone.VAKIOKONE_LATEST_PAGE_CONTENT) == -1:
                    print "Vakio game statuses changed!"
                    try:
                        greet_bot.send_message(last_chat_id, page_content)
                        vakiokone.VAKIOKONE_LATEST_PAGE_CONTENT = page_content
                    except ConnectionError:
                        last_update = ""
                        greet_bot = BotHandler(bot_token)
                    new_offset = last_update_id + 1

                else:
                    print "No vakio game changes"

            id = 0
            while (id < len(browser.TEKSTITV_MONITOR_PAGE_NUMBERS)):
                page_content = browser.get_page_content(browser.TEKSTITV_MONITOR_PAGE_NUMBERS[id])
                if page_content.find(browser.TEKSTITV_MONITOR_PAGE_CONTENTS[id]) == -1:
                    print "Page " + browser.TEKSTITV_MONITOR_PAGE_NUMBERS[id] + " status changed!"
                    try:
                        page_content_incl_diff_list = difflib.ndiff(browser.TEKSTITV_MONITOR_PAGE_CONTENTS[id].splitlines(1), page_content.splitlines(1))
                        page_content_incl_diff = ''.join(page_content_incl_diff_list)
                        # Remove empty lines, question mark -lines and minus-lines
                        only_diff_str = re.sub(r'^[-? \t]+[^\n]+[\n]', '', page_content_incl_diff, flags=re.MULTILINE)
                        greet_bot.send_message(last_chat_id, only_diff_str)
                        browser.TEKSTITV_MONITOR_PAGE_CONTENTS[id] = page_content
                    except ConnectionError:

                        last_update = ""
                        greet_bot = BotHandler(bot_token)
                    new_offset = last_update_id + 1
                else:
                    print "No page changes"
                id += 1
        COUNT += 1

if __name__ == '__main__':
    global COUNT
    global MAX_COUNT
    while True:
        if (COUNT < MAX_COUNT):
            try:
                main()
            except Exception as e:
                print e
                print "COUNT:" + str(COUNT)
        else:
            print "COUNT:" + str(COUNT)
            exit()
