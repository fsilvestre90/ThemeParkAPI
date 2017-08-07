from flask import logging

from magicride.extensions.api import api_v1
from magicride.modules.bookmarks.models import Bookmark
from magicride.modules.reviews.models import Review
from magicride.modules.users.models import User
from magicride.modules.users.schemas import BaseUserSchema
from utilities import Resource

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

users_ns = api_v1.namespace(
    'users', description="User operations")  # pylint: disable=invalid-name


@users_ns.route('/')
class UserByID(Resource):

    @users_ns.response(BaseUserSchema())
    def get(self, user):
        """
        Login a user.
        """
        return user

    @users_ns.response(BaseUserSchema())
    def post(self, user):
        """
        Create a new user.
        """
        return user


@users_ns.route('/<int:user_id>/reviews')
@users_ns.resolve_object_by_model(User, 'user')
class UserByID(Resource):

    @users_ns.response(BaseUserSchema())
    def post(self, user):
        """
        Submit a new user review.
        """
        return user


@users_ns.route('/<int:user_id>/reviews/<int:review_id>')
@users_ns.resolve_object_by_model(User, 'user')
@users_ns.resolve_object_by_model(Review, 'review')
class BookmarkByUserID(Resource):
    @users_ns.response(BaseUserSchema())
    def put(self, user, review):
        """
        Update a users review.
        """
        return user

    @users_ns.response(BaseUserSchema())
    def delete(self, user):
        """
        Remove a users review.
        """
        return user


@users_ns.route('/<int:user_id>/bookmarks')
@users_ns.resolve_object_by_model(User, 'user')
class BookmarkByUserID(Resource):
    @users_ns.response(BaseUserSchema())
    def post(self, user):
        """
        Submit a new bookmark.
        """
        return user


@users_ns.route('/<int:user_id>/bookmarks/<int:bookmark_id')
@users_ns.resolve_object_by_model(User, 'user')
@users_ns.resolve_object_by_model(Bookmark, 'bookmark')
class BookmarkByUserID(Resource):
    @users_ns.response(BaseUserSchema())
    def put(self, user, bookmark):
        """
        Update a bookmark.
        """
        return user

    @users_ns.response(BaseUserSchema())
    def delete(self, user, bookmark):
        """
        Delete a bookmark.
        """
        return user
