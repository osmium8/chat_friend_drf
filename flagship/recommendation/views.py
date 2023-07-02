from recommendation.sample_data.sample_data import user_data
from heapq import nsmallest
from operator import itemgetter
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RecommendationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        response = self.get_top_five_recommended_users(user_id)
        return Response({'user_id': user_id, 'recommended_users': response}, status=status.HTTP_200_OK)

    def get_top_five_recommended_users(self, user_id: int):
        """
        Helper function to return top 5 recommended users to chat with based on interest

        Time complexity: O(N * log(5))
        Space complexity: O(N)

        where N is the number of data objects corresponding to user interests

        """
        user_interests_data = user_data['user_interests']
        interests_delta_mapping = self.get_interests_delta_mapping(user_id, user_interests_data)
        
        # N * log 5
        top_five_recommended_users = nsmallest(5, interests_delta_mapping, key=itemgetter(1))

        # N * Log N
        # top_five_recommended_users = sorted(interests_delta_mapping, key=lambda x: x[1], reverse=False)[:5]

        return top_five_recommended_users

    def get_interests_delta_mapping(self, user_id: int, user_interests_data: list):
        """Helper function to get interest delta for a given user id"""
        target_user = self.get_user(user_id, user_interests_data)
        interests_delta_mapping: list = list()
        for user in user_interests_data:
            if (user['id'] == user_id):
                continue
            interests_delta = self.get_interests_delta(
                target_user['interests'], user['interests'])
            interests_delta_mapping.append((user, interests_delta))
        return interests_delta_mapping

    def get_interests_delta(self, target_user_interests: dict, other_user_interests: dict) -> int:
        """Helper function to calculate delta based on interest parameters"""
        interests_params: list[str] = [
            "music", "photography", "dancing", "drawing", "cars", "cooking"]
        interests_delta: int = 0

        for interests in interests_params:
            interests_delta += abs(target_user_interests.get(interests,
                                   0) - other_user_interests.get(interests, 0))

        return interests_delta

    def get_user(self, user_id: int, user_interests_data: list):
        for user in user_interests_data:
            if user['id'] == user_id:
                return user
        return {}
