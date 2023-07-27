from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from omdbapi.movie_search import GetMovie
import config
movie = GetMovie(config.api_key)
import pyrebase


config = {
    'apiKey': "AIzaSyAuDVn9AW4rxSUeoR8lB6Ux7tSl9OCaMcQ",
    'authDomain': "movie-c2cda.firebaseapp.com",
    'projectId': "movie-c2cda",
    'storageBucket': "movie-c2cda.appspot.com",
    'messagingSenderId': "100899876519",
    'appId': "1:100899876519:web:c3475927833664a9127582",
    "databaseURL": "https://movie-c2cda-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase =pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return render_template('search.html')
        except :
            error = "Authintication failed"
    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"full_name":full_name, "username":username}
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return render_template('login.html')
        except :
            error = "Authintication failed"
    return render_template("signup.html")



@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        try:
            moviename = request.form['movie']
            movieinfo = movie.get_movie(title = moviename)
            print(movieinfo)
            return render_template("search.html", movieinfo = movieinfo)
        except:
            print("didnt find the movie")
    return render_template("search.html")

favorites_dict = {}

@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    if request.method == 'POST':
        movie_title = request.form['movie_title']
        movie_info = {
            'imdbrating': request.form['movie_imdb_rating'],
            'plot': request.form['movie_plot'],
            'language': request.form['movie_language'],
            'actors': request.form['movie_actors'],
            'country': request.form['movie_country'],
            'genre': request.form['movie_genre'],
            'director': request.form['movie_director'],
            'year': request.form['movie_year'],
        }

        user_id = login_session.get('user', {}).get('localId')

        if user_id:
            db.child("Users").child(user_id).child("Favorites").child(movie_title).set(movie_info)

        return redirect(url_for('favorites'))
    

@app.route('/favorites', methods=['GET'])
def favorites():
    favorites_info = {}
    try:
        user_id = login_session.get('user', {}).get('localId')

        if user_id:
            favorites_data = db.child("Users").child(user_id).child("Favorites").get()
            if favorites_data.each():
                for favorite_movie in favorites_data.each():
                    favorites_info[favorite_movie.key()] = favorite_movie.val()
    except:
        flash("Failed to fetch favorites from the database.", "error")

    return render_template("favorites.html", favorites_info=favorites_info)






if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True)