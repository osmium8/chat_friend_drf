from django.urls import path
from recommendation.views import RecommendationView

urlpatterns = [
    path('recommendation/<int:user_id>/friends', RecommendationView.as_view(), name='suggestedFriends')
]
