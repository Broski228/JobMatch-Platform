from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, ResumeForm, SearchForm
from .models import Favorite, Notification, Profile, Resume

def home(request):
    return render(request, 'home.html')

def register_options(request):
    return render(request, 'register_options.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        Profile.objects.create(
            user=user,
            role=form.cleaned_data['role'],
            phone=form.cleaned_data.get('phone', ''),
            company_name=form.cleaned_data.get('company_name', ''),
        )
        login(request, user)
        messages.success(request, 'Регистрация успешно завершена.')
        return redirect('dashboard')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        error = 'Неверный логин или пароль.'
    return render(request, 'login.html', {'error': error})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    role = request.user.profile.role
    if role == 'worker':
        return render(request, 'dashboard_worker.html', {'resumes': request.user.resumes.all()})
    return render(request, 'dashboard_employer.html')

@login_required
def profile_page(request):
    return render(request, 'profile.html')

@login_required
def security_page(request):
    return render(request, 'security.html')

@login_required
def resume_create(request):
    if request.user.profile.role != 'worker':
        messages.error(request, 'Только работник может создавать резюме.')
        return redirect('dashboard')
    form = ResumeForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        resume = form.save(commit=False)
        resume.user = request.user
        resume.country = 'Қазақстан'
        resume.save()
        messages.success(request, 'Резюме успешно сохранено.')
        return redirect('resume_detail', pk=resume.pk)
    return render(request, 'resume_form.html', {'form': form, 'title': 'Создать резюме'})

@login_required
def resume_edit(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    form = ResumeForm(request.POST or None, request.FILES or None, instance=resume)
    if request.method == 'POST' and form.is_valid():
        resume = form.save(commit=False)
        resume.country = 'Қазақстан'
        resume.save()
        messages.success(request, 'Резюме обновлено.')
        return redirect('resume_detail', pk=resume.pk)
    return render(request, 'resume_form.html', {'form': form, 'title': 'Редактировать резюме'})

@login_required
def my_resumes(request):
    if request.user.profile.role != 'worker':
        return redirect('dashboard')
    return render(request, 'my_resumes.html', {'resumes': request.user.resumes.all()})

@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    is_favorite = False
    if request.user.is_authenticated and request.user.profile.role == 'employer':
        is_favorite = Favorite.objects.filter(employer=request.user, resume=resume).exists()
    return render(request, 'resume_detail.html', {'resume': resume, 'is_favorite': is_favorite})

@login_required
def search_specialists(request):
    if request.user.profile.role != 'employer':
        return redirect('dashboard')
    form = SearchForm(request.GET or None)
    resumes = Resume.objects.all().select_related('user')
    if form.is_valid():
        profession = form.cleaned_data.get('profession')
        city = form.cleaned_data.get('city')
        level = form.cleaned_data.get('level')
        min_experience = form.cleaned_data.get('min_experience')
        bachelor_done = form.cleaned_data.get('bachelor_done')
        language = form.cleaned_data.get('language')

        if profession:
            resumes = resumes.filter(profession=profession)
        if city:
            resumes = resumes.filter(city=city)
        if level:
            resumes = resumes.filter(profession_level__icontains=level)
        if min_experience is not None:
            resumes = resumes.filter(experience_years__gte=min_experience)
        if bachelor_done is not None:
            resumes = resumes.filter(bachelor_done=bachelor_done)
        if language:
            resumes = [r for r in resumes if language in (r.spoken_languages or [])]

    favorite_ids = set(Favorite.objects.filter(employer=request.user).values_list('resume_id', flat=True))
    return render(request, 'search.html', {'form': form, 'resumes': resumes, 'favorite_ids': favorite_ids})

@login_required
def toggle_favorite(request, resume_id):
    if request.user.profile.role != 'employer':
        return redirect('dashboard')
    resume = get_object_or_404(Resume, pk=resume_id)
    fav = Favorite.objects.filter(employer=request.user, resume=resume).first()
    if fav:
        fav.delete()
        messages.info(request, 'Удалено из избранного.')
    else:
        Favorite.objects.create(employer=request.user, resume=resume)
        company = request.user.profile.company_name or request.user.username
        Notification.objects.create(worker=resume.user, message=f'Ваша резюме понравилось: {company}')
        messages.success(request, 'Добавлено в избранное.')
    next_url = request.META.get('HTTP_REFERER') or 'favorites'
    return redirect(next_url)

@login_required
def favorites_page(request):
    if request.user.profile.role != 'employer':
        return redirect('dashboard')
    favorites = Favorite.objects.filter(employer=request.user).select_related('resume')
    return render(request, 'favorites.html', {'favorites': favorites})

@login_required
def notifications_page(request):
    notifications = request.user.notifications.all()
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})
