from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("load_solar_events", views.load_solar_events, name="load_solar_events"),
    path("scrape_revisions", views.scrape_revisions, name="scrape_revisions"),
    path("chart_data", views.chart_data, name="chart_data"),
]
