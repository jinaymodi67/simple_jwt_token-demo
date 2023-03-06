from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('signup',views.usercreateViews.as_view()),
    # path('login',views.LoginViews.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('createblog',views.CreateBlogViews.as_view()),
    path('listblog',views.ListBlogViews.as_view()),
    path('updateblog/<int:id>',views.UpdateBlogViews.as_view()),
    path('deleteblog/<int:id>',views.DeleteBlogViews.as_view()),

    path('adminview',views.Adminpanelview.as_view()),
    path('adminblogview',views.AdminBlogView.as_view()),
    path('adminuserupdateview/<int:id>',views.AdminUserUpdate.as_view()),
    path('adminuserdeleteview',views.AdminUserDelete.as_view()),
    path('adminblogupdateview/<int:id>',views.AdminBlogUpdate.as_view()),
    path('adminblogdeleteview/<int:id>',views.AdminBlogDelete.as_view()),
    path('adminuseractiveview/<int:id>',views.AdminUserActive.as_view()),
    path('userbloggraph/<int:id>',views.UserBlogCount.as_view()),


]