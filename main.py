from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações da API TMDB
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

def get_movies(endpoint, page=1):
    """Função auxiliar para buscar filmes da API"""
    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            params={
                "api_key": TMDB_API_KEY,
                "language": "pt-BR",
                "page": page
            }
        )
        return response.json()
    except requests.exceptions.RequestException:
        return None

@app.route('/')
def index():
    # Busca filmes populares
    popular_movies = get_movies("movie/popular")
    if popular_movies:
        movies = popular_movies.get('results', [])
        return render_template('index.html', movies=movies, poster_base_url=POSTER_BASE_URL)
    return "Erro ao carregar filmes populares", 500

@app.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        try:
            response = requests.get(
                f"{BASE_URL}/search/movie",
                params={
                    "api_key": TMDB_API_KEY,
                    "language": "pt-BR",
                    "query": query
                }
            )
            search_results = response.json()
            movies = search_results.get('results', [])
            return render_template('search.html', movies=movies, query=query, poster_base_url=POSTER_BASE_URL)
        except requests.exceptions.RequestException:
            return "Erro na busca", 500
    return render_template('search.html', movies=[], query='', poster_base_url=POSTER_BASE_URL)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    try:
        response = requests.get(
            f"{BASE_URL}/movie/{movie_id}",
            params={
                "api_key": TMDB_API_KEY,
                "language": "pt-BR",
                "append_to_response": "credits"
            }
        )
        movie = response.json()
        return render_template('movie_detail.html', movie=movie, poster_base_url=POSTER_BASE_URL)
    except requests.exceptions.RequestException:
        return "Erro ao carregar detalhes do filme", 500

if __name__ == '__main__':
    app.run(debug=True)
