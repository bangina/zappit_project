
from django.contrib import admin
from django.urls import path, include
from posts import views  # views 파일의 posts를 가져옴

urlpatterns = [
    path('admin/', admin.site.urls),
    # Post DB쿼리셋을 모두 보여주는 뷰를 보여쥬는 주소
    path('api/posts/', views.PostList.as_view()),  # post 리스트 뷰
    path('api/posts/<int:pk>', views.PostRetrieveDestroy.as_view()),  # post 아이템 뷰
    path('api/posts/<int:pk>/vote', views.VoteCreate.as_view()),  # 투표하기 POST뷰
    # 요거 한줄만 추가하면???우측 상단에 login버튼 생김!
    path('api-auth/', include('rest_framework.urls'))
]
