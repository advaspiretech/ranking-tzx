from django.urls import path
from .views import HomePageView, LoginPageView, StaffPageView, StudentPageView, ModifyPageView, HistoryPageView,LogoutView,LessonView,LessonCreateView,TransferPageView,AttendanceMarkingView
from django.conf import settings
from django.conf.urls.static import static


#类视图（class-based views）
#我开那一个页面的时候才会启动那一个页面的class view
urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('staff/', StaffPageView.as_view(), name='staff'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('student/', StudentPageView.as_view(), name='student'),
    path('modify/', ModifyPageView.as_view(), name='modify'),
    path('history/', HistoryPageView.as_view(), name='history'),
    path('lesson_view/', LessonView.as_view(), name='lesson_view'),
    path('lesson_create/', LessonCreateView.as_view(), name='lesson_create'),
    path('transfer/', TransferPageView.as_view(), name='transfer'),
    path('attendance/marking/', AttendanceMarkingView.as_view(), name='attendance'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#函数视图（function-based views）
#from . import views
# urlpatterns = [
#     path('home/', views.home, name='home'),
#     path('login/', views.login, name='login'),
#     path('staff/', views.staff, name='staff'),
#     path('logout/', views.logout, name='logout'),
#     path('student/', views.student, name='student'),
#     path('modify/', views.modify, name='modify'),
#     path('history/', views.history, name='history'),
# ]

