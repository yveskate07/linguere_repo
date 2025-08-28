from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from Users.models import Fab_User


# Create your views here.

@login_required
def user_home(request):
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    # si l'utilisateur est un superuser, rediriger vers la page d'administration
    if user.is_superuser:
        return redirect('/admin')
    return render(request ,'Users/home/index.html', {'user':user})

@login_required
def user_edit(request):

    if request.method == "POST":
        user = get_object_or_404(Fab_User, uuid=request.user.uuid)
        user.tel_num = request.POST.get("tel_num")
        user.adress = request.POST.get("adress")
        user.username = request.POST.get("username")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.set_password(request.POST.get("password"))

        user.save()

    return redirect('user_home')

@login_required
def user_orders(request):
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    return render(request, "Users/orders/index.html", {'user':user})

def user_favourites(request):
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    return render(request, "Users/favourites/index.html", {'user':user})

def user_tracked_deliveries(request):
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    return render(request, "Users/tracked_deliveries/index.html", {'user':user})