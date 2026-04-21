from django import forms
from django.contrib.auth.models import User
from .models import (
    Profile, Resume, ROLE_CHOICES, UNIVERSITY_CHOICES, PROFESSION_CHOICES,
    LANGUAGE_CHOICES, CITY_CHOICES
)

PROGRAMMER_LANGS = ['Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'PHP', 'Kotlin', 'Swift']
GENERAL_SKILLS_HINT = 'Напишите навыки через запятую: Python, Django, SQL...'

class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=150)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    phone = forms.CharField(label='Номер телефона', max_length=30, required=False)
    role = forms.ChoiceField(label='Кто вы?', choices=ROLE_CHOICES)
    company_name = forms.CharField(label='Название компании', max_length=200, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже существует.')
        return username

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('role') == 'employer' and not cleaned.get('company_name'):
            self.add_error('company_name', 'Для работодателя укажите компанию.')
        return cleaned

class ResumeForm(forms.ModelForm):
    spoken_languages = forms.MultipleChoiceField(
        label='Какие языки вы знаете?',
        choices=LANGUAGE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Resume
        fields = [
            'photo', 'last_name', 'first_name', 'middle_name', 'email', 'phone', 'address',
            'profession', 'specialty_title', 'profession_level', 'experience_years', 'previous_workplace',
            'city', 'bachelor_done', 'bachelor_university', 'bachelor_start_year', 'bachelor_end_year',
            'master_done', 'master_university', 'master_specialty',
            'phd_done', 'phd_university', 'phd_specialty',
            'has_personal_projects', 'projects_link', 'spoken_languages', 'hard_skills', 'about_me'
        ]
        widgets = {
            'about_me': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Расскажите о себе...'}),
            'hard_skills': forms.Textarea(attrs={'rows': 3, 'placeholder': GENERAL_SKILLS_HINT}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес проживания'}),
            'specialty_title': forms.TextInput(attrs={'placeholder': 'Например: Python Backend Developer'}),
            'previous_workplace': forms.TextInput(attrs={'placeholder': 'Где вы работали?'}),
            'projects_link': forms.URLInput(attrs={'placeholder': 'Оставьте ссылку'}),
        }
        labels = {
            'photo': 'Фото',
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'email': 'Почта',
            'phone': 'Телефон',
            'address': 'Адрес проживания',
            'profession': 'Специальность',
            'specialty_title': 'Название специальности',
            'profession_level': 'Уровень',
            'experience_years': 'Опыт работы (лет)',
            'previous_workplace': 'Где работали',
            'city': 'Город',
            'bachelor_done': 'Есть бакалавр?',
            'bachelor_university': 'Выберите вуз',
            'bachelor_start_year': 'Год начала',
            'bachelor_end_year': 'Год окончания',
            'master_done': 'Есть магистратура?',
            'master_university': 'Вуз магистратуры',
            'master_specialty': 'Специальность магистратуры',
            'phd_done': 'Есть докторантура?',
            'phd_university': 'Вуз докторантуры',
            'phd_specialty': 'Специальность докторантуры',
            'has_personal_projects': 'Есть личные проекты?',
            'projects_link': 'Ссылка на проект',
            'hard_skills': 'Навыки / технологии',
            'about_me': 'О себе',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_year = 2026
        year_choices = [(y, y) for y in range(1990, current_year + 1)]
        self.fields['bachelor_start_year'] = forms.TypedChoiceField(choices=[('', '---------')] + year_choices, coerce=int, required=False, label='Год начала')
        self.fields['bachelor_end_year'] = forms.TypedChoiceField(choices=[('', '---------')] + year_choices, coerce=int, required=False, label='Год окончания')
        self.fields['city'].choices = CITY_CHOICES
        self.fields['bachelor_university'].choices = UNIVERSITY_CHOICES
        self.fields['master_university'].choices = UNIVERSITY_CHOICES
        self.fields['phd_university'].choices = UNIVERSITY_CHOICES
        self.fields['profession'].choices = PROFESSION_CHOICES

        for name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple, forms.FileInput)):
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = (css + ' input').strip()

    def clean(self):
        cleaned = super().clean()
        exp = cleaned.get('experience_years') or 0
        if exp > 0 and not cleaned.get('previous_workplace'):
            self.add_error('previous_workplace', 'Укажите, где вы работали.')
        if cleaned.get('bachelor_done'):
            if not cleaned.get('bachelor_university'):
                self.add_error('bachelor_university', 'Выберите вуз.')
        if cleaned.get('master_done'):
            if not cleaned.get('master_university'):
                self.add_error('master_university', 'Выберите вуз магистратуры.')
        if cleaned.get('phd_done'):
            if not cleaned.get('phd_university'):
                self.add_error('phd_university', 'Выберите вуз докторантуры.')
        if cleaned.get('has_personal_projects') and not cleaned.get('projects_link'):
            self.add_error('projects_link', 'Оставьте ссылку на проект.')
        return cleaned

class SearchForm(forms.Form):
    profession = forms.ChoiceField(label='Специальность', choices=[('', 'Все')] + PROFESSION_CHOICES, required=False)
    city = forms.ChoiceField(label='Город', choices=[('', 'Все')] + CITY_CHOICES, required=False)
    level = forms.CharField(label='Уровень', max_length=50, required=False)
    min_experience = forms.IntegerField(label='Опыт от', required=False, min_value=0)
    bachelor_done = forms.NullBooleanField(label='Бакалавр', required=False)
    language = forms.ChoiceField(label='Язык', choices=[('', 'Любой')] + LANGUAGE_CHOICES, required=False)
