
async def get_genres():
    return await fetch_from_backend("/subscription/genres/")


async def get_user_subscriptions(tg_id: int):
    params = {"user_tg_id": tg_id}
    return await fetch_from_backend("/subscription/subscriptions/", params=params)


async def subscribe_genre(tg_id: int, genre_id: int):
    data = {"user_tg_id": tg_id, "genre_id": genre_id}
    return await fetch_from_backend("/subscription/subscribe/", method="POST", data=data)


async def unsubscribe_genre(tg_id: int, genre_id: int):
    data = {"user_tg_id": tg_id, "genre_id": genre_id}
    return await fetch_from_backend("/subscription/unsubscribe/", method="DELETE", data=data)
