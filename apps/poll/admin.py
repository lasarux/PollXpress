from django.contrib import admin
from models import Poll, Query, Option, Person, Ballot, Space

class OptionInline(admin.TabularInline):
    model = Option
    extra = 3
    fields = ['name', 'description']

class QueryAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('name', 'date_creation', 'description')

class PersonAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'space']
    list_display = ['name', 'email']
    
class BallotAdmin(admin.ModelAdmin):
    list_display = ['uid', 'person', 'sent', 'done']
    
class SpaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    
class PollAdmin(admin.ModelAdmin):
    list_display = ['query', 'space', 'date_published', 'date_finish']

admin.site.register(Poll, PollAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Ballot, BallotAdmin)
admin.site.register(Space, SpaceAdmin)


