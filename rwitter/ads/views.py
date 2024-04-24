
from django.contrib.auth.decorators import login_required


@login_required
def ads(request):
    if request.method == "POST":
        pass