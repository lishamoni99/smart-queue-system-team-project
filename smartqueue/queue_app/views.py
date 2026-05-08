from django.shortcuts import render, redirect
from .models import Queue

# -------- TOKEN GENERATE --------
def generate_token(request):
    student_id = request.session.get("student_id")
    sector = request.session.get("sector")

    if not student_id or not sector:
        return redirect("student_login")

    count = Queue.objects.filter(sector=sector).count()
    position = count + 1

    prefix = {
        "Bank": "B",
        "Library": "L",
        "Office": "O",
        "Canteen": "C"
    }

    token = prefix.get(sector, "X") + str(position)

    Queue.objects.create(
        student_id=student_id,
        sector=sector,
        token=token,
        position=position
    )

    request.session["token"] = token
    request.session["position"] = position

    return redirect("student_dashboard")


# -------- QUEUE LIST (ADMIN VIEW) --------
def queue_list(request):
    sector = request.session.get("sector")
    data = Queue.objects.filter(sector=sector).order_by("position")

    return render(request, "queue_list.html", {"queues": data})


# -------- UPDATE STATUS --------
def mark_served(request, id):
    q = Queue.objects.get(id=id)
    q.status = "served"
    q.save()
    return redirect("queue_list")


# -------- DELETE TOKEN --------
def delete_token(request, id):
    Queue.objects.get(id=id).delete()
    return redirect("queue_list")