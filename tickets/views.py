from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, Comment


@login_required
def ticket_list(request):
    """Client faqat o'z tiketlarini, admin hammasini ko'radi"""
    if request.user.role == 'admin':
        tickets = Ticket.objects.all().order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')

    # Filterlar
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    date = request.GET.get('date')

    if status:
        tickets = tickets.filter(status=status)
    if priority:
        tickets = tickets.filter(priority=priority)
    if date:
        tickets = tickets.filter(created_at__date=date)

    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


@login_required
def ticket_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'normal')
        image = request.FILES.get('image')

        if title and description:
            ticket = Ticket.objects.create(
                title=title,
                description=description,
                priority=priority,
                image=image,
                created_by=request.user,
                status='new',
            )
            messages.success(request, "Tiket muvaffaqiyatli yaratildi!")
            return redirect('ticket_list')

    return render(request, 'tickets/ticket_create.html')


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Client faqat o'z tiketini ko'ra oladi
    if request.user.role != 'admin' and ticket.created_by != request.user:
        messages.error(request, "Bu tiketga ruxsatingiz yo'q!")
        return redirect('dashboard')

    comments = ticket.comments.all().order_by('created_at')

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
    })


@login_required
def ticket_update_status(request, ticket_id):
    if request.user.role != 'admin':
        messages.error(request, "Faqat admin statusni o'zgartira oladi!")
        return redirect('dashboard')

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['new', 'in_progress', 'closed']:
            ticket.status = new_status
            ticket.save()
            messages.success(request, "Status yangilandi!")

    return redirect('ticket_detail', ticket_id=ticket.id)


@login_required
def comment_create(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Client faqat o'z tiketiga izoh yozadi
    if request.user.role != 'admin' and ticket.created_by != request.user:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('dashboard')

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Comment.objects.create(
                ticket=ticket,
                user=request.user,
                message=message,
            )
            messages.success(request, "Izoh qo'shildi!")

    return redirect('ticket_detail', ticket_id=ticket.id)


@login_required
def admin_ticket_list(request):
    """Faqat admin uchun — barcha tiketlar + user qidirish"""
    if request.user.role != 'admin':
        messages.error(request, "Bu sahifa faqat admin uchun!")
        return redirect('dashboard')

    tickets = Ticket.objects.all().order_by('-created_at')

    username = request.GET.get('username')
    if username:
        tickets = tickets.filter(created_by__username__icontains=username)

    return render(request, 'tickets/admin_ticket_list.html', {
        'tickets': tickets,
        'username': username,
    })