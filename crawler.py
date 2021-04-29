import mechanize
from bs4 import BeautifulSoup
import re


class MtG_Browser:
    '''
    browser class for all the interactions with website
    '''

    def __init__(self):
        # Browser
        self.br = mechanize.Browser()

        # Cookie Jar
        self.br.set_cookiejar(mechanize.CookieJar())

        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # User-Agent (this is cheating, ok?)
        self.br.addheaders = [('User-agent',
                               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def grab_themes(self):
        '''
        crawls through every theme
        :return:
        '''
        dl = self.br.open('https://mtgdecks.net/Pauper')
        # crawl themes --> https://mtgdecks.net/Pauper
        html = self.br.response().read()
        parsed_html = BeautifulSoup(html)

        table = parsed_html.body.find(class_='clickable table sortable table-striped')
        table_text = str(table)
        table_text = table_text.replace('\n', '')
        # <a href="/Pauper/mono-black-control">Mono Black Control</a>
        regex = '\<a href="\/.*?"\>'

        theme_list = re.findall(regex, table_text)
        for theme in theme_list:
            theme = theme.replace('<a href="', '')
            theme = theme.replace('">', '')

            url = 'https://mtgdecks.net' + theme
            print('\n' + url)
            self.grab_decks(url, 1)

        # print(table_text)

    def grab_decks(self, theme_url, index):
        '''
        crawls through every deck
        :param theme_url: url to every theme
        :param index: current page (iterates through all decks per theme)
        :return:
        '''
        # crawl individual decks --> https://mtgdecks.net/Pauper/mono-black-control

        dl = self.br.open(theme_url + '/page:' + str(index + 1))
        html = self.br.response().read()
        parsed_html = BeautifulSoup(html)

        table = parsed_html.body.find(class_='clickable table table-striped')
        table_text = str(table)
        table_text = table_text.replace('\n', '')
        # <a href="/Pauper/mono-black-control">Mono Black Control</a>
        regex = '\<a href="\/.*?"\>'

        deck_list = re.findall(regex, table_text)
        for deck in deck_list:
            if '/sort:' not in deck:
                deck = deck.replace('<a href="', '')
                deck = deck.replace('">', '')

                deck_url = 'https://mtgdecks.net' + deck
                print(deck_url)
                self.grab_cards(deck_url)

        # start:
        # remaining links: <a href="/Pauper/affinity/page:41" rel="nofollow" class="next">Next Page&gt;</a>
        # no links left:   <a href="/Pauper/affinity/page:41" rel="nofollow">Next Page&gt;</a>

        pagination = parsed_html.body.find(class_='pagination')
        next = pagination.find(class_='next disabled')
        if str(next) is not None:
            self.grab_decks(theme_url, index + 1)

    def grab_cards(self, url):
        '''
        grabs the cards in a deck
        :param url: url to deck
        :return:
        '''
        dl = self.br.open(url)
        html = self.br.response().read()
        parsed_html = BeautifulSoup(html)
        # not all cards are in arena
        cards = parsed_html.body.find(class_="wholeDeck")
        cards_text = str(cards)

        card = cards.find_all(class_='cardItem')

        for c in card:
            print(c['data-required'], c['data-card-id'])




if __name__ == "__main__":
    # let's do some magic here
    b = MtG_Browser()
    b.grab_themes()
