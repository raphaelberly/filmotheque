import requests
import re
from bs4 import BeautifulSoup
import yaml


class Scraper(object):

    _conf = yaml.safe_load(open('conf/scraper.yaml'))

    url = _conf['url']
    position2day = _conf['position2day']

    position_re = re.compile(r'left:(\d+)px;')
    duration_re = re.compile(r'Durée du film (\d{2}) : (\d{2})')
    time_re = re.compile(r'Séance : (\d{1,2}) H (\d{2})')

    @classmethod
    def run(cls):

        soup = BeautifulSoup(requests.get(cls.url).content, 'html.parser')
        shows = soup.findAll('a', attrs={'class': 'label popup'})

        results = []
        for show in shows:

            title = show.find('h5').text.capitalize()
            if not title:
                continue

            position = cls.position_re.findall(show['style'])[0]
            day = cls.position2day[position]

            tooltip = show.find('div', attrs={'class': 'tooltip'}).extract()

            duration = tooltip.find('span').text
            duration = cls.duration_re.findall(duration)[0]
            duration = ':'.join(duration)

            time = show.find('span').text
            time = cls.time_re.findall(time)[0]
            time = ':'.join(time)

            results.append({'title': title, 'duration': duration, 'time': time, 'day': day})

        return results
