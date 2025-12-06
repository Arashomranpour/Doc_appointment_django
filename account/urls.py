from django.urls import path

from . import views

app_name="account"
urlpatterns=[path("login",views.UserLoginView.as_view(),name="login"),
             path("logout",views.UserLogoutView,name="logout"),
             path("register",views.UserSignUpView.as_view(),name="register"),
             path("checkotp",views.Checkotpview.as_view(),name="checkotp"),

             path("otplogin",views.OtploginView.as_view(),name="otplogin"),

             # path("add_address",views.AddAddressView.as_view(),name="add_address"),
             path("set_password/", views.SetPasswordView.as_view(), name="set_password"),
             path("profile/",views.ProfileUpdateView.as_view(), name="profile_update"),
             path("DeleteProfile/",views.DeleteProfileView.as_view(), name="DeleteProfile"),
             path("contactus/", views.ContactusView.as_view(), name="contactus"),
             path("allmessages/", views.MessageListView.as_view(), name="allmessages"),
             path("allmessages/delete/<int:pk>", views.MessageDelete.as_view(), name="MessageDelete"),

             ]