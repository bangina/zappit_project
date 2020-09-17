from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer

# ListAPIView -> Allow: GET, HEAD, OPTIONS
# ListCreateAPIView -> Allow: GET, "POST", HEAD, OPTIONS


class PostList(generics.ListCreateAPIView):  # 뷰 기반의 클래스 생성
    # 뭘 보여줄거야
    queryset = Post.objects.all()  # DB에서 쿼리셋 전부 가져왕
    serializer_class = PostSerializer
    # IsAuthenticated:로그인유저만 /IsAuthenticatedOrReadOnly: 로그인유저는 post가능,아니면 readonly
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 예약어임
    def perform_create(self, serializer):
        # 시리얼라이저야, 저장할 때 poster컬럼은 POST요청자 이름을 넣어
        serializer.save(poster=self.request.user)

# 투표하기


class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.object.filter(voter=user, post=post)

    def perform_create(self, serializer):
        # 시리얼라이저야, 저장할 때 poster컬럼은 POST요청자 이름을 넣어
        serializer.save(voter=self.request.user,
                        post=Post.objects.get(pk=self.kwargs['pk']))  # post
