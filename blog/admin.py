from django.contrib import admin
from .models import TravelPost, Category, Tag, Comment
from .models import Profile

class TravelPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published')
    list_filter = ('published', 'category', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    search_fields = ('author', 'content')

admin.site.register(TravelPost, TravelPostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)
