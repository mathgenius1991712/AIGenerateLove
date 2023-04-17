from django.contrib import admin

from mainapp.models import Type, Question, Media, Prompt,CustomUser 

admin.site.register(Type)
admin.site.register(Question)
admin.site.register(Media)
admin.site.register(Prompt)
admin.site.register(CustomUser)

# Register your models here.
