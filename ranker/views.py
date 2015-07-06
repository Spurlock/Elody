from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from csv import DictReader
from ranker.models import Artist, Album
from ranker.functions import *
import random
from math import ceil


# Home page / Leaderboard
def index(request):
    albums = Album.objects.all().order_by('-current_rating')
    context = {
        'title': 'Leaderboard',
        'albums': albums
    }
    return render_to_response('ranker/index.html', context)


# Process the results of the previous match and present the next one
def match(request, select=None):

    if request.method == "POST":
        update_scores(request.POST['winner'], request.POST['loser'])
        return HttpResponseRedirect('/match/%s' % select)

    # Pair up albums for the next match. The "select" argument determines the algorithm
    # used to choose the albums.
    if select == 'random':
        albums = list(Album.objects.order_by('?')[0:2])

    elif select == 'fewest-matches':
        all_albums = Album.objects.all()
        for album in all_albums:
            album.matches = album.matches_won.count() + album.matches_lost.count()
        slice_size = max(int(len(all_albums) / 4), 2)
        candidate_albums = sorted(all_albums, key=lambda(x): x.matches)[0:slice_size]
        albums = [candidate_albums[0], random.choice(candidate_albums[1:])]

    elif select == 'closely-scored':
        all_albums = Album.objects.all().order_by('-current_rating')
        first_index = random.randrange(len(all_albums)-12)
        second_index = random.randrange(first_index+1, first_index+12)
        albums = [all_albums[first_index], all_albums[second_index]]

    elif select == 'smart':
        all_albums = Album.objects.all().order_by('-current_rating', 'title')

        # filter to all the albums tied for fewest matches, and choose one at random to be the first album
        potential_first_albums = []
        for index, album in enumerate(all_albums):
            album.matches = album.matches_won.count() + album.matches_lost.count()
            if not potential_first_albums or album.matches < potential_first_albums[0].matches:
                potential_first_albums = [album]
            elif album.matches == potential_first_albums[0].matches:
                potential_first_albums.append(album)

        print "%d albums remaining in round:" % len(potential_first_albums)
        print [album.title for album in potential_first_albums]

        first_album = random.choice(potential_first_albums)

        # remove the first album and its most recent opponents from the opponent candidate list.
        exclude_opponent_ids = []
        for match in first_album.matches_won.all().order_by('-id')[:3]:
            exclude_opponent_ids.append(match.loser_id)
        for match in first_album.matches_lost.all().order_by('-id')[:3]:
            exclude_opponent_ids.append(match.winner_id)
        all_albums = list(all_albums.exclude(id__in=exclude_opponent_ids))

        first_album_index = all_albums.index(first_album)
        all_albums.pop(first_album_index)

        # choose a suitable opponent, where the distance from first album is inversely related to its number of matches
        slice_size = len(all_albums) * ((5.0 ** (1 + first_album.matches)) / (6.0 ** (1 + first_album.matches)))
        slice_size = max(slice_size, 12)
        lower_bound = max(0, first_album_index - int(ceil(slice_size / 2)))
        upper_bound = min(len(all_albums), first_album_index + int(ceil(slice_size / 2)))
        second_album = random.choice(all_albums[lower_bound:upper_bound])

        albums = [first_album, second_album]

    # If we don't have album art for either of the chosen albums, try to grab it now
    for album in albums:
        if not album.artwork:
            album.artwork = get_thumb_url(album)
            album.save()

    random.shuffle(albums)

    context = RequestContext(request, {
        'title': 'Match',
        'select': select.replace("-", " ").title(),
        'albums': albums,
        'album_ids': "|".join([str(album.id) for album in albums])
    })
    return render_to_response('ranker/match.html', context)


# Figure out which albums have inconsistent star ratings. Inconsistent means that there are bunch of
# with higher Elo scores but lower star ratings, or vice versa.
def consistency_report(request):
    all_albums = Album.objects.all().order_by('-current_rating', 'title')

    adjustments = []
    for index, album in enumerate(all_albums):
        my_rating = album.star_rating
        better_albums = all_albums[0:index]
        worse_albums = all_albums[index:]

        needs_fewer_stars = len([a for a in better_albums if a.star_rating < my_rating])
        needs_more_stars = len([a for a in worse_albums if a.star_rating > my_rating])

        if needs_more_stars != needs_fewer_stars and (needs_more_stars > 0 or needs_fewer_stars > 0):
            adjustments.append({
                'album': album,
                'magnitude': abs(needs_more_stars - needs_fewer_stars),
                'needs_more': needs_more_stars,
                'needs_fewer': needs_fewer_stars
            })
    adjustments = sorted(adjustments, key=lambda i: i['magnitude'], reverse=True)

    context = {
        'title': 'Evaluate Star Ratings',
        'adjustments': adjustments
    }
    return render_to_response('ranker/consistency_report.html', context)


def import_rym(request):

    #REMEMBER: the rym csv file has an extra space before "first name" in the headers row. take it out.

    return  # lets not run this again by accident

    rym_rows = {}
    with open('rym-050514.csv') as csvfile:
        rym_reader = DictReader(csvfile, delimiter=',')
        for row in rym_reader:
            artist = row['First Name'] + ' ' + row['Last Name'] if row.get('First Name') else row['Last Name']
            album = {'title': row['Title'], 'star_rating': row['Rating']}

            # Special hack to avoid importing my band
            if artist != "Doctor Squid":
                if rym_rows.get(artist):
                    rym_rows[artist].append(album)
                else:
                    rym_rows[artist] = [album]

    for artist_name, albums in rym_rows.iteritems():
        artist = Artist(name=artist_name)
        artist.save()
        for info in albums:
            album = Album(title=info['title'], artist=artist, star_rating=info['star_rating'])
            album.save()

    return render_to_response('ranker/import_rym.html', {'rym_rows':rym_rows})