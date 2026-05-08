from django.shortcuts import render, redirect

def select_sector(request):
    if request.method == "POST":
        sector = request.POST.get("sector")
        request.session["sector"] = sector
        return redirect("generate_token")

    return render(request, "sector/sector_select.html")