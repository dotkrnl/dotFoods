from django.db import models

from dotFoods.settings import MAX_LEN_KEYWORD
from wikipage.models import WikiPage

class PageKeyword(models.Model):
    keyword = models.CharField(max_length=MAX_LEN_KEYWORD, db_index=True)
    count = models.FloatField()
    page = models.ForeignKey(WikiPage, db_index=True)

    def __str__(self):
        return self.keyword
