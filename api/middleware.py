from urllib.parse import parse_qs

from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.db import close_old_connections


User = get_user_model()


class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()

        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        scope["user"] = AnonymousUser()

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token["user_id"]
                user = await self.get_user(user_id)
                scope["user"] = user
            except (InvalidToken, TokenError, User.DoesNotExist, KeyError):
                scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @staticmethod
    async def get_user(user_id):
        from channels.db import database_sync_to_async

        @database_sync_to_async
        def _get_user():
            return User.objects.get(id=user_id)

        return await _get_user()