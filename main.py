import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from lib.mailer import Mailer
from lib.scraper import Scraper

credentials = yaml.safe_load(open('conf/credentials.yaml'))
conf = yaml.safe_load(open('conf/conf.yaml'))


def format_results(shows):
    # Group results by day
    days = {item: [] for item in conf['days']}
    for show in shows:
        day = show.pop('day')
        days[day].append(show)
    # Order results by time
    for day, item in days.items():
        days[day] = sorted(item, key=lambda x: x['time'])
    # Join days together and return
    return days


results = Scraper.run()

environment = Environment(loader=FileSystemLoader('templates'), undefined=StrictUndefined)
html = environment.get_template('email.html').render(results=format_results(results))

payload = yaml.safe_load(open('conf/mailer.yaml'))['payload']
payload['Messages'][0]['HTMLPart'] = html

mailer = Mailer(**credentials)
print(mailer.send(payload))
