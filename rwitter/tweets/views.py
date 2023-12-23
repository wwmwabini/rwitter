from django.shortcuts import render, redirect
from .forms import SearchHistoryForm
from .models import SearchHistory
from users.models import UserProfile
from django.contrib.auth.models import User 
from django.db.models import Q
from django.utils import timezone


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
        

    context = {
        'form1': form1,
        'search_history': search_history
    }


    return render(request, 'tweets/feed.html', context)


def searchresults(request):
    
    return render(request, 'tweets/search.html')