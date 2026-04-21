from django.db import models
from django.contrib.auth.models import User


ROLE_CHOICES = [
    ('worker', 'Соискатель'),
    ('employer', 'Работодатель'),
]


CITY_CHOICES = [
    ('Алматы', 'Алматы'),
    ('Астана', 'Астана'),
    ('Шымкент', 'Шымкент'),
    ('Караганда', 'Караганда'),
    ('Актобе', 'Актобе'),
    ('Атырау', 'Атырау'),
    ('Павлодар', 'Павлодар'),
    ('Тараз', 'Тараз'),
    ('Усть-Каменогорск', 'Усть-Каменогорск'),
    ('Костанай', 'Костанай'),
    ('Кызылорда', 'Кызылорда'),
    ('Уральск', 'Уральск'),
    ('Семей', 'Семей'),
    ('Петропавловск', 'Петропавловск'),
    ('Туркестан', 'Туркестан'),
    ('Актау', 'Актау'),
]


UNIVERSITY_CHOICES = [
    ('КБТУ', 'КБТУ'),
    ('КазНУ', 'КазНУ им. аль-Фараби'),
    ('ЕНУ', 'ЕНУ им. Л.Н. Гумилева'),
    ('SDU', 'SDU University'),
    ('AITU', 'Astana IT University'),
    ('Satbayev', 'Satbayev University'),
    ('Nazarbayev', 'Nazarbayev University'),
    ('МУИТ', 'МУИТ'),
    ('Narxoz', 'Narxoz University'),
    ('KIMEP', 'KIMEP University'),
    ('АУЭС', 'Алматинский университет энергетики и связи'),
    ('КазАТУ', 'КазАТУ'),
    ('Карагандинский университет', 'Карагандинский университет'),
    ('Абылай хан', 'КазУМОиМЯ имени Абылай хана'),
    ('Абай', 'КазНПУ имени Абая'),
    ('SDU Демиреля', 'Университет Сулеймана Демиреля'),
    ('Торайгыров', 'Торайгыров университет'),
    ('СКУ', 'Северо-Казахстанский университет'),
    ('Уалиханов', 'Кокшетауский университет им. Ш. Уалиханова'),
    ('ЗКГУ', 'Западно-Казахстанский университет'),
]


PROFESSION_CHOICES = [
    ('programmer', 'Программист'),
    ('teacher', 'Учитель'),
    ('designer', 'Дизайнер'),
    ('data_analyst', 'Аналитик данных'),
    ('accountant', 'Бухгалтер'),
    ('manager', 'Менеджер'),
    ('marketer', 'Маркетолог'),
    ('hr', 'HR-специалист'),
    ('sales', 'Менеджер по продажам'),
    ('translator', 'Переводчик'),
]


PROGRAMMER_LEVELS = [
    ('junior', 'Junior'),
    ('middle', 'Middle'),
    ('senior', 'Senior')
]

TEACHER_LEVELS = [
    ('teacher', 'Педагог'),
    ('moderator', 'Педагог-модератор'),
    ('expert', 'Педагог-эксперт'),
    ('researcher', 'Педагог-исследователь'),
    ('master', 'Педагог-мастер')
]

GENERIC_LEVELS = [
    ('beginner', 'Начальный'),
    ('specialist', 'Специалист'),
    ('lead', 'Руководитель')
]


LANGUAGE_CHOICES = [
    ('Русский', 'Русский'),
    ('Английский', 'Английский'),
    ('Турецкий', 'Турецкий'),
    ('Китайский', 'Китайский'),
    ('Немецкий', 'Немецкий'),
    ('Французский', 'Французский'),
    ('Арабский', 'Арабский'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    last_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    middle_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES)
    specialty_title = models.CharField(max_length=120, help_text='Например: Python Backend Developer')
    profession_level = models.CharField(max_length=50, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    previous_workplace = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, default='Казахстан')
    city = models.CharField(max_length=50, choices=CITY_CHOICES)

    bachelor_done = models.BooleanField(default=False)
    bachelor_university = models.CharField(max_length=120, choices=UNIVERSITY_CHOICES, blank=True)
    bachelor_start_year = models.PositiveIntegerField(blank=True, null=True)
    bachelor_end_year = models.PositiveIntegerField(blank=True, null=True)

    master_done = models.BooleanField(default=False)
    master_university = models.CharField(max_length=120, choices=UNIVERSITY_CHOICES, blank=True)
    master_specialty = models.CharField(max_length=150, blank=True)

    phd_done = models.BooleanField(default=False)
    phd_university = models.CharField(max_length=120, choices=UNIVERSITY_CHOICES, blank=True)
    phd_specialty = models.CharField(max_length=150, blank=True)

    has_personal_projects = models.BooleanField(default=False)
    projects_link = models.URLField(blank=True)

    spoken_languages = models.JSONField(default=list, blank=True)

    hard_skills = models.TextField(blank=True, help_text='Навыки, инструменты, технологии')
    about_me = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join([p for p in parts if p]).strip()

    def __str__(self):
        return f"{self.full_name} - {self.get_profession_display()}"


class Favorite(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employer', 'resume')


class Notification(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']