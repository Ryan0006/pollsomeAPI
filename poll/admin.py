from django.contrib import admin
from .models import Poll, Entry, Comment, Vote

admin.site.register(Poll)
admin.site.register(Entry)
admin.site.register(Comment)
admin.site.register(Vote)
