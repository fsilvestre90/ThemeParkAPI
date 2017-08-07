from flask import logging

from magicride.extensions import db
from magicride.extensions.api import api_v1
from magicride.modules.bookmarks.models import Bookmark
from magicride.modules.reviews.models import Review
from magicride.modules.rides.models import Ride
from magicride.modules.users.models import User
from magicride.modules.users.parameters import LoginParameters, CreateUserParameters, CreateReviewParameters
from magicride.modules.users.schemas import BaseUserSchema, LoginUserSchema
from utilities import Resource
from utilities._http import HTTPStatus

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

users_ns = api_v1.namespace(
    'users', description="User operations")  # pylint: disable=invalid-name


@users_ns.route('/')
class UsersIndex(Resource):
    @users_ns.response(code=HTTPStatus.UNPROCESSABLE_ENTITY)
    @users_ns.parameters(CreateUserParameters())
    @users_ns.response(BaseUserSchema())
    def post(self, args):
        """
        Create a new user.
        """
        if not User.find_user(args['email']):
            with users_ns.commit_or_abort(
                    db.session,
                    default_error_message="Failed to create a new user."
            ):
                new_user = User(**args)
                db.session.add(new_user)
            return new_user
        # TODO: find out why response isnt working when set to None
        return {"error": "{0} already taken".format(args['email'])}, 409


@users_ns.route('/login')
class UserLogin(Resource):
    @users_ns.response(LoginUserSchema())
    @users_ns.parameters(LoginParameters())
    @users_ns.response(code=HTTPStatus.CONFLICT)
    @users_ns.response(code=HTTPStatus.NO_CONTENT)
    def post(self, args):
        """
        Login a user.
        """
        return User.find_with_password(args['email'], args['password'])


@users_ns.route('/<int:user_id>/reviews')
@users_ns.resolve_object_by_model(User, 'user')
class ReviewsByUserID(Resource):
    @users_ns.response(BaseUserSchema())
    def get(self, user):

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
class SubmitBookmarkByUserID(Resource):
    @users_ns.response(BaseUserSchema())
    def post(self, user):
        """
        Submit a new bookmark.
        """
        return user


@users_ns.route('/<int:user_id>/bookmarks/<int:bookmark_id>')
@users_ns.resolve_object_by_model(User, 'user')
@users_ns.resolve_object_by_model(Bookmark, 'bookmark')
class EditBookmarkByUserID(Resource):
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
