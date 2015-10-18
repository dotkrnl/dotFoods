from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import BotoFinished
from .forms import NewRootForm
from .tasks import crawl_page

class BotoAdmin(admin.ModelAdmin):
    list_display = ('url',)
    search_fields = ['url']

    def get_urls(self):
        urls = super(BotoAdmin, self).get_urls()
        my_urls = [
            url(r'^new/$',
                self.admin_site.admin_view(self.new_root))
        ]
        return my_urls + urls

    def new_root(self, request):
        # if this is a POST request
        if request.method == 'POST':
            # create a form instance and populate
            # it with data from the request:
            form = NewRootForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                root = form.cleaned_data['new_root']
                depth = form.cleaned_data['depth']
                crawl_page.delay(root, depth=depth)
                # redirect to a new URL:
                return HttpResponseRedirect('/admin/')

        # if a GET (or any other method)
        else:
            form = NewRootForm()

        context = dict(
            self.admin_site.each_context(request),
            form=form,
        )
        return render(request, 'admin/new_root.html', context)


admin.site.register(BotoFinished, BotoAdmin)
