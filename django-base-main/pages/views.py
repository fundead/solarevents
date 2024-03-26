import json
import requests
from dateutil import parser as dateparser

from django.http import HttpResponse
from django.shortcuts import render

from .models import Revision, SolarEvent, query_chart_data, read_solar_events

# GET /pages/
# Reads all solar events if they are loaded, displaying them in the main static view
def home(request):
    solar_events = SolarEvent.objects.all()

    context = {
        'solar_events': solar_events
    }
    return render(context=context, request=request, template_name='pages/home.html')

# GET /pages/load_solar_events
# Load solar events from disk and persists to the database
#
# table: pages_solarevent
def load_solar_events(request):
    # First delete all existing records
    solar_events = SolarEvent.objects.all()
    solar_events.delete()

    # Load data from disk
    solar_events = read_solar_events()

    # Parse into model
    models = [
        SolarEvent(
            event_date=dateparser.parse(solar_event['event_date']),
            event_name=solar_event['event_name'],
            event_description=solar_event['event_description'],
            tags=solar_event['tags'],
            link=solar_event['link'],
        )
        for solar_event in solar_events
    ]
    
    # Persist
    for model in models:
        model.save()

    body = json.dumps({"result": "ok"})
    return HttpResponse(content=body, content_type="application/json")

# GET /pages/scrape_revisions
# Performs paginated GET requests to retrieve all revisions for the articles listed from Wikipedia,
# then persists results as records to the DB
#
# This will not scrape if records already exist - in which case execute: DELETE FROM pages_revision;
#
# table: pages_revision
def scrape_revisions(request):
    if Revision.objects.count() != 0:
        return HttpResponse(content=json.dumps({"result": "Table not empty; did not scrape"}), content_type="application/json")

    articles = [
        'Perovskite solar cell',
        'Solar cell',
        'Semiconductor'
    ]

    try:
        for article in articles:
            # Make GET request to Wikipedia
            results = get_article_revisions(article)
            models = to_revision_models(results, article)
            
            # Persist to database
            for model in models:
                model.save()
    except Exception as e:
        print(e)
        return HttpResponse(content=json.dumps({'result': 'Backend persist error'}), content_type='application/json')

    return HttpResponse(content=json.dumps({'result': 'ok'}), content_type='application/json')

# Builds list of Revision models formatted with expected date string
def to_revision_models(revisions, article):
    # Emits YYYY-MM-DD
    def format(timestamp):
        return dateparser.parse(timestamp).strftime('%Y-%m-%d')

    return [
        Revision(timestamp=format(r['timestamp']), article=article)
        for r in revisions
    ]


# Gets timestamps of all revisions for a Wikipedia article by title.
# Paginated in batches of 500
#
# returns: [{ 'timestamp': 'ISO8601' }]
def get_article_revisions(article):
    results = []

    url = 'https://www.wikipedia.org/w/api.php'
    request = {
        'action': 'query',
        'prop': 'revisions',
        'titles': article,
        'rvprop': 'timestamp',
        'rvslots': 'main',
        'formatversion': '2',
        'format': 'json',
        'rvlimit': '500'
    }
    last_continue = {}
    while True:
        req = request.copy()
        req.update(last_continue)
        response = requests.get(url, params=req).json()
        if 'error' in response:
            raise Exception(response['error'])
        if 'query' in response:
            pages = response['query']['pages']
            for page in pages:
                results.extend(page['revisions'])
        if 'continue' not in response:
            break
        last_continue = response['continue']
    
    return results


# GET /pages/chart_data
# Ajax endpoint for populating chart data
def chart_data(request):
    query_result = query_chart_data()

    years = [] # For echarts x-axis
    all_series = []

    for article, points in query_result.items():
        # Finds the longest series, updating if the current series is greater than prior series - ensures all years visible
        current_years = [el['year'] for el in points]
        if len(current_years) > len(years):
            years = current_years

        # The data points (counts of edits) as a raw integer array for the current article (series)
        data = [el['revisions'] for el in points]

        all_series.append({
            'name': article,
            'type': 'line',
            'data': data
        })
    
    # Pad series that do not start at 2001 with zero points (e.g. Perovskite)
    for series in all_series:
        if len(series['data']) < len(years):
            pad_count = len(years) - len(series['data'])
            padding = [0] * pad_count
            padding.extend(series['data'])
            series['data'] = padding

    # DB query: get event_name from pages_solarevent table
    events = SolarEvent.objects.values_list('event_name', 'event_date')
    markline_data = []
    for event in events:
        formatted_date = event[1].strftime('%Y')
        if markline_data and markline_data[-1]['date'] == formatted_date:
            # Handle years with multiple events by concatenating (rendered in one tooltip)
            markline_data[-1]['name'] += f'<br />{event[0]}'
            continue

        markline_data.append({
            'name': event[0],
            'date': formatted_date
        })
    
    echarts_data = {
        'xAxis': years,
        'series': all_series,
        'markLineData': markline_data
    }
    json_body = json.dumps(echarts_data)
    return HttpResponse(content=json_body, content_type='application/json')