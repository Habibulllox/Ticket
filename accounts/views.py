from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tickets.models import Ticket


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {
                'error': "Username yoki parol noto'g'ri!"
            })

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        from .forms import RegisterForm
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'client'
            user.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            return redirect('dashboard')
    else:
        from .forms import RegisterForm
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.user.role == 'admin':
        context = {
            'new_count': Ticket.objects.filter(status='new').count(),
            'in_progress_count': Ticket.objects.filter(status='in_progress').count(),
            'closed_count': Ticket.objects.filter(status='closed').count(),
            'total_count': Ticket.objects.count(),
        }
        return render(request, 'accounts/admin_dashboard.html', context)
    else:
        tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
        return render(request, 'accounts/dashboard.html', {'tickets': tickets})