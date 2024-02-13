from django.urls import path

from users.apis import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('change_password/', views.ChangePasswordView.as_view(), name="change_password"),
    path('reset_password/', views.ResetPasswordView.as_view(), name="reset_password"),
    path("token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path('list/', views.UserlistingView.as_view(), name="users_data"),
    path('add_user/', views.AddUserView.as_view(), name="add_user"),
]
