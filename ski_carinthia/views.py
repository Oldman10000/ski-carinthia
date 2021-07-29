from django.shortcuts import render


def error_404_view(request, exception):
    return render(request, 'auth/error_404.html')


def error_500_view(request):
    return render(request, 'auth/error_500.html')
