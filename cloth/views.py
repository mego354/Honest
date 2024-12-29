from django.shortcuts import render
from .models import Fabric,CutTransfer,ReturnTransfer,Statistics, Updates

def fabric_view(request):
    return render(request, "cloth/balance.html", {
        'models': Fabric.objects.all().order_by('-date'),
        'update': Updates.objects.all().order_by('-date').first()
    })

def cut_transfer_view(request):
    return render(request, "cloth/cut.html", {
        'models': CutTransfer.objects.all().order_by('-date'),
        'update': Updates.objects.all().order_by('-date').first()
    })

def return_transfer_view(request):
    return render(request, "cloth/return.html", {
        'models': ReturnTransfer.objects.all().order_by('-date'),
        'update': Updates.objects.all().order_by('-date').first()
    })

def statistics_view(request):
    return render(request, "cloth/statistics.html", {
        'models': Statistics.objects.all().order_by('-date'),
        'update': Updates.objects.all().order_by('-date').first()
    })
