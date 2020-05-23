from flask import Flask, render_template, url_for, request, redirect
from shexstatements.shexfromcsv import CSV
import json

app = Flask(__name__, static_url_path='',
              static_folder='./static',
              template_folder='./templates')

@app.route('/', methods=['GET','POST'])
def generateshex():
  data = {}
  if ("text/html" in request.headers["Accept"] ):
    if request.method == "POST" and "shexstatements" in request.form:
      shexstatements = request.form['shexstatements']
      delim = request.form['delim']
      shex = CSV.generate_shex_from_csv(shexstatements, delim=delim, filename=False)
      data["input"] = shexstatements
      data["output"] = shex
      return render_template('shexstatements.html', data=data)
    else:
      return render_template('shexstatements.html', data=data)
  elif ("application/json" in request.headers["Accept"]):
    jsonstr = next(iter(request.form.to_dict().keys()))
    jsonval = json.loads(jsonstr)
    shex = CSV.generate_shex_from_csv(jsonval[1], delim=jsonval[0], filename=False)
    return json.dumps(shex)
  # Currently shexstatements does not handle any other formats
  else:
    return ""


@app.route('/quickstart')
def quickstart():
  return render_template('quickstart.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/api')
def api():
  return render_template('api.html')

@app.route('/docs')
def docs():
  return render_template('docs.html')

def run():
  app.run(debug=True)

