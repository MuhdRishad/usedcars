from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,TemplateView,FormView,UpdateView,View
from cars.forms import SignupForm,SigninForm,ProfileForm,SellCarsForm,PasswordChangeForm,MessagesForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from cars.models import UserProfile,Cars,Messages
from django.contrib import messages
from django.utils.decorators import method_decorator

# Create your views here.


#Cannot access without signin
def signin_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            messages.error(request,"Please Login")
            return redirect("sign-in")
    return wrapper


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
@signin_required
def signout(request,*args,**kwargs):
    logout(request)
    return redirect('sign-in')


# This is the home page view
@method_decorator(signin_required,name="dispatch")
class HomeView(TemplateView):
    template_name = "home.html"


# This view is for Adding profile for user
@method_decorator(signin_required,name="dispatch")
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
@method_decorator(signin_required,name="dispatch")
class ViewProfileView(TemplateView):
    template_name = "view-profile.html"


# For updating user profile details
@method_decorator(signin_required,name="dispatch")
class ProfileUpdate(UpdateView):
     template_name = "profile-update.html"
     form_class = ProfileForm
     model = UserProfile
     success_url = reverse_lazy('home')


# View for selling cars
@method_decorator(signin_required,name="dispatch")
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
@method_decorator(signin_required,name="dispatch")
class ViewCarsView(TemplateView):
    template_name = "view-cars.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_cars = Cars.objects.all().exclude(user=self.request.user)
        context["cars"] = all_cars
        return context


# This view for more details about cars
@method_decorator(signin_required,name="dispatch")
class ViewCarDetailView(TemplateView):
    template_name = "view-car-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = kwargs.get("pk")
        car = Cars.objects.get(id=car_id)
        context["car_details"] = car
        return context


# If Current user added cars to sell , To see them
@method_decorator(signin_required,name="dispatch")
class MyCarListView(TemplateView):
    template_name = "my-car-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cars = Cars.objects.filter(user=self.request.user)
        context["my_car_list"] = cars
        return context


# View for Updating car details
@method_decorator(signin_required,name="dispatch")
class UpdateCarDetails(UpdateView):
    template_name = "update-car-details.html"
    model = Cars
    form_class = SellCarsForm
    success_url = reverse_lazy("my-cars-list")

# This function is for deleting car
@signin_required
def remove_car(request,*args,**kwargs):
    car_id = kwargs.get("pk")
    car = Cars.objects.get(id=car_id)
    car.delete()
    return redirect("home")


#For Changing password
@method_decorator(signin_required,name="dispatch")
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


class MessagesView(TemplateView):
    template_name = "messages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = kwargs.get("pk")
        car = Cars.objects.get(id=car_id)
        context["car_details"] = car
        return context

class SentMessagesView(CreateView):
    model = Messages
    template_name = "messages.html"
    form_class = MessagesForm

    def post(self, request, *args, **kwargs):
        owner_id = kwargs.get("pk")
        owner = User.objects.get(id = owner_id)
        user = request.user
        message = request.POST.get("message")
        Messages.objects.create(message = message , user = user , reciever = owner)
        return redirect("home")

def enquiries(request,*args,**kwargs):
    user_id = request.user.id
    messages = Messages.objects.filter(reciever = user_id)
    return render(request , "enquires.html" , {"messages":messages})

def delete_message(request,*args,**kwargs):
    message_id = kwargs.get("pk")
    message = Messages.objects.get(id = message_id)
    message.delete()
    return redirect("home")
