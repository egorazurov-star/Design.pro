from django.contrib import admin

from .models import Category, DesignRequest

admin.site.register(Category)


@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
