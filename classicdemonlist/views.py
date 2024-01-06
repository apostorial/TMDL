from django.shortcuts import render
from classicdemonlist.models.classiclevel import ClassicLevel

# Create your views here.

def index(request):
    classic_levels = ClassicLevel.objects.filter(ranking__lte=75)
    return render(request, 'index.html', {'classic_levels': classic_levels})

def classic_extendedlist(request):
    classic_extended_levels = ClassicLevel.objects.filter(ranking__range=(76, 150))
    return render(request, 'classic_extendedlist.html', {'classic_extended_levels': classic_extended_levels})

# def level_legacylist(request):
#     legacy_levels = ClassicLevel.objects.filter(ranking__gt=150)
#     return render(request, 'level_legacylist.html', {'legacy_levels': legacy_levels})

def level_detail(request, level_id):
    level = ClassicLevel.objects.get(pk=level_id)
    return render(request, 'level_detail.html', {'level': level})