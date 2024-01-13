from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
print(hasattr(app, 'before_first_request'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iumor.db'  # Update this for your database
app.config['SECRET_KEY'] = 'password123'  # Change this to a random secret key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model for jokes
class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(500), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/category/<category_name>')
def category_jokes(category_name):
    jokes = Joke.query.filter(Joke.category.ilike(category_name)).all()
    return render_template('category.html', category=category_name, jokes=jokes)

@app.route('/delete_joke/<int:joke_id>', methods=['POST'])
def delete_joke(joke_id):
    joke_to_delete = Joke.query.get(joke_id)
    if joke_to_delete:
        db.session.delete(joke_to_delete)
        db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Implement your authentication logic
        return redirect(url_for('admin_panel'))
    return render_template('admin.html')

@app.route('/admin/panel')
def admin_panel():
    jokes = Joke.query.all()
    return render_template('admin_panel.html', jokes=jokes)




@app.route('/admin/add_joke', methods=['POST'])
def add_joke():
    category = request.form.get('category')
    joke_text = request.form.get('jokeText')

    print(f"Adding joke in category: {category}, Text: {joke_text}")  # Debug print

    new_joke = Joke(category=category, text=joke_text)
    db.session.add(new_joke)
    db.session.commit()

    return redirect(url_for('admin_panel'))


@app.route('/logout')
def logout():
    # Implement your logout logic here
    # For example, if using Flask-Login: logout_user()

    return redirect(url_for('home'))



# Run this function to create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
