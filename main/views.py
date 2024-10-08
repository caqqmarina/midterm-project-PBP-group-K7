from django.shortcuts import render

# def show_main(request):
#     context = {
#         'group' : 'K7',
#         'class': 'PBP KKI'
#     }

#     return render(request, "main.html", context)

def homepage(request):
    return render(request, 'homepage.html')



