# API 로그인
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# TODO 3주차 설명, 이걸 사용해서 만들지 않으면, 페이로드에 user_id 만 들어갑니다. ㅜㅜ. 특히 is_staff 는 꼭 넣어주세요.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['gender_display'] = user.get_gender_display()
        token['gender'] = user.get_gender_display()
        token['name'] = user.name
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_active'] = user.is_active
        token['profile_img_url'] = user.profile_img_url

        return token


class ApiRefreshRefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    pass
