from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account, Profile, FriendRequest
from django.contrib import messages
from django.template import loader
from django.contrib.auth.decorators import login_required
from finder.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.views.generic import FormView, UpdateView
from django.urls import reverse
from .filters import DropdownFilter

# Create your views here.

def index(request):
    #if request.method == 'POST':
    #    form = UserCreationForm(request.POST)
    #    if form.is_valid():
    #        form.save()
    #        username = Account.objects.order_by('username')
    #else:
    #    form = UserCreationForm()
    #return render(request, 'finder/index.html', {'form':form})
    users = Account.objects.order_by('username')
    template = loader.get_template('finder/index.html')
    context = {'users': users}
    return HttpResponse(template.render(context, request))


def search(request):
    #current_user = Profile.objects.all()
    users = Profile.objects.all()
    friendreq = FriendRequest.objects.all()
    freqsto=[]
    for friendob in friendreq:
        if request.user == friendob.from_user:
            freqsto.append((friendob.to_user).id)
    #checks = request.POST.getlist('checks')
    profile_filter = DropdownFilter(request.GET, queryset=users)
    template = loader.get_template('finder/search.html')
    '''major = False
    yog = False
    specific_major = ""
    specific_yog = ""
    for check in checks:
        if(check == "1"):
            major = True
            specific_major = request.Post.get('specific_major')
        elif(check == "2"):
            yog = True
            specific_yog = request.POST.get("specific_yog")
    new_users = []
    if(major == True and yog == True):
        for user in users:
            if(user.major == specific_major and user.graduation == specific_yog):
                new_users.append(user)
        context = {'users': new_users}
        return HttpResponse(template.render(context, request))
    elif(major == True):
        for user in users:
            if(user.major == specific_major):
                new_users.append(user)
        context = {'users': new_users}
        return HttpResponse(template.render(context, request))
    elif(yog == True):
        for user in users:
            if(user.graduation == specific_yog):
                new_users.append(user)
        context = {'users': new_users}
        return HttpResponse(template.render(context, request))
    '''
    #context = {'users': users}
    return HttpResponse(template.render({'filter': profile_filter,'freqsto': freqsto}, request))


def login(request):
    return HttpResponse("You are at the login screen")

def user_detail(request, username):
    return HttpResponse("You're looking at the account with username:  %s." % username)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('../profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'finder/edit_profile.html', context)

@login_required
def send_FriendRequest(request,id):
    from_user=request.user
    to_user=(Profile.objects.get(id=id)).user
    frequest=FriendRequest.objects.get_or_create(from_user=from_user,to_user=to_user)
    return redirect('/finder/search')

@login_required
def cancel_FriendRequest(request,id):
    from_user=request.user
    to_user=(Profile.objects.get(id=id)).user
    frequest=FriendRequest.objects.get(from_user=from_user,to_user=to_user)
    frequest.delete()
    return redirect('/finder/search')

@login_required
def accept_FriendRequest(request,id):
    user1=request.user
    profile1=Profile.objects.get(user=user1)
    profile2=Profile.objects.get(id=id)
    user2=profile2.user
    frequest=FriendRequest.objects.get(from_user=user2,to_user=user1)
    profile1.friends.add(profile2)
    profile2.friends.add(profile1)
    frequest.delete()
    return redirect('/finder/friendlist')

@login_required
def delete_FriendRequest(request,id):
    user1=request.user
    profile1=Profile.objects.get(user=user1)
    profile2=Profile.objects.get(id=id)
    user2=profile2.user
    frequest=FriendRequest.objects.get(from_user=user2,to_user=user1)
    frequest.delete()
    return redirect('/finder/friendlist')

@login_required
def remove_Friend(request,id):
    user1=request.user
    profile1=Profile.objects.get(user=user1)
    profile2=Profile.objects.get(id=id)
    user2=profile2.user
    profile1.friends.remove(profile2)
    profile2.friends.remove(profile1)
    return redirect('/finder/friendlist')

@login_required
def friendlist_home(request):
    friends = Profile.objects.get(user=request.user).friends.all()
    friendreq = FriendRequest.objects.all()
    freqs= []
    pendingReq = False
    for friendob in friendreq:
        if request.user == friendob.to_user:
            freqs.append(friendob.from_user)
            pendingReq = True
    for i in range(len(freqs)):
        freqs[i]=Profile.objects.get(id=(freqs[i]).id)
    template = loader.get_template('finder/FriendList.html')
    context = {'friends': friends, 'freqs': freqs, 'pendingReq': pendingReq}
    return HttpResponse(template.render(context, request))