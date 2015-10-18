from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render

from .models import PageKeyword
from .tasks import parse_all

class SearchAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'count', 'page')
    search_fields = ['keyword']

    def get_urls(self):
        urls = super(SearchAdmin, self).get_urls()
        my_urls = [
            url(r'^parse/$',
                self.admin_site.admin_view(self.to_parse))
        ]
        return my_urls + urls

    def to_parse(self, request):
        parse_all.delay()

        context = dict(
            self.admin_site.each_context(request),
        )
        return render(request, 'admin/to_parse.html', context)

admin.site.register(PageKeyword, SearchAdmin)
