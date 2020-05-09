from flask import Flask, render_template, url_for

app = Flask(__name__, static_url_path='',
              template_folder='templates')

@app.route('/')
def index():
  return render_template('shexstatements.html')

@app.route('/quickstart')
def quickstart():
  return render_template('quickstart.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/docs')
def docs():
  return render_template('docs.html')

if __name__ == '__main__':
  app.run(debug=True)

