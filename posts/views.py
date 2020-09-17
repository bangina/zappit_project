from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
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


# post건 삭제하기!(RetrieveDestroyAPIView: reade&delete)
class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 작성자만 삭제가능

    # 삭제하는 함수
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(
            pk=self.kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("그쪽 게시물이 아닌데용!!! 못 지우세요!!")


# 투표하기 & un투표하기
class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        # obj를 중복생성하는 걸 막기(아래 코드 없으면 vote할 때마다 obj하나씩 생성함)
        if self.get_queryset().exists():
            raise ValidationError("이미 투표하셨어요! :)")
            # 시리얼라이저야, 저장할 때 poster컬럼은 POST요청자 이름을 넣어
        serializer.save(voter=self.request.user,
                        post=Post.objects.get(pk=self.kwargs['pk']))  # post

  # vote삭제하는 함수 정의

    def delete(self, request, *args, **kwargs):
        # 만약 이미 쿼리셋 존재한다면
        if self.get_queryset().exists():
            self.get_queryset().delete()  # 나 자신 삭제해
            return Response(status=status.HTTP_204_NO_CONTENT)  # 응답 메시지도 보내준다.
        else:
            raise ValidationError("으아니 투표하신 적이 없는데요?뭘 삭제하신단건지..")
