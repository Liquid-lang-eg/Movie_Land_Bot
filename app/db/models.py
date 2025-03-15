from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, TEXT, DateTime, func, Integer, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import String, ForeignKey, Boolean, DateTime, Integer, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass

# Пользователи
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[Optional[int]] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    genre_subscriptions: Mapped[List["UserGenreSubscription"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    # favorite_movies: Mapped[List["FavoriteMovie"]] = relationship(
    #     back_populates="user", cascade="all, delete-orphan"
    # )
    favorite_series: Mapped[List["FavoriteSeries"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

# Жанры
class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


# Подписка на жанры
class UserGenreSubscription(Base):
    __tablename__ = "user_genre_subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="genre_subscriptions")
    genre: Mapped["Genre"] = relationship()

# Любимые фильмы
# class FavoriteMovie(Base):
#     __tablename__ = "favorite_movies"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
#     movie_id: Mapped[int] = mapped_column(Integer)  # ID фильма в TMDB
#     title: Mapped[str] = mapped_column(String(255))
#
#     user: Mapped["User"] = relationship(back_populates="favorite_movies")

# Любимые сериалы
class FavoriteSeries(Base):
    __tablename__ = "favorite_series"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    series_id: Mapped[int] = mapped_column(Integer)  # ID сериала в TMDB
    title: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="favorite_series")

# Запланированные уведомления о релизах
class ScheduledNotification(Base):
    __tablename__ = "scheduled_notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    movie_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # ID фильма, если это фильм
    series_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # ID сериала, если это сериал
    release_date: Mapped[Date] = mapped_column(Date)
    notified: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship()