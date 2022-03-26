from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim
import pandas
import datetime

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/success-table', methods=['POST'])
def success_table():
    global filenaam
    if request.method == "POST":
        files = request.files['file']
        try:
            df = pandas.read_csv('sample_files')
            gc = Nominatim(scheme='http')
            df["coordinates"] = df["Address"].apply(gc.geocode)
            df['Latitude'] = df['coordinates'].apply(lambda x: x.latitude if x is not None else None)
            df['Longitude'] = df['coordinates'].apply(lambda x: x.longitude if x is not None else None)
            df = df.drop("coordinates", 1)
            filenaam = datetime.datetime.now().strftime("sample_files/%Y-%m-%d-%H-%M-%S-%f" + ".csv")
            df.to_csv(filenaam, index=None)
            return render_template("index.html", text=df.to_html(), btn='download.html')
        except Exception as e:
            return render_template("index.html", text=str(e))


@app.route("/download-file/")
def download():
    return send_file(filenaam, attachment_filename='yourfile.csv', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
