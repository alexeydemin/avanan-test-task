from django.contrib import admin
from django.urls import path, include
from actions.views import slack_hook, entry_hook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/hook/', slack_hook, name='slack_hook'),
    path('event/entry_hook/', entry_hook, name='entry_hook'),
]
