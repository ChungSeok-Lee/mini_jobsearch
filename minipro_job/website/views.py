from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'website/home.html', {})

def makewordcloud(request):
    return render(request, 'webstie/wordcloud_page.html', {})