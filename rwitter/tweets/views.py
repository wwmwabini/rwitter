from typing import Optional
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SearchHistoryForm, FeedbackForm
from .models import SearchHistory, Post, Feedback

from users.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView


def do_search(searchterm):
    # search users, usersprofile table: columns username, bio
    # search posts: column content, 
    results = User.objects.filter(username__icontains=searchterm).all()

    for result in results:
        print(result)

    return results


def home(request):

    #Search

    form1 = SearchHistoryForm(request.POST)

    if request.method == 'POST':
        searchterm = request.POST.get('searchterm')
        clearall = request.POST.get('clearall')

        if clearall and request.user.is_authenticated:
            clear = SearchHistory.objects.filter(user_id=request.user.id).all()
            clear.delete()

        print(request.POST.get('searchterm'))

        if searchterm and request.user.is_authenticated:
            previoussearch = SearchHistory.objects.filter(searchterm=searchterm, user_id=request.user.id).first()

            if not previoussearch:
                logsearch_history = SearchHistory.objects.create(searchterm=searchterm, user_id=request.user.id)
                logsearch_history.save()
            else:
                previoussearch.created_at = timezone.now()
                previoussearch.save()

            
            results = do_search(searchterm)

            searchcontext = {
                'searchterm': searchterm,
                'results': results
            }

            return render(request, 'tweets/search.html', searchcontext)
        
        elif searchterm:
           
           querydetails = SearchHistory.objects.create(searchterm=searchterm)
           querydetails.save()

           results = do_search(searchterm)
           searchcontext = {
                'searchterm': searchterm,
                'results': results
            }

           return render(request, 'tweets/search.html', searchcontext)


        else:
            #if searchterm is None, do nothing
            return redirect('tweets-home')
            

        return redirect('tweets-home')
    
    elif request.method == 'GET':
        if request.user.is_authenticated:
            search_history = SearchHistory.objects.filter(user=request.user).order_by('-created_at').values_list('searchterm', flat=True)[:10]
        else:
            search_history = SearchHistory.objects.order_by('-created_at').values_list('searchterm', flat=True)[:5]
        


    # Posts

    posts = Post.objects.all().order_by('-created_at')



    context = {
        'form1': form1,
        'posts': posts,
        'search_history': search_history
    }


    return render(request, 'tweets/feed.html', context)



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template="tweets/feed.html"
    fields = ['content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False



def searchresults(request):
    
    return render(request, 'tweets/search.html')

def feedback(request):
    form = FeedbackForm()

    if request.method == "POST":
        feedback_subject = request.POST.get('subject')
        feedback_content = request.POST.get('content')
        feedback_media = ""

        log_feedback = Feedback.objects.create(subject=feedback_subject, content=feedback_content, user_id=request.user.id)
        log_feedback.save()

        messages.warning(request, 'Thank you for your feedback. We will look into it.')
        return redirect('tweets-feedback')

    context = {
        'form': form
    }

    return render(request, 'tweets/feedback.html', context=context)