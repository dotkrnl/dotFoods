from django.db import models

class BotoFinished(models.Model):
    url = models.CharField(primary_key=True, max_length=128, db_index=True)

    def __str__(self):
        return self.url

