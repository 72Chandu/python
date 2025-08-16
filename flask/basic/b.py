from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    username = "Chandu"
    items = ["Apple", "Banana", "Mango", "Pineapple"]
    return render_template('index.html', name=username, fruits=items)

@app.route('/about')
def about():
    name = "Chandu"
    return render_template('about.html', name2=name)

if __name__ == '__main__':
    app.run(debug=True)   # automatic run 