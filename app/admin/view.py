from sqladmin import Admin, ModelView
from app.db.conn import engine
from app.db.models import (
    User,
    Genre,
    UserGenreSubscription,
    FavoriteSeries,
    ScheduledNotification,
)

from admin.auth import authentication_backend


class UserAdmin(ModelView, model=User):
    column_list = [
        "id",
        "tg_id",
        "created_at",
    ]
    column_searchable_list = [
        "id",
        "tg_id",
    ]
    column_sortable_list = [
        "id",
        "tg_id",
    ]
    can_export = False


class GenreAdmin(ModelView, model=Genre):
    column_list = [
        "id",
        "name",
    ]
    column_searchable_list = ["id", "name"]
    column_sortable_list = ["id", "name"]
    can_export = False


class UserGenreSubscriptionAdmin(ModelView, model=UserGenreSubscription):
    column_list = [
        "id",
        "user_id",
        "genre_id",
    ]
    column_searchable_list = [
        "id",
        "user_id",
        "genre_id",
    ]
    column_sortable_list = ["id"]
    can_export = False


class FavoriteSeriesAdmin(ModelView, model=FavoriteSeries):
    column_list = [
        "id",
        "user_id",
        "series_id",
        "title",
    ]
    column_searchable_list = [
        "id",
        "title",
    ]
    column_sortable_list = [
        "id",
        "title",
    ]
    can_export = False


class ScheduledNotificationAdmin(ModelView, model=ScheduledNotification):
    column_list = [
        "id",
        "user_id",
        "movie_id",
        "series_id",
        "release_date",
        "notified",
    ]
    column_searchable_list = [
        "id",
        "user_id",
        "movie_id",
        "series_id",
    ]
    column_sortable_list = [
        "id",
        "user_id",
        "movie_id",
        "series_id",
    ]
    can_export = False


def setup_admin(app):
    admin = Admin(
        app,
        engine,
        authentication_backend=authentication_backend,
        templates_dir="admin/templates",
        debug=True,
    )
    admin.add_view(UserAdmin)
    admin.add_view(GenreAdmin)
    admin.add_view(UserGenreSubscriptionAdmin)
    admin.add_view(FavoriteSeriesAdmin)
    admin.add_view(ScheduledNotificationAdmin)
