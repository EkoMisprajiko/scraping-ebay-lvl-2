import os

from flask import Flask, render_template, request, send_file, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Regexp
from project.scraper import ebays_scraper
import json

def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    #set config development
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    class Search(FlaskForm):
        search = StringField('search:', validators=[InputRequired(), Regexp(r'[0-9A-Za-z ,.-]')])

    @app.route("/", methods=['GET', 'POST'])
    def index():
        title = "Ebay's Product Scraper"
        alert = 0
        form = Search(request.form)

        if form.validate_on_submit():
            name = form.search.data
            # data = name
            url = ebays_scraper.make_urls(name)
            check = ebays_scraper.scrape(url)
            data = check
            alert = "Result for " + name
            download_csv = "| <a href='/download-csv.html' target='_blank' class='btn btn-info'>CSV</a>"
            api_link = "| <a href='/all-api.html' target='_blank' class='btn btn-danger'>API</a>"
            download_json = "| <a href='/download-json.html' target='_blank' class='btn btn-warning'>JSON</a>"
            download_excel = "| <a href='/download-excel.html' target='_blank' class='btn btn-success'>Excel</a>"
            return render_template('res.html', title=title, form=form,
                                   data=data, csv=download_csv, alert=alert,
                                   api=api_link, json=download_json, excel=download_excel)
        else:
            return render_template('base_template.html', title=title, form=form, alert=alert)

    @app.route('/download-csv.html', methods=['GET'])
    def download_csv():
        path = 'files/ebays_product.csv'
        return send_file(path, as_attachment=True, cache_timeout=0)

    @app.route('/all-api.html', methods=['GET'])
    def all_api():
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(fileDir, 'project/files/ebays_product.json')
        file = open(filename)
        data = json.load(file)
        return jsonify(data)

    @app.route('/download-json.html', methods=['GET'])
    def download_json():
        path = 'files/ebays_product.json'
        return send_file(path, as_attachment=True, cache_timeout=0)

    @app.route('/download-excel.html', methods=['GET'])
    def download_excel():
        path = 'files/ebays_product.xlsx'
        return send_file(path, as_attachment=True, cache_timeout=0)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app}

    return app