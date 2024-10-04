from django.db import models

class ReviewEntry(models.Model):
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    review = models.TextField()
    rating = models.IntegerField()

    @property
    def good_rating(self):
        return self.rating > 3