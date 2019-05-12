from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from base.models import UserProfile
# Create your views here.

def user_unicode_patch(self):
    return '%s %s' % (self.first_name, self.last_name)

def about_view(request):
    #staff = User.objects.all().filter(is_staff=True).order_by('username')
    staff = UserProfile.objects.all().filter(user__is_staff = True)
    return render(request, 'about/about.html',{'staff': staff})