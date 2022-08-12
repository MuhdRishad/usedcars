from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,TemplateView,FormView,UpdateView,View
from cars.forms import SignupForm,SigninForm,ProfileForm,SellCarsForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from cars.models import UserProfile,Cars


# Create your views here.


# This view is for user registration
class SignupView(CreateView):
    form_class = SignupForm
    template_name = "sign-up.html"
    model = User
    success_url = reverse_lazy("sign-in")


# This view is for user login
class SigninView(FormView):
    form_class = SigninForm
    template_name = "sign-in.html"
    model = User

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect("home")
            else:
                return render(request, self.template_name, {"form": form})
        else:
            return render(request, self.template_name, {"form": form})


# This function for user logout
def signout(request,*args,**kwargs):
    logout(request)
    return redirect('sign-in')


# This is the home page view
class HomeView(TemplateView):
    template_name = "home.html"


# This view is for Adding profile for user
class ProfileView(CreateView):
    model = UserProfile
    template_name = "profile-add.html"
    form_class = ProfileForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)


# For seeing user profile . Also we can see some registration details except password .In this page details not updatable
class ViewProfileView(TemplateView):
    template_name = "view-profile.html"


# For updating user profile details
class ProfileUpdate(UpdateView):
     template_name = "profile-update.html"
     form_class = ProfileForm
     model = UserProfile
     success_url = reverse_lazy('home')


# View for selling cars
class SellCarsView(CreateView):
    form_class = SellCarsForm
    template_name = "sell-car.html"
    model = Cars
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)


# View for all cars , can see limited data
class ViewCarsView(TemplateView):
    template_name = "view-cars.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_cars = Cars.objects.all()
        context["cars"] = all_cars
        return context


# This view for more details about cars
class ViewCarDetailView(TemplateView):
    template_name = "view-car-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = kwargs.get("pk")
        car = Cars.objects.get(id=car_id)
        context["car_details"] = car
        return context


# If Current user added cars to sell , To see them
class MyCarListView(TemplateView):
    template_name = "my-car-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cars = Cars.objects.filter(user=self.request.user)
        context["my_car_list"] = cars
        return context


# View for Updating car details
class UpdateCarDetails(UpdateView):
    template_name = "update-car-details.html"
    model = Cars
    form_class = SellCarsForm
    success_url = reverse_lazy("my-cars-list")

# This function is for deleting car
def remove_car(request,*args,**kwargs):
    car_id = kwargs.get("pk")
    car = Cars.objects.get(id=car_id)
    car.delete()
    return redirect("home")


class ChangePassword(FormView):
    form_class = PasswordChangeForm
    template_name = "change-password.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            old_pwd = form.cleaned_data.get("old_password")
            new_pwd = form.cleaned_data.get("new_password")
            confirm_pwd = form.cleaned_data.get("confirm_password")
            user = authenticate(request,username=request.user.username,password=old_pwd)
            if user and new_pwd == confirm_pwd:
                user.set_password(confirm_pwd)
                user.save()
                return redirect("sign-in")
            else:
                return render(request,self.template_name,{"form":form})