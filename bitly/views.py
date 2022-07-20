from django.shortcuts import redirect

def homepage(request):
    return redirect("https://dashboard.amalitech.me/")
