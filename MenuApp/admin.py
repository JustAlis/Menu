from django.contrib import admin
from .models import *

class MenuAdmin(admin.ModelAdmin):
    ordering = ['menu_name', 'parent']
    list_display = ('name','children','parent','menu_name','slug',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('menu_name','parent')
    autocomplete_fields = ('parent',)
    list_select_related = ('parent',)
    list_per_page = 100
    #убрана возможность вручную выставлять слаг, чтобы избегать багов, связанных 
    #с уникальнотью поля 'slug' модели 'Menu'. В любом случе слаг задаётся автоматически
    exclude = ["slug"]

    def get_queryset(self, request):
        self.qs = super(MenuAdmin,self).get_queryset(request).prefetch_related('children')
        return self.qs
    
    def children(self, obj):
        return (*obj.children.all(),)
    
    children.short_description = 'Подпункты'

admin.site.register(Menu, MenuAdmin)