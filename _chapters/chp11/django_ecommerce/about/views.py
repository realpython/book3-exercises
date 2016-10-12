from django.shortcuts import render

# Create your views here.

def about(request):
    return render(request, "about/jinja2/about.html")


