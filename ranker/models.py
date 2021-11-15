from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    current_rating = models.IntegerField(default=1000)
    artwork = models.CharField(null=True, max_length=250, blank=True)
    star_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.artist.name, self.title)


class Match(models.Model):
    winner = models.ForeignKey(Album, related_name="matches_won", on_delete=models.PROTECT)
    winner_rating = models.IntegerField()
    loser = models.ForeignKey(Album, related_name="matches_lost", on_delete=models.PROTECT)
    loser_rating = models.IntegerField()