from rest_framework import serializers
from .models import Post, Vote  # 같은 앱 내이니까 .models


class PostSerializer(serializers.ModelSerializer):
    # 컬럼 읽기전용으로 만들기
    poster = serializers.ReadOnlyField(source="poster.username")
    poster_id = serializers.ReadOnlyField(source="poster.id")

    class Meta:
        model = Post  # 여기서 말하는 모델은 Post란다
        fields = ['id', 'title', 'url', 'poster', 'poster_id',
                  'created']  # id는 필수니깐.장고레스트에는 무조건 다 있음


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']  # vote id만 필요함!
