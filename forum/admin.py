from django.contrib import admin
from .models import Post, Comment

# Register Post model
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  
    search_fields = ('title', 'author__username')    
    list_filter = ('created_at', 'author')            

# Register Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')  
    search_fields = ('post__title', 'author__username')
    list_filter = ('created_at', 'author')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
