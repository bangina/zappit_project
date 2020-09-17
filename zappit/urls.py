
from django.contrib import admin
from django.urls import path
from posts import views  # views 파일의 posts를 가져옴

urlpatterns = [
    path('admin/', admin.site.urls),
    # Post DB쿼리셋을 모두 보여주는 뷰를 보여쥬는 주소
    path('api/posts', views.PostList.as_view()),
    path('api/posts/<int:pk>/vote', views.VoteCreate.as_view()),  # 투표하기
]
