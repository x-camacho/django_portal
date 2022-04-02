from ast import Str
from re import S
from django import http
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View #handles views
from django.http import HttpResponse # handles responses
from .models import Location, Report
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
#AUTH STUFF#
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

#create home class and extend with view
class Home(TemplateView):
    template_name = 'home.html'

class LocationList(TemplateView):
    template_name = 'locationlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["locations"] = Location.objects.filter(name_icontains=name)
            context["header"] = f"Searching for {name}"
        else:
            context["locations"] = Location.objects.all() # this is where we add the key into our context object for the view to use
        return context

@method_decorator(login_required, name='dispatch')
class LocationCreate(CreateView):
    model = Location
    fields = ['name', 'location_number', 'city', 'state', 'reports', 'user']
    template_name = "location_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/locations')


class LocationDetail(DetailView):
    model = Location
    template_name = "location_detail.html"

@method_decorator(login_required, name='dispatch')
class LocationUpdate(UpdateView):
    model = Location
    fields = ['name', 'location_number', 'city', 'state', 'reports', 'user']
    template_name = "location_create.html"

    def get_success_url(self):
        return reverse('location_detail', kwargs={'pk': self.object.pk}) 

@method_decorator(login_required, name='dispatch')
class LocationDelete(DeleteView):
    model = Location
    template_name = "location_delete_confirmation.html"
    success_url = "/locations/"

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    locations = Location.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'locations': locations})

def reports_index(request):
    reports = Report.objects.all()
    return render(request, 'report_index.html', {'reports': reports})

def reports_show(request, report_id):
    report = Report.objects.get(id=report_id)
    return render(request, 'report_show.html', {'report': report})

@method_decorator(login_required, name='dispatch')
class ReportCreate(CreateView):
    model = Report
    fields = '__all__'
    template_name = "report_form.html"
    success_url = '/reports'

@method_decorator(login_required, name='dispatch')
class ReportUpdate(UpdateView):
    model = Report
    fields = '__all__'
    template_name = "report_update.html"
    success_url = '/reports'

@method_decorator(login_required, name='dispatch')
class ReportDelete(DeleteView):
    model = Report
    template_name = "report_confirm_delete.html"
    success_url = '/reports'

#login, logout, and signup  
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None: 
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled')

            else:
                print('The username and/or password is incorrect, please try again!')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/locations')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('Hey', user.username)
            return HttpResponseRedirect('/user/'+str(user))
        else:
            HttpResponse('<h1>Try Again!</h1>')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})