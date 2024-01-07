from django.shortcuts import render
from classicdemonlist.models.classiclevel import ClassicLevel

# Create your views here.

def index(request):
    classic_levels = ClassicLevel.objects.filter(ranking__lte=75)
    return render(request, 'index.html', {'classic_levels': classic_levels})

def classic_extendedlist(request):
    classic_extended_levels = ClassicLevel.objects.filter(ranking__range=(76, 150))
    return render(request, 'classic_extendedlist.html', {'classic_extended_levels': classic_extended_levels})

def classic_legacylist(request):
    classic_legacy_levels = ClassicLevel.objects.filter(ranking__gt=150)
    return render(request, 'classic_legacylist.html', {'classic_legacy_levels': classic_legacy_levels})