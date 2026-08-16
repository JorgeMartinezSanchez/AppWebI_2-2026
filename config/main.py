from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', name='John Doe')
    # render_template needs a template file named 'index.html' in a folder named 'templates' in the same directory as this script.

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')