import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    s = requests.Session()
    response = s.get("http://ip-api.com/json").json()
    country = response["city"]
    lat = str(response["lat"])
    long = str(response["lon"])
    coord = (lat+','+long)

    weather = s.get("https://darksky.net/forecast/{}/ca12".format(coord))
    weatherhtml= weather.text
    soup = BeautifulSoup(weatherhtml,'html.parser')
    currently = soup.select('span.summary.swap')[0].text
    feelslike = soup.find('span', class_='summary-high-low').find('span').text
    image = soup.find('span', class_='currently').find('img')['src']
    image_src = ("https://darksky.net" + image)
    
    ip = request.remote_addr
    print(ip)
    
    weather_data = {'country': country, 'currently': currently, 'feelslike':feelslike, 'image_src': image_src}

    return render_template('index.html', weather_data= weather_data)
