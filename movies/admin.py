from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ('id', "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="110" height="80">')
    
    get_image.short_description = "Кадры"
    

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft",)
    list_filter = ("category", "year",)
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"), )
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"),)
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ('Actor/directors', {
            'classes': ('collapse',),
            "fields": (('actors', 'directors', 'genres', 'category'), )
        }),
        (None, {
            "fields": (('budget', 'fees_in_usa', 'fees_in_world'), )
        }),
        ('Option', {
            "fields": (('url', 'draft'), )
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="70" height="100">')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1  запись была обновлена'
        elif row_update > 1 and row_update < 5:
            message_bit = f'{row_update} записи были обновлены'
        else:
            message_bit = f'{row_update} записей было обновлено'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1  запись была обновлена'
        elif row_update > 1 and row_update < 5:
            message_bit = f'{row_update} записи были обновлены'
        else:
            message_bit = f'{row_update} записей было обновлено'
        self.message_user(request, f'{message_bit}')
    
    publish.short_description = 'Опубликовать'
    publish.allowed_permission = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permission = ('change',)


    get_image.short_description = "Постер"

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актёры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры к фильму"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="70" height="50">')

    get_image.short_description = "Кадры"




admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"