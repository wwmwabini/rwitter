from django.shortcuts import render, redirect
from .forms import SearchHistoryForm
from .models import SearchHistory
from django.db.models import Q

def home(request):

    #Search

    form1 = SearchHistoryForm(request.POST)

    if request.method == 'POST':
        searchterm = request.POST.get('searchterm')
        print(request.POST.get('searchterm'))

        if request.user.is_authenticated:
            querydetails = SearchHistory.objects.create(searchterm=searchterm, user_id=request.user.id)
        else:
            querydetails = SearchHistory.objects.create(searchterm=searchterm)
        
        querydetails.save()

        return redirect('tweets-home')
    
    elif request.method == 'GET':
        if request.user.is_authenticated:
            search_history = SearchHistory.objects.filter(user=request.user).order_by('-id').values_list('searchterm', flat=True)[:10]
        else:
            search_history = SearchHistory.objects.order_by('-id').values_list('searchterm', flat=True)[:5]
        

    context = {
        'form1': form1,
        'search_history': search_history
    }


    return render(request, 'tweets/feed.html', context)
