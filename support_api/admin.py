from django.contrib import admin

from support_api.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'status')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'created', 'author')
    search_fields = ('text', 'author', 'created')
    list_filter = ('created', 'author', 'text')
    empty_value_display = '-пусто-'


class PostInline(admin.TabularInline):
    model = Post
    raw_id_fields = ('group',)
    max_num = 1
    readonly_fields = ('text',)
    can_delete = False
    fields = ('text',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
