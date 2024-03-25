# This is the main page of the web application
from flask import Flask, render_template, request
from weather import get_current_weather
# waitress package is needed to serve our application in the production deployment
from waitress import serve

# The below command makes our app a flask app
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city') # received from the form

    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        city = "New Delhi"

    weather_data = get_current_weather(city)

    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')
    
    return render_template(
        "weather.html",
        title = weather_data["name"], # JSON data object recieved from the api
        status = weather_data["weather"][0]["description"].capitalize(),
        temp=f'{weather_data["main"]["temp"]:.1f}',
        feels_like = f'{weather_data["main"]["feels_like"]:.1f}'
    )

if __name__=='__main__':
    # Used in the development server
    # app.run(host="0.0.0.0", port = 8000)

    # used in production deployment
    serve(app, host="0.0.0.0", port = 8000)