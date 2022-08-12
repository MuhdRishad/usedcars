from django.urls import path
from cars import views

urlpatterns = [
    path('account/signup',views.SignupView.as_view(),name="sign-up"),
    path('account/signin',views.SigninView.as_view(),name="sign-in"),
    path('account/signout',views.signout,name="sign-out"),
    path('home',views.HomeView.as_view(),name="home"),
    path('user/profile/add',views.ProfileView.as_view(),name="profile-add"),
    path('user/profile/view',views.ViewProfileView.as_view(),name="profile-view"),
    path('user/profile/update/<int:pk>',views.ProfileUpdate.as_view(),name="profile-update"),
    path('user/change/password',views.ChangePassword.as_view(),name="change-password"),
    path('user/car/add',views.SellCarsView.as_view(),name="sell-car"),
    path('user/all/cars/list',views.ViewCarsView.as_view(),name="view-cars"),
    path('user/car/details/<int:pk>',views.ViewCarDetailView.as_view(),name="view-car-details"),
    path('user/cars/list',views.MyCarListView.as_view(),name="my-cars-list"),
    path('user/car/details/update/<int:pk>',views.UpdateCarDetails.as_view(),name="update-car-details"),
    path('user/car/remove/<int:pk>',views.remove_car,name="remove-car")
]