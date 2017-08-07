from werkzeug.security import generate_password_hash, check_password_hash

from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin
from magicride.modules.reviews.models import Review
from magicride.modules.bookmarks.models import Bookmark


class User(ResourceMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # Authentication
    email = db.Column(db.String(255), unique=True, index=True, nullable=False,
                      default='')
    password = db.Column(db.String(128), nullable=False, default='')

    # Relationships
    reviews = db.relationship(Review, backref='users',
                              passive_deletes=True)

    bookmarks = db.relationship(Bookmark, backref='users',
                                passive_deletes=True)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(User, self).__init__(**kwargs)

        self.password = User.encrypt_password(kwargs.get('password', ''))

    @classmethod
    def find_with_password(cls, email, password):
        """
        :param email: email to search
        :param password: password in plain text
        :return: User instance, none if not found
        """
        user = cls.query.filter_by(email=email).first()
        if not user:
            return None

        if check_password_hash(user.password, password):
            return user
        return None

    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using PBKDF2.
        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return generate_password_hash(plaintext_password)

        return None
