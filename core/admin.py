from django.contrib import admin
from .models import Profile, Resume, Favorite, Notification

admin.site.register(Profile)
admin.site.register(Resume)
admin.site.register(Favorite)
admin.site.register(Notification)
