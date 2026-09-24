import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from itertools import groupby

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError, connection
from django.db.models import Q
from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import ImportJokesForm, JokeForm
from .models import Joke

HIDDEN_JOKES_COOKIE = 'hidden_jokes'
JOKES_PER_PAGE = 5


def get_hidden_joke_ids(request):
    raw = request.COOKIES.get(HIDDEN_JOKES_COOKIE, '')
    if not raw:
        return []
    return [int(value) for value in raw.split(',') if value.isdigit()]


def group_jokes_by_category(jokes):
    sorted_jokes = sorted(jokes, key=lambda joke: (joke.display_category, joke.text))
    return [
        (category, list(group))
        for category, group in groupby(sorted_jokes, key=lambda joke: joke.display_category)
    ]


def filter_jokes(request, search_term, search_mode):
    queryset = Joke.objects.all()
    hidden_ids = get_hidden_joke_ids(request)
    if hidden_ids:
        queryset = queryset.exclude(id__in=hidden_ids)

    term = search_term.strip()
    if not term:
        return queryset.order_by('category', 'text')

    if search_mode == 'fts' and connection.vendor == 'postgresql':
        from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

        vector = SearchVector('text', 'author')
        query = SearchQuery(term)
        return (
            queryset.annotate(rank=SearchRank(vector, query))
            .filter(rank__gt=0)
            .order_by('-rank')
        )

    return queryset.filter(
        Q(text__icontains=term) | Q(author__icontains=term)
    ).order_by('category', 'text')


def joke_index(request):
    search_term = request.GET.get('q', '')
    search_mode = request.GET.get('mode', 'basic')
    add_form = JokeForm()

    if request.method == 'POST' and 'add_joke' in request.POST:
        add_form = JokeForm(request.POST)
        if add_form.is_valid():
            try:
                add_form.save()
                messages.success(request, 'Joke added.')
                return redirect('techJokes:index')
            except IntegrityError:
                add_form.add_error(
                    None,
                    'This joke already exists with the same text, author, and category.',
                )

    jokes = filter_jokes(request, search_term, search_mode)
    paginator = Paginator(jokes, JOKES_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    if search_mode == 'fts' and search_term.strip() and connection.vendor == 'postgresql':
        grouped_jokes = [(None, list(page_obj.object_list))]
    else:
        grouped_jokes = group_jokes_by_category(page_obj.object_list)

    hidden_ids = get_hidden_joke_ids(request)
    context = {
        'add_form': add_form,
        'grouped_jokes': grouped_jokes,
        'page_obj': page_obj,
        'search_term': search_term,
        'search_mode': search_mode,
        'has_hidden_jokes': bool(hidden_ids),
        'fts_available': connection.vendor == 'postgresql',
    }
    return render(request, 'techJokes/joke_index.html', context)


@require_POST
def hide_joke(request, joke_id):
    hidden_ids = get_hidden_joke_ids(request)
    if joke_id not in hidden_ids:
        hidden_ids.append(joke_id)

    response = redirect(request.POST.get('next') or 'techJokes:index')
    response.set_cookie(
        HIDDEN_JOKES_COOKIE,
        ','.join(str(joke_id) for joke_id in hidden_ids),
        max_age=365 * 24 * 60 * 60,
    )
    return response


@require_POST
def reset_personalization(request):
    response = redirect('techJokes:index')
    response.delete_cookie(HIDDEN_JOKES_COOKIE)
    messages.success(request, 'Personalization erased.')
    return response

def export_json(request):
    jokes = [
        {
            'id': joke.id,
            'text': joke.text,
            'author': joke.author,
            'category': joke.category,
        }
        for joke in Joke.objects.all().order_by('id')
    ]
    return JsonResponse(jokes, safe=False)


def export_xml(request):
    root = ET.Element('jokes')
    for joke in Joke.objects.all().order_by('id'):
        joke_element = ET.SubElement(root, 'joke')
        ET.SubElement(joke_element, 'id').text = str(joke.id)
        ET.SubElement(joke_element, 'text').text = joke.text
        ET.SubElement(joke_element, 'author').text = joke.author
        ET.SubElement(joke_element, 'category').text = joke.category

    xml_bytes = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    return HttpResponse(xml_bytes, content_type='application/xml')


def import_jokes(request):
    form = ImportJokesForm()

    if request.method == 'POST':
        form = ImportJokesForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['xml_url']
            try:
                request_obj = urllib.request.Request(
                    url,
                    headers={'User-Agent': 'techJokes-importer'},
                )
                with urllib.request.urlopen(request_obj, timeout=10) as response:
                    xml_data = response.read()
            except (urllib.error.URLError, TimeoutError) as exc:
                messages.error(request, f'Could not reach remote server: {exc}')
            else:
                try:
                    root = ET.fromstring(xml_data)
                except ET.ParseError:
                    messages.error(request, 'Invalid XML received from remote server.')
                else:
                    imported_count = 0
                    skipped_count = 0
                    for joke_element in root.findall('joke'):
                        text = (joke_element.findtext('text') or '').strip()
                        author = (joke_element.findtext('author') or '').strip()
                        category = (joke_element.findtext('category') or '').strip()
                        if not text or not author:
                            continue
                        try:
                            Joke.objects.create(
                                text=text,
                                author=author,
                                category=category,
                            )
                            imported_count += 1
                        except IntegrityError:
                            skipped_count += 1

                    messages.success(
                        request,
                        f'Imported {imported_count} joke(s). Skipped {skipped_count} duplicate(s).',
                    )
                    return redirect('techJokes:import')

    return render(request, 'techJokes/import_jokes.html', {'form': form})

def ps2_index(request):
    return render(request, 'techJokes/ps2_index.html')


def sql_transcript(request):
    transcript_path = settings.BASE_DIR.parent / 'sql' / 'ps2_sql_transcript.sql'
    return FileResponse(transcript_path.open('rb'), content_type='text/plain')
