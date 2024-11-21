from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__) 
@app.route("/contact/")
def contact():
    return render_template("contact.html")
  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

  
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2
  
@app.route('/commits/')
def commits():
    # URL de l'API GitHub
    repo_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    # Requête pour récupérer les commits
    response = urlopen(repo_url)
    if response.status != 200:
        return jsonify({"error": "Impossible de récupérer les données des commits"}), 500

    commits_data = json.loads(response.read().decode('utf-8'))
    minutes_count = {}

    # Extraction des minutes de chaque commit
    for commit in commits_data:
        commit_date = commit["commit"]["author"]["date"]
        date_object = datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")
        minute = date_object.minute

        if minute not in minutes_count:
            minutes_count[minute] = 0
        minutes_count[minute] += 1

    # Préparation des données pour le graphique
    results = [{"Minute": minute, "Commits": count} for minute, count in minutes_count.items()]
    return jsonify(results=results)
  
if __name__ == "__main__":
  app.run(debug=True)
