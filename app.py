from flask import Flask, render_template, url_for, request, redirect
from shexstatements.shexfromcsv import CSV

app = Flask(__name__, static_url_path='',
              template_folder='templates')

@app.route('/', methods=['GET','POST'])
#def index():
#  return render_template('shexstatements.html')
#
#@app.route('/generateshex', methods=['POST'])
def generateshex():
  data = {}
  if request.method == "POST":
    shexstatements = request.form['shexstatements']
    delim = request.form['delim']
    shex = CSV.generate_shex_from_csv(shexstatements, delim=delim, filename=False)
    data["input"] = shexstatements
    data["output"] = shex
    return render_template('shexstatements.html', data=data)
  else:
    return render_template('shexstatements.html', data=data)


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

