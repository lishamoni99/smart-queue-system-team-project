from django.shortcuts import render, redirect
from .models import Queue, Student
from history.models import QueueHistory
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
    return redirect('student_login')


# ---------------- STUDENT LOGIN ----------------
def student_login(request):
    error = None
    
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        if student_id and password:
            # Try to authenticate the student
            try:
                student = Student.objects.get(student_id=student_id, password=password)
                request.session['user_type'] = 'student'
                request.session['student_id'] = student_id
                return redirect('sector_select')
            except Student.DoesNotExist:
                # Check if student exists but wrong password
                if Student.objects.filter(student_id=student_id).exists():
                    error = "Invalid password. Please try again."
                else:
                    # Auto-create student if they don't exist (first-time login)
                    Student.objects.create(
                        student_id=student_id,
                        password=password,
                        name=f"Student {student_id}"
                    )
                    request.session['user_type'] = 'student'
                    request.session['student_id'] = student_id
                    return redirect('sector_select')
        else:
            error = "Please enter both student ID and password."

    return render(request, 'student_login.html', {'error': error})


# ---------------- SECTOR SELECT ----------------
from django.shortcuts import render, redirect
from notifications.models import Notification  # Notification pathanor jonno
from emergency_app.models import EmergencyRequest  # Emergency record rakhar jonno


def sector_select(request):
    # Check koro user login kora kina
    if request.session.get('user_type') not in ['student', 'guardian']:
        return redirect('student_login')

    if request.method == "POST":
        sector = request.POST.get('sector')
        is_emergency = request.POST.get('emergency') == 'on'
        student_id = request.session.get('student_id')

        request.session['sector'] = sector

        # --- Standard Queue Logic ---
        queue_number = request.session.get('queue_number')
        if queue_number is None:
            queue_number = 1
        else:
            queue_number = int(queue_number) + 1

        request.session['queue_number'] = queue_number

        prefix = get_prefix(sector)
        token = generate_token(prefix, queue_number)

        request.session['token'] = token

        # --- EMERGENCY LOGIC ADDED HERE ---
        if is_emergency:

            EmergencyRequest.objects.create(
                student_id=student_id,
                reason=f"Standard Emergency for {sector}"
            )

            request.session['position'] = 1
            msg = f"EMERGENCY: Your token {token} has been prioritized for {sector}."
        else:
            request.session['position'] = queue_number
            msg = f"Success! Your token {token} has been generated for {sector}."

        # --- NOTIFICATION TRIGGER ---

        Notification.objects.create(
            student_id=student_id,
            message=msg
        )

        if request.session.get('user_type') == 'guardian':
            return redirect('guardian_dashboard')

        return redirect('student_dashboard')

    return render(request, 'sector_select.html')

# ---------------- STUDENT DASHBOARD ----------------
def student_dashboard(request):
    if request.session.get('user_type') != 'student':
        return redirect('student_login')

    student_id = request.session.get('student_id')
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        # Handle case where student was deleted
        Student.objects.create(
            student_id=student_id,
            password="default",
            name=f"Student {student_id}"
        )
        student = Student.objects.get(student_id=student_id)

    position = request.session.get('position', 1)
    waiting_time = estimate_time(position)


    if waiting_time <= 5:
        already_notified = Notification.objects.filter(
            student_id=student_id,
            message__contains="coming in 5 minutes"
        ).exists()

        if not already_notified:
            Notification.objects.create(
                student_id=student_id,
                message=f"Please be ready! Your turn is coming in {waiting_time} minutes."
            )


    history = QueueHistory.objects.filter(
        student_id=student_id
    ).order_by('-id')[:5]

    QueueHistory.objects.create(
        user_type="student",
        student_id=student_id,
        phone_number=None,
        token_number=request.session.get('token'),
        sector=request.session.get('sector'),
        waiting_time=waiting_time
    )

    return render(request, 'student_dashboard.html', {
        'student_id': student_id,
        'sector': request.session.get('sector'),
        'token': request.session.get('token'),
        'position': position,
        'estimated_time': waiting_time,
        'history': history,
        'student': student,
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

    # ---------------- HISTORY SAVE ----------------

    QueueHistory.objects.create(

        user_type="guardian",

        phone_number=request.session.get('phone'),

        token_number=request.session.get('token'),

        sector=request.session.get('sector'),

        waiting_time=estimate_time(position)

    )

    # ---------------- HISTORY FETCH ----------------

    history = QueueHistory.objects.filter(

        phone_number=request.session.get('phone')

    ).order_by('-id')[:5]

    # ---------------- RENDER ----------------

    return render(request, 'guardian_dashboard.html', {

        'phone': request.session.get('phone'),

        'sector': request.session.get('sector'),

        'token': request.session.get('token'),

        'position': position,

        'estimated_time': estimate_time(position),

        'history': history

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