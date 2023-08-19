import requests
import csv
import configparser

def make_request(url, headers=None):
    response = requests.get(url, headers=headers)
    return response.json()

def make_csv(data):
    with open('./simklData.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(['tmdbID','imdbID'])
        for movie in data:
            row = [movie['tmdb'],movie['imdb']]
            wr.writerow(row)

def map_data(data):
    return data['movie']['ids']

config = configparser.ConfigParser()

config.read('conf.ini')

client_id = config["CONFIGS"]["client_id"]

get_pin_url = "https://api.simkl.com/oauth/pin?client_id=" + client_id

pin_request = make_request(get_pin_url)

user_code = pin_request['user_code']
verification_url = pin_request['verification_url']

is_user_authenticated = False
code_verification_url = "https://api.simkl.com/oauth/pin/" + user_code + "?client_id=" + client_id

while not is_user_authenticated:
    print("Go to " + verification_url + " and input the following code")
    print(user_code)
    input("After confirming the code press enter...")
    code_verification_request = make_request(code_verification_url)
    if 'access_token' in code_verification_request:
        access_token = code_verification_request['access_token']
        is_user_authenticated = True

get_movies_list_url = "https://api.simkl.com/sync/all-items/movies/completed"

z = make_request(get_movies_list_url, {'Authorization':'Bearer ' + access_token, 'simkl-api-key': client_id})

data = list(map(map_data,z['movies']))

make_csv(data)