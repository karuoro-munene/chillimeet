from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'index.html', locals())


def meetings(request):
    return render(request, 'meetings.html', locals())


def reports(request):
    return render(request, 'reports.html', locals())


def staff(request):
    return render(request, 'staff.html', locals())
