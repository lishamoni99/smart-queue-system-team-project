from django.shortcuts import render, redirect
from .models import Queue
from history.models import QueueHistory
from notifications.models import Notification

# ---------------- SETTINGS ----------------
TIME_PER_PERSON = 3

# ---------------- HELPER FUNCTIONS ----------------

def get_estimated_time(sector):

    count = QueueHistory.objects.filter(sector=sector).count()

    return count * TIME_PER_PERSON


def get_prefix(sector):

    if sector == "Bank":
        return "B"
    elif sector == "Library":
        return "L"
    elif sector == "UAP Office":
        return "O"
    elif sector == "Canteen":
        return "C"
    return "X"


# ---------------- TOKEN ----------------
def generate_token(prefix, number):
    return f"{prefix}{number}"


# ---------------- TIME ----------------
def estimate_time(position):
    return position * TIME_PER_PERSON


# ---------------- HOME REDIRECT ----------------
def home(request):
    return render(request, 'home.html')


# ---------------- STUDENT LOGIN ----------------
def student_login(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        if student_id and password:
            request.session['user_type'] = 'student'
            request.session['student_id'] = student_id
            return redirect('sector_select')

    return render(request, 'student_login.html')


# ---------------- SECTOR SELECT ----------------
def sector_select(request):
    if request.session.get('user_type') not in ['student', 'guardian']:
        return redirect('student_login')

    if request.method == "POST":
        sector = request.POST.get('sector')
        print("SECTOR:", sector)
        request.session['sector'] = sector

        # FIX: auto increment token logic
        queue_number = request.session.get('queue_number')
        if queue_number is None:
            queue_number = 1
        else:
            queue_number = int(queue_number) + 1

        request.session['queue_number'] = queue_number

        prefix = get_prefix(sector)
        token = generate_token(prefix, queue_number)

        request.session['token'] = token
        request.session['position'] = queue_number

        # --- NOTIFICATION TRIGGER: Token Generation ---
        Notification.objects.create(
            student_id=request.session.get('student_id'),
            message=f"Your token {token} has been generated for {sector}. Your current position is {queue_number}."
        )

        if request.session.get('user_type') == 'guardian':
            return redirect('guardian_dashboard')

        return redirect('student_dashboard')

    return render(request, template_name='sector_select.html')

# ---------------- STUDENT DASHBOARD ----------------
def student_dashboard(request):
    if request.session.get('user_type') != 'student':
        return redirect('student_login')

    position = request.session.get('position', 1)
    student_id = request.session.get('student_id')
    waiting_time = estimate_time(position)


    QueueHistory.objects.create(
        user_type="student",
        student_id=student_id,
        phone_number=None,
        token_number=request.session.get('token'),
        sector=request.session.get('sector'),
        waiting_time=waiting_time
    )

    # --- NOTIFICATION PART (Add this) ---
    # 1. Feature: Time Alert (Jodi waiting time 5 min ba tar kom hoy)
    if waiting_time <= 5:
        # Age check koro oi student-ke ei alert-ta deya hoyeche kina
        already_alerted = Notification.objects.filter(
            student_id=student_id,
            message__contains="coming in 5 minutes"
        ).exists()

        if not already_alerted:
            Notification.objects.create(
                student_id=student_id,
                message=f"Please be ready! Your turn is coming in {waiting_time} minutes."
            )

    return render(request, template_name='student_dashboard.html', context={
        'student_id': student_id,
        'sector': request.session.get('sector'),
        'token': request.session.get('token'),
        'position': position,
        'estimated_time': waiting_time
    })

# ---------------- GUARDIAN LOGIN ----------------
def guardian_login(request):
    if request.method == "POST":
        phone = request.POST.get('phone')

        if phone:
            request.session['user_type'] = 'guardian'
            request.session['phone'] = phone
            return redirect('sector_select')

    return render(request, 'guardian_login.html')


# ---------------- GUARDIAN DASHBOARD ----------------
def guardian_dashboard(request):
    if request.session.get('user_type') != 'guardian':
        return redirect('guardian_login')

    position = request.session.get('position')

    if position is None:
        position = 1
    # HISTORY SAVE (GUARDIAN)
    QueueHistory.objects.create(
        user_type="guardian",


        phone_number=request.session.get('phone'),

        token_number=request.session.get('token'),

        sector=request.session.get('sector'),

        waiting_time=estimate_time(position)

    )
    return render(request, 'guardian_dashboard.html', {
        'phone': request.session.get('phone'),
        'sector': request.session.get('sector'),
        'token': request.session.get('token'),
        'position': position,
        'estimated_time': estimate_time(position)
    })



# ---------------- CANCEL TOKEN ----------------
def cancel_token(request):

    token = request.session.get('token')

    if token:

        QueueHistory.objects.filter(
            token_number=token
        ).delete()

    # decrease queue number
    queue_number = request.session.get('queue_number', 1)

    if queue_number > 1:
        request.session['queue_number'] = queue_number - 1

    request.session['token'] = None
    request.session['sector'] = None
    request.session['position'] = None

    return redirect('sector_select')


# ---------------- LOGOUT ----------------
def logout_view(request):
    request.session.flush()
    return redirect('student_login')