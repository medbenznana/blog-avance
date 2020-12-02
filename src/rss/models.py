from django.db import models


class Feed(models.Model):
    url = models.URLField(max_length=255, unique=True)

    def __repr__(self):
        return "<Feed '{}'>".format(self.url)