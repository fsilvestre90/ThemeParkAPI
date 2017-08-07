from magicride.modules.reviews.models import Review
from utilities import ModelSchema


class BaseReviewSchema(ModelSchema):
    class Meta:
        model = Review
        exclude = (
            Review.id.key,
        )


class ReviewSchema(BaseReviewSchema):
    class Meta:
        model = Review
        fields = (
            Review.description.key,
            Review.rating.key
        )
