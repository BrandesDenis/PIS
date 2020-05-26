from django.contrib import admin
from apps.thoughts.models import Paragraph, Topic, Thought

admin.site.register(Paragraph)
admin.site.register(Topic)
admin.site.register(Thought)