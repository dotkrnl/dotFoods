from django.contrib import admin
from wikipage.models import WikiList, WikiPage, WikiCategory

class WikiListAdmin(admin.ModelAdmin):
    list_display = ('url_name', 'title')
    search_fields = ['url_name', 'title']

class WikiPageAdmin(admin.ModelAdmin):
    list_display = ('url_name', 'title', 'origin')
    search_fields = ['url_name', 'title']

class WikiCategoryAdmin(admin.ModelAdmin):
    list_display = ('url_name', 'title')
    search_fields = ['url_name', 'title']


admin.site.register(WikiList, WikiListAdmin)
admin.site.register(WikiCategory, WikiCategoryAdmin)
admin.site.register(WikiPage, WikiPageAdmin)
