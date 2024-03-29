from __future__ import division
from ranker.models import Album, Match
from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen
import json
import Elody.environment as env


def update_scores(winner_id, loser_id):

    winner = Album.objects.get(id=winner_id)
    loser = Album.objects.get(id=loser_id)

    # Record the match
    match = Match(winner=winner, loser=loser, winner_rating=winner.current_rating, loser_rating=loser.current_rating)
    match.save()

    # Compute the numbers we need in order to update the albums' scores.
    winner_expected = 1 / (1 + 10**((loser.current_rating - winner.current_rating)/400))
    loser_expected = 1 - winner_expected
    winner_k = get_k_factor(winner)
    loser_k = get_k_factor(loser)

    # Compute the updated scores
    winner_new = winner.current_rating + winner_k * (1 - winner_expected)
    loser_new = loser.current_rating + loser_k * (0 - loser_expected)

    # print("WINNER: %d K, %0.1f%% chance, %d -> %0.0f" % (winner_k, winner_expected*100, winner.current_rating, winner_new))
    # print("LOSER:  %d K, %0.1f%% chance, %d -> %0.0f" % (loser_k, loser_expected*100, loser.current_rating, loser_new))

    # Save the updated scores
    winner.current_rating = int(round(winner_new))
    loser.current_rating = int(round(loser_new))
    winner.save()
    loser.save()


def get_k_factor(album):
    total_matches = album.matches_won.count() + album.matches_lost.count()
    return max(40 - total_matches, 10)


# Fetch the album art URL from last.fm
def get_thumb_url(album):
    # TODO: Use unidecode to handle special characters
    try:
        params = urlencode({
            'method': 'album.getinfo',
            'api_key': env.AUDIO_SCROBBLER_API_KEY,
            'artist': album.artist.name,
            'album': album.title,
            'format': 'json'
        })

        response = urlopen(urlencode(params, quote_via=quote_plus))
        if response:
            raw_response = response.read()
            album_info = json.loads(raw_response)
            image_url = album_info['album'].get('image')[2].get('#text')
            return image_url
    except Exception:
        return ""
    return ""
