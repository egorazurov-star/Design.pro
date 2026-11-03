from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

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
    """Личный кабинет пользователя."""
    return render(request, 'studio/cabinet.html')


@admin_required
def admin_panel(request):
    """Панель управления сайтом (личный кабинет администратора)."""
    return render(request, 'studio/admin_panel.html')
