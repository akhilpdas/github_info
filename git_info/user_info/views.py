from django.shortcuts import render
from django.views.generic.base import View
from user_info.forms import *
from django import http
from django.urls import reverse
import requests
from requests.auth import HTTPBasicAuth

import json
from .models import UserInfo, GithubCredentials
from django.views.generic import ListView
from .common_functions import github_get_operation

# Create your views here.

class SearchView(View):
    """Getting details of person in github."""

    template_name = 'user_info/search.html'
    form_class = GithubUerForm

    def get(self, request):
        """Get."""
        cred = GithubCredentials.objects.all()
        print(len(cred))
        if not bool(cred):
            return http.HttpResponseRedirect(reverse('CredentialsView'))

        form = self.form_class
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Posting the search form."""
        form = self.form_class(request.POST)
        print("form", request.POST.get('username'))
        if form.is_valid():
            cred = GithubCredentials.objects.all()
            print(cred)
            if not bool(cred):
                return http.HttpResponseRedirect(reverse('CredentialsView'))
            username = str(request.POST.get('username'))
            followers = []
            followings = []
            repos = []
            auth = GithubCredentials.objects.all()[0].authtoken
            
            """Followers"""
            followers_url = 'users/' + username + '/followers'
            response = github_get_operation(followers_url, auth)
            print(response)
            if 'message' in response:
                if response['message'] == "Not Found":
                    context = {
                    'form': form,
                    'status': '1'
                    }
                    return render(request, self.template_name, context)


            for follower in response:

                print("followers", follower['login'])
                followers.append(follower['login'])
            
            """Foloowing"""
            following_url = 'users/' + username + '/following'
            response = github_get_operation(following_url, auth)
            for following in response:
                followings.append(following['login'])
            
            """Repositories"""
            repos_url = 'users/' + username + '/repos?type=all'
            response = github_get_operation(repos_url, auth)
            for repo in response:
                print("following", repo['name'])
                repos.append(repo['name'])

            """Write or update into db"""
            UserInfo.objects.update_or_create(username=username,
                                              defaults={'followers': followers,
                                                        'following': followings,
                                                        'respositories': repos
                                                        })
            
            context = {
                'username': str(request.POST.get('username'))
            }
            return http.HttpResponseRedirect(reverse('ResultView')+ "?u_name=" + context['username'])

        else:
            context = {
                'form': form
            }
            return render(request, self.template_name, context)


class ResultView(ListView):
    """Showing result."""

    template_name = 'user_info/result.html'
    context_object_name = 'info_list'

    def get_queryset(self):
        cred = GithubCredentials.objects.all()
        print(cred)
        if not bool(cred):
            print("yes")
            return http.HttpResponseRedirect(reverse('CredentialsView'))
        print(self.request.GET.get('u_name'))
        u_name = str(self.request.GET.get('u_name'))
        queryset = UserInfo.objects.get(username=u_name)
        return queryset


class CredentialsView(ListView):
    """Showing result."""

    template_name = 'user_info/credentials.html'
    form_class = CredentialForm

    # context_object_name = 'info_list'

    def get(self, request):
        """Get."""
        form = self.form_class
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Posting the credentials form."""
        form = self.form_class(request.POST)
        authtoken = str(request.POST.get('authtoken'))
        # r = requests.get('https://api.github.com/user', auth=('akhilpdas', 'mypulsar180$'))
        # print(r.text)
        url = 'user/followers'
        auth = HTTPBasicAuth('', authtoken)
        url = 'https://api.github.com/' + url
        response = requests.get(url, auth=auth)
        response = response.json()
        print(response)
        if 'message' in response:
            print(response['message'])
            if response['message'] == "Bad credentials" or response['message'] == "Requires authentication":
                context = {
                    'form': form,
                    'status': '1'
                }
                return render(request, self.template_name, context)
                context = {
                    'form': form,
                    'status': '2'
                }
            return render(request, self.template_name, context)

        GithubCredentials.objects.all().delete()

        GithubCredentials.objects.create(authtoken=authtoken)
        return http.HttpResponseRedirect(reverse('SearchView'))

        
        
