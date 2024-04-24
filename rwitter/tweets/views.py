from typing import Optional
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import SearchHistoryForm, FeedbackForm, StoryForm, CommentForm
from .models import SearchHistory, Post, Feedback, Story, Comment
from ads.models import Ads

from rwitter.functions import handle_uploaded_file
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver    


def do_search(searchterm):
    # search users, usersprofile table: columns username, bio
    # search posts: column content, 
    results = User.objects.filter(username__icontains=searchterm).all()

    for result in results:
        print(result)

    return results


def get_contacts():
    @receiver(user_logged_in)
    def got_online(sender, user, request, **kwargs):    
        user.userprofile.is_online = True
        user.userprofile.save()

    @receiver(user_logged_out)
    def got_offline(sender, user, request, **kwargs):   
        user.userprofile.is_online = False
        user.userprofile.save()

    from django.db.models import F

    contacts = User.objects.annotate( is_online=F('userprofile__is_online')).order_by('-is_online')[:5]

    return contacts


@login_required
def home(request):

    #Comments
    
    comment_form = CommentForm(request.POST)

    if request.method == 'POST' and 'post_comment_form' in request.POST:
        post_id = request.POST.get('post_id')
        if comment_form.is_valid() and request.POST.get('content') != "":
            log_comment = Comment.objects.create(content=request.POST.get('content'), post_id=post_id, user_id=request.user.id)
            log_comment.save()

            return HttpResponseRedirect(request.path_info)
        else:
            messages.warning(request, "Please type your message first before submitting the comment.")
            return HttpResponseRedirect(request.path_info)
        

    #Search

    search_history = ""

    form1 = SearchHistoryForm(request.POST)

    if request.method == 'POST' and 'searchterm' in request.POST:
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
            
    
    elif request.method == 'GET':
        if request.user.is_authenticated:
            search_history = SearchHistory.objects.filter(user=request.user).order_by('-created_at').values_list('searchterm', flat=True)[:10]
        else:
            search_history = SearchHistory.objects.order_by('-created_at').values_list('searchterm', flat=True)[:5]
        


    # Posts
    posts = Post.objects.all().order_by('-updated_at')

    # Stories
    stories = Story.objects.order_by('-created_at')[:10]

    # Ads
    ads = Ads.objects.order_by('-created_at')[:2]


    context = {
        'form1': form1,
        'posts': posts,
        'stories':stories,
        'ads': ads,
        'comment_form': comment_form,
        'search_history': search_history,
        'contacts': get_contacts()
    }


    return render(request, 'tweets/feed.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template="tweets/feed.html"
    fields = ['content', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user

        media_location = 'post_media'

        post_file = handle_uploaded_file(form.cleaned_data.get('image'), media_location, 'post')
        form.instance.image = post_file

        return super().form_valid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user

        media_location = 'post_media'

        post_file = handle_uploaded_file(form.cleaned_data.get('image'), media_location, 'post')
        form.instance.image = post_file

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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def feedback(request):
    media_location = 'feedback_media'
    form = FeedbackForm()

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_subject = request.POST.get('subject')
            feedback_content = request.POST.get('content')
            feedback_media = request.FILES['media']

            media_file_name = handle_uploaded_file(feedback_media, media_location, 'feedback')

            log_feedback = Feedback.objects.create(subject=feedback_subject, content=feedback_content, user_id=request.user.id, media=media_file_name)
            log_feedback.save()

            messages.info(request, 'Thank you for your feedback. We will look into it.')
            return redirect('tweets-feedback')
        else:
            messages.warning(request, 'Sorry, there was an error uploading your file. Please try again later.')
            return redirect('tweets-feedback')

    context = {
        'form': form,
        'contacts': get_contacts()
    }

    return render(request, 'tweets/feedback.html', context=context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def story(request):
    media_location = 'stories_media'

    story_form = StoryForm()

    if request.method == "POST":
        story_form = StoryForm(request.POST)

        if story_form.is_valid():

            story_media = request.FILES['story']

            story_file = handle_uploaded_file(story_media, media_location, 'story')

            log_story = Story.objects.create(story=story_file, user_id=request.user.id)
            log_story.save()
            

            messages.info(request, 'Great, your story has been updated...')
            return redirect('tweets-home')
        
            
        else:
            messages.warning(request, 'Oops. There was an error updating your story, please retry...')
            return redirect('tweets-story')

    
    context = {
                'story_form': story_form,
                'contacts': get_contacts()
            }

    print(context)

    return render(request, 'tweets/story.html', context=context)
