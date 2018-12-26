from flask import render_template, redirect, flash, url_for
from app import app
from app.models import ATPase, Organism
from app import db
from forms import SearchForm

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
    	return redirect(url_for('search_results', query = form.search.data))	
    return render_template('searchform.html', 
        title = 'The AOS database',
        form = form)

@app.route('/about', methods = ['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
    	return redirect(url_for('search_results', query = form.search.data))	
    return render_template('searchform.html', 
        title = 'Search',
        form = form)

from config import MAX_SEARCH_RESULTS

@app.route('/search_results:<query>')
def search_results(query):
    results = Organism.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
        query = query,
        results = results)

@app.route('/<organism>')
def org_data(organism):
	name = organism[12:-2]
	organism_detailed = Organism.query.filter_by(name = name).first()
	return render_template('organism_info.html',
		org = organism_detailed)