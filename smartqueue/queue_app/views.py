from django.shortcuts import render, redirect

# ---------------- SETTINGS ----------------
TIME_PER_PERSON = 3

# ---------------- SECTOR PREFIX ----------------
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
    if request.session.get('user_type') != 'student':
        return redirect('student_login')

    if request.method == "POST":
        sector = request.POST.get('sector')

        request.session['sector'] = sector

        # queue number (temporary simple logic)
        queue_number = request.session.get('queue_number', 1)

        prefix = get_prefix(sector)
        token = generate_token(prefix, queue_number)

        request.session['token'] = token
        request.session['position'] = queue_number

        return redirect('student_dashboard')

    return render(request, 'sector_select.html')


# ---------------- STUDENT DASHBOARD ----------------
def student_dashboard(request):
    if request.session.get('user_type') != 'student':
        return redirect('student_login')

    position = request.session.get('position', 1)

    return render(request, 'student_dashboard.html', {
        'student_id': request.session.get('student_id'),
        'sector': request.session.get('sector'),
        'token': request.session.get('token'),
        'position': position,
        'estimated_time': estimate_time(position)
    })


# ---------------- GUARDIAN LOGIN ----------------
def guardian_login(request):
    if request.method == "POST":
        phone = request.POST.get('phone')

        if phone:
            request.session['user_type'] = 'guardian'
            request.session['phone'] = phone
            return redirect('guardian_dashboard')

    return render(request, 'guardian_login.html')


# ---------------- GUARDIAN DASHBOARD ----------------
def guardian_dashboard(request):
    if request.session.get('user_type') != 'guardian':
        return redirect('guardian_login')

    position = request.session.get('position', 1)

    return render(request, 'guardian_dashboard.html', {
        'phone': request.session.get('phone'),
        'sector': request.session.get('sector'),
        'token': request.session.get('token'),
        'position': position,
        'estimated_time': estimate_time(position)
    })


# ---------------- LOGOUT ----------------
def logout_view(request):
    request.session.flush()
    return redirect('student_login')