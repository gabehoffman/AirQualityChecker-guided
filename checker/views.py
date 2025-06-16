from django.shortcuts import render
from .forms import LocationForm


def location_view(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            # For now, just show the cleaned data on the same page
            return render(request, "checker/location_form.html", {"form": form, "submitted": True, "data": form.cleaned_data})
    else:
        form = LocationForm()
    return render(request, "checker/location_form.html", {"form": form})
