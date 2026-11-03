from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DesignRequestForm
from .models import DesignRequest


def admin_required(view_func):
    """Доступ только для авторизованного администратора (иначе вход или ошибка 403)."""
    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped


def home(request):
    """Главная страница: 4 последние выполненные заявки и счётчик заявок «в работе»."""
    done_requests = (
        DesignRequest.objects
        .filter(status=DesignRequest.STATUS_DONE)
        .select_related('category')[:4]
    )
    in_progress_count = DesignRequest.objects.filter(
        status=DesignRequest.STATUS_IN_PROGRESS
    ).count()
    return render(request, 'studio/home.html', {
        'done_requests': done_requests,
        'in_progress_count': in_progress_count,
    })


@login_required
def cabinet(request):
    """Личный кабинет: свои заявки (новые - сверху) с фильтром по статусу."""
    design_requests = (
        DesignRequest.objects
        .filter(user=request.user)
        .select_related('category')
    )
    status = request.GET.get('status', '')
    if status in dict(DesignRequest.STATUS_CHOICES):
        design_requests = design_requests.filter(status=status)
    else:
        status = ''
    return render(request, 'studio/cabinet.html', {
        'design_requests': design_requests,
        'status': status,
        'statuses': DesignRequest.STATUS_CHOICES,
    })


@login_required
def request_create(request):
    """Создание заявки. Статус «Новая» задаётся автоматически."""
    form = DesignRequestForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        design_request = form.save(commit=False)
        design_request.user = request.user
        design_request.save()
        messages.success(request, 'Заявка успешно создана.')
        return redirect('cabinet')
    return render(request, 'studio/request_form.html', {'form': form})


@login_required
def request_delete(request, pk):
    """Удаление своей заявки (только в статусе «Новая») с подтверждением."""
    design_request = get_object_or_404(DesignRequest, pk=pk, user=request.user)
    if design_request.status != DesignRequest.STATUS_NEW:
        messages.error(
            request,
            'Нельзя удалить заявку, статус которой изменён администратором.',
        )
        return redirect('cabinet')

    if request.method == 'POST':
        design_request.delete()
        messages.success(request, 'Заявка удалена.')
        return redirect('cabinet')
    return render(request, 'studio/request_confirm_delete.html', {
        'design_request': design_request,
    })


@admin_required
def admin_panel(request):
    """Панель управления сайтом (личный кабинет администратора)."""
    return render(request, 'studio/admin_panel.html')
