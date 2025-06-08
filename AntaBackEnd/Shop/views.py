from django.shortcuts import render

# Create your views here.
def arduino(request):
    return render(request, 'Shop/arduino/index.html')

def installations(request):
    return render(request, "Shop/installations/index.html")

def machine(request):
    return render(request, "Shop/machine/index.html")