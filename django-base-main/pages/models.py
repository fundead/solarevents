import json
from collections import defaultdict
from django.db import models


class Revision(models.Model):
    timestamp = models.DateField()
    article = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.timestamp} {self.article}'

# Single DB query aggregating over timestamp field truncated to the year and counting
# records (revisions/edits) for each article
def query_chart_data():
    result = Revision.objects.raw(
        """
        SELECT
            1 AS id,
            article,
            strftime("%Y", timestamp) AS year,
            count(1) AS count
        FROM
            pages_revision
        GROUP BY
            year, article
        ORDER BY
            timestamp ASC;
        """
    )

    output = defaultdict(list)
    for obj in result:
        output[obj.article].append({
            'year': obj.year,
            'revisions': obj.count
        })

    return output
    

class SolarEvent(models.Model):
    event_date = models.DateField()
    event_name = models.CharField(max_length=100)
    event_description = models.CharField(max_length=200)
    tags = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

# Reads the converted JSON data set from disk and returns it as a JSON object
def read_solar_events():
    with open('pages/data/solar_events.json') as file:
        content_json = file.read()
        events = json.loads(content_json)
        return events