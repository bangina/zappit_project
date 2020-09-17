from rest_framework import serializers
from .models import Post, Vote  # 같은 앱 내이니까 .models


class PostSerializer(serializers.ModelSerializer):
    # 컬럼 읽기전용으로 만들기
    poster = serializers.ReadOnlyField(source="poster.username")
    poster_id = serializers.ReadOnlyField(source="poster.id")
    # field에 메소드 추가(votes는 원래 model에 없는 필드)
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post  # 여기서 말하는 모델은 Post란다
        fields = ['id', 'title', 'url', 'poster', 'poster_id',
                  'created', 'votes']  # id는 필수니깐.장고레스트에는 무조건 다 있음

    def get_votes(self, post):
        # 함수형태로 해당 post의 vote개수 셈
        return Vote.objects.filter(post=post).count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']  # vote id만 필요함!
