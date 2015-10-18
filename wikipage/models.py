from django.db import models

class WikiList(models.Model):
    url_name = models.CharField(primary_key=True, max_length=128, db_index=True)
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.url_name


class WikiPage(models.Model):
    url_name = models.CharField(primary_key=True, max_length=128, db_index=True)
    title = models.CharField(max_length=128)
    body = models.TextField(null=True)
    origin = models.URLField(null=True)
    lists = models.ManyToManyField("WikiList", db_index=True)
    categories = models.ManyToManyField("WikiCategory", db_index=True)

    def __str__(self):
        return self.url_name


class WikiCategory(models.Model):
    url_name = models.CharField(primary_key=True, max_length=128, db_index=True)
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.url_name

