from django.shortcuts import render


def handwrite_view(request):
    return render(request, "handwrite.html")
