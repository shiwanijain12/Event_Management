from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Participant)
admin.site.register(Product)
admin.site.register(Event)
admin.site.register(Tag)
