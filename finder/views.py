'''***************************************************************************************
*  REFERENCES
*  Title: django-filter 2.4.0
*  Author: Alex Gaynor
*  Date: Not Provided
*  Code version: 2.4.0
*  URL: https://pypi.org/project/django-filter/
*  Software License: BSD

*  Title: newsapi-python
*  Author: Matt Lisivick
*  Date: 10/3/19
*  Code version: 2.0
*  URL: https://github.com/mattlisiv/newsapi-python
*  Software License: MIT

*  Title: Python Django Tutorial: Full-Featured Web App Part 9 - Update User Profile
*  Author: Corey Schafer
*  Date: 2/18/19
*  URL_1: https://www.youtube.com/watch?v=CQ90L5jfldw&t
*  URL_2: https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog
*  Software License: MIT

*  Title: Python Django Tutorial: Full-Featured Web App Part 8 - User Profile and Picture
*  Author: Corey Schafer
*  Date: 2/18/19
*  URL_1: https://www.youtube.com/watch?v=FdVuKt_iuSI&t
*  URL_2: https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog
*  Software License: MIT

* Title: Django-allauth Tutorial
* Author: Will Vincent
* Date: 11/10/20
* URL: https://learndjango.com/tutorials/django-allauth-tutorial
* Software License: MIT

*  Title: Django Friends tutorial // How to create a Facebook-like system.
*  Author: JustDjango
*  Date: 4/22/18
*  URL_1: https://www.youtube.com/watch?v=QS9z4g0JAOY
*  URL_2: https://github.com/justdjango/friends
*  Software License: BSD
***************************************************************************************'''


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account, Profile, FriendRequest, GroupRequest
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.template import loader
from django.contrib.auth.decorators import login_required
from finder.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.views.generic import FormView, UpdateView
from django.urls import reverse
from .filters import DropdownFilter
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
import requests

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



@login_required
def search(request):
    #current_user = Profile.objects.all()
    users = Profile.objects.all()
    friendreq = FriendRequest.objects.all()
    freqsto=[]
    for friendob in friendreq:
        if request.user == friendob.from_user:
            freqsto.append((friendob.to_user).id)
    groupreq = GroupRequest.objects.all()
    greqsto=[]
    for groupob in groupreq:
        if request.user == groupob.from_user:
            greqsto.append((groupob.to_user.id))
    valid = Profile.objects.get(user=request.user).group != ""
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
    return HttpResponse(template.render({'filter': profile_filter,'freqsto': freqsto, 'greqsto':greqsto, 'valid':valid}, request))


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

@login_required
def create_group(request):
    group_name = request.POST.get('group_name')
    group_zoom_link = request.POST.get('group_zoom_link')
    profile1 = Profile.objects.get(user=request.user)

    if len(list(Profile.objects.filter(group=group_name))) == 0:
        profile1.group = group_name
        profile1.group_zoom_link = group_zoom_link
        profile1.group_leader = True
        profile1.group_valid = True
        profile1.save()

        groupreq = GroupRequest.objects.all()
        for groupob in groupreq:
            if request.user == groupob.from_user:
                groupob.delete()
    else:
        if group_name != "":
            profile1.group_valid = False
            profile1.save()
    group_invite = ''
    group = Profile.objects.get(user=request.user).group
    groupreq = GroupRequest.objects.all()
    greqs = []
    pendingReq = False
    for groupob in groupreq:
        if request.user == groupob.to_user:
            greqs.append(groupob.from_user)
            group_invite = Profile.objects.get(user=groupob.from_user).group
            pendingReq = True
    for i in range(len(greqs)):
        greqs[i] = Profile.objects.get(id=(greqs[i]).id)
    template = loader.get_template('finder/groups.html')
    context = {'group_invite': group_invite, 'greqs': greqs, 'pendingReq': pendingReq, 'group': group,'valid': profile1.group_valid}
    return HttpResponse(template.render(context, request))


@login_required
def invite_to_group(request, id):
    from_user=request.user
    to_user=(Profile.objects.get(id=id)).user
    GroupRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    return redirect('/finder/search')

@login_required
def cancel_group_invite(request,id):
    from_user=request.user
    to_user=(Profile.objects.get(id=id)).user
    grequest=GroupRequest.objects.get(from_user=from_user,to_user=to_user)
    grequest.delete()
    return redirect('/finder/search')

@login_required
def groups(request):
    group_invite = ''
    group = Profile.objects.get(user=request.user).group
    groupreq = GroupRequest.objects.all()
    greqs= []
    pendingReq = False
    for groupob in groupreq:
        if request.user == groupob.to_user:
            greqs.append(groupob.from_user)
            group_invite = Profile.objects.get(user=groupob.from_user).group
            pendingReq = True
    for i in range(len(greqs)):
        greqs[i]=Profile.objects.get(id=(greqs[i]).id)
    template = loader.get_template('finder/groups.html')
    context = {'group_invite': group_invite, 'greqs': greqs, 'pendingReq': pendingReq, 'group':group,
               'valid' : Profile.objects.get(user=request.user).group_valid}
    return HttpResponse(template.render(context, request))

@login_required
def accept_GroupRequest(request,id):
    user1=request.user
    profile1=Profile.objects.get(user=user1)
    profile2=Profile.objects.get(id=id)
    user2=profile2.user
    grequest=GroupRequest.objects.get(from_user=user2,to_user=user1)
    profile1.group = profile2.group
    profile1.save()
    grequest.delete()
    return redirect('/finder/groups')

@login_required
def delete_GroupRequest(request,id):
    user1=request.user
    profile1=Profile.objects.get(user=user1)
    profile2=Profile.objects.get(id=id)
    user2=profile2.user
    grequest=GroupRequest.objects.get(from_user=user2,to_user=user1)
    grequest.delete()
    return redirect('/finder/groups')

@login_required
def leave_group(request):
    user1=request.user
    profile1=Profile.objects.get(user=user1)
    if profile1.group_leader is True:
        group_name = profile1.group
        for profile in list(Profile.objects.filter(group=group_name)):
            profile.group = ""
            profile.save()
    profile1.group = ""
    profile1.group_leader = False
    profile1.save()

    groupreq = GroupRequest.objects.all()
    for groupob in groupreq:
        if request.user == groupob.from_user:
            groupob.delete()

    return redirect('/finder/groups')

@login_required
def view_group(request, group_name):
    members = []
    for profile in list(Profile.objects.filter(group=group_name)):
        members.append(profile)
    template = loader.get_template('finder/group_view.html')
    context = {'group_name': group_name, 'members': members}
    return HttpResponse(template.render(context, request))

@login_required
def top_stories_home(request):
    response = requests.get('https://api.nytimes.com/svc/topstories/v2/health.json?api-key=4IOHvPz5HqGNR8t6q8cG2hmkxYiNFAIv')
    data = response.json()
    articles = data['results']
    titles = {}
    for article in articles[:10]:
        titles[article['title']] = article['url']
    context = {'titles' : titles}
    template = loader.get_template('finder/top_stories.html')
    return HttpResponse(template.render(context, request))


def top_stories_index(request):
    response = requests.get('https://api.nytimes.com/svc/topstories/v2/health.json?api-key=4IOHvPz5HqGNR8t6q8cG2hmkxYiNFAIv')
    data = response.json()
    articles = data['results']
    titles1 = {}
    titles1[articles[0]['title']] = articles[0]['url']
    titles2 = {}
    titles2[articles[1]['title']] = articles[1]['url']
    titles3 = {}
    titles3[articles[2]['title']] = articles[2]['url']
    titles4 = {}
    titles4[articles[3]['title']] = articles[3]['url']
    context = {'titles1' : titles1, 'titles2' : titles2, 'titles3' : titles3, 'titles4' : titles4}
    
    template = loader.get_template('finder/index.html')
    return HttpResponse(template.render(context, request))
