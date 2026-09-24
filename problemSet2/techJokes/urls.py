from django.urls import path

from . import views

app_name = 'techJokes'

urlpatterns = [
    path('', views.ps2_index, name='ps2_index'),
    path('sql/', views.sql_transcript, name='sql_transcript'),

    # Q1 / Q2 / Q3 — joke list, add form, search, hide/reset personalization
    path('jokes/', views.joke_index, name='index'),
    path('jokes/hide/<int:joke_id>/', views.hide_joke, name='hide_joke'),
    path('jokes/reset-personalization/', views.reset_personalization, name='reset_personalization'),

    # Q4 — export endpoints
    path('jokes/export/json/', views.export_json, name='export_json'),
    path('jokes/export/xml/', views.export_xml, name='export_xml'),

    # Q5 — import from remote XML URL
    path('jokes/import/', views.import_jokes, name='import'),
]
