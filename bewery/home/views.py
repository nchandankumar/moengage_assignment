from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
# from .forms import ReviewForm
import requests

from .models import Review

from .forms import ReviewForm

def search_breweries(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        api_url_by_city = f'https://api.openbrewerydb.org/v1/breweries?by_city={data}'
        api_url_by_name = f'https://api.openbrewerydb.org/v1/breweries?by_name={data}'
        api_url_by_type = f'https://api.openbrewerydb.org/v1/breweries?by_type={data}'
        breweries = []
        if requests.get(api_url_by_city).status_code == 200:
           breweries = requests.get(api_url_by_city).json()
        elif requests.get(api_url_by_name).status_code == 200:
           breweries = requests.get(api_url_by_name).json()
        else:
           breweries = requests.get(api_url_by_type).json()
        id_list = [d['id'] for d in breweries]
        ids=','.join(id_list)
        api = f'https://api.openbrewerydb.org/v1/breweries?by_ids={ids}'
        print(api)
        res = requests.get(api)
        api_data_id = res.json()
        return render(request, 'home/search_results.html', {'breweries': api_data_id, 'city': data,  "Reviews": Review.objects.all()})


def home(request):
  api_data = []
  api_url = 'https://api.openbrewerydb.org/v1/breweries?per_page=20'
  response = requests.get(api_url)
  if response.status_code == 200:
    api_data = response.json()
    print(api_data)
  else:
    print("error")

  context = {
     "beweries": api_data
  }
  # form = ReviewForm()
  
  return render(request,"home/index.html", context)


def review_form(request,id):
   user = request.user
   
   message = ""
   if request.method == 'POST':
      cmt = request.POST.get('comment')
      rat = request.POST.get('rating')
      res=Review.objects.create(brew_id=id,comment=cmt,rating=rat,author=user)
      if res:
         message += "successfully added the reiew"
      else:
         message += "review not added"
      print(cmt,rat)
   form = ReviewForm()

   context = {
      "message": message,
       "form": form,
       "reviews": Review.objects.all(),
       "id":id
   }
   
   return render(request,"home/review.html",context)

