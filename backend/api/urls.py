from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('api/signup/',views.register_user, name='register_user'),
    path('api/verify/',views.verify_signup, name='verify_signup'),
    path('api/login/',views.user_login, name='user_login'),
    path('api/renew/',views.renew_tokens, name='renew_tokens'),
    path('api/logout/',views.logout_user, name='logout_user'),
    path('api/reset-password/',views.initiate_reset_password, name='initiate_reset_password'),
    path('api/confirm-reset-password/',views.confirm_reset_password, name='confirm_reset_password'),
    path('api/friendlist/',views.get_user_friends, name='get_user_friends'),
    path('api/resend-code/',views.get_resend_code, name='resend_code'),
    path('api/verify-user-access/',views.verify_user_access, name='verify_user_access'),
    path('api/user-profile/',views.get_user_profile, name='get_user_profile'),
    path('api/change-password/',views.change_password, name='change_password'),
    path('api/update-user-profile/',views.update_user_profile, name='update_user_profile'),
    path('api/send-friend-request/',views.send_friend_request, name='send_friend_request'),
    path('api/accept-friend-request/',views.accept_friend_request, name='accept_friend_request'),
    path('api/remove-friend/',views.remove_friend, name='remove_friend'),
    path('api/add-expense/',views.add_expense, name='add_expense'),
]