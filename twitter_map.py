"""
Twitter map yees!!!
"""
import geopy.geocoders
import certifi
import ssl
import requests
import pprint
import folium
from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from geopy.exc import GeocoderTimedOut
app = Flask(__name__)
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim(user_agent="vihtoriaaa", scheme='http')


def twitter_friends_info(bearer_token: str, screen_name: str):
    """
    Sends a request to Twitter using API bearer token abd returns json file
    that collects data about first 50 followers of user with given screen_name
    Sends request to Twitter with the help of bearer token.
    Returns json with the information about first 50 friends of user with given username.
    """
    base_url = 'https://api.twitter.com/'
    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }
    search_params = {
        'screen_name': '{}'.format(screen_name),
        'count': 50
    }
    search_url = '{}1.1/friends/list.json'.format(base_url)
    response = requests.get(
        search_url, headers=search_headers, params=search_params)
    data = response.json()
    return data


def get_user_info(data):
    """
    """
    users_info = []
    for user in data['users']:
        try:
            location = geolocator.geocode(user['location'])
            user_location = [location.latitude, location.longitude]
            while (user_location) in users_info:
                user_location[0] += 0.001
                user_location[1] += 0.001
            name = user['screen_name']
            users_info.append([name, tuple(user_location)])
        except AttributeError:
            pass
        except GeocoderUnavailable:
            pass
        except GeocoderTimedOut:
            pass
    return users_info


def create_map(users_info):
    """
    This function builds an HTML map with locations of user's friends on
    Twitter.
    """
    my_map = folium.Map(
        location=[49.818396058511645, 24.02258071000576], zoom_start=10)
    folium.TileLayer('cartodbdark_matter').add_to(my_map)
    folium.TileLayer('stamentoner').add_to(my_map)
    folium.TileLayer('openstreetmap').add_to(my_map)
    fg_friends = folium.FeatureGroup(name='Twitter Friends')
    for user in users_info:
        nickname = user[0]
        user_coord = user[1]
        fg_friends.add_child(folium.Marker(location=user_coord,
                                           popup=nickname,
                                           icon=folium.Icon(color='darkred',
                                                            icon='heart')))
    my_map.add_child(fg_friends)
    my_map.add_child(folium.LayerControl())
    return my_map.get_root().render()


@app.route("/")
def home_page():
    """
    This function creates the main page of the app
    """
    return render_template("index.html")


@app.route("/map", methods=["POST"])
def build_map():
    """
    """
    try:
        bearer_token = request.form.get("bearer_token")
        screen_name = request.form.get("screen_name")
        if not screen_name or not bearer_token:
            return render_template("failure.html")
        data = twitter_friends_info(bearer_token, screen_name)
        return create_map(get_user_info(data))
    except KeyError:
        return render_template("failure.html")


if __name__ == "__main__":
    app.run(debug=False)
