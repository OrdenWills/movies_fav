import requests

TMDB_API_KEY = "4c037c4071e799bcab80a58973278537"
TMDB_LINK = "https://api.themoviedb.org/3"


class DataManager:

    def send_request(self, movie_name):
        params = {
            "query": movie_name,
            "api_key": TMDB_API_KEY
        }
        # header = {
        #
        # }
        response = requests.get(f"{TMDB_LINK}/search/movie", params=params)
        result = response.json()["results"]
        return result

    def get_details(self, movie_id):
        params = {
            "api_key": TMDB_API_KEY
        }
        response = requests.get(f"{TMDB_LINK}/movie/{movie_id}", params=params)
        result = response.json()
        return result


