from flask import Flask
app = Flask(__name__)
@app.route('/add')
def addition():
    result = 10 + 2
    return f"The sum is: {result}"  # Returning the result as a response

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)  # Debug mode enabled for easier debugging