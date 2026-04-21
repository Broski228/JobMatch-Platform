from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('worker', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='notifications',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(
                    choices=[
                        ('Соискатель', 'Соискатель'),
                        ('Работодатель', 'Работодатель')
                    ],
                    max_length=20
                )),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('company_name', models.CharField(blank=True, max_length=200)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='profile',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('last_name', models.CharField(max_length=120)),
                ('first_name', models.CharField(max_length=120)),
                ('middle_name', models.CharField(blank=True, max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=255)),
                ('profession', models.CharField(
                    choices=[
                        ('Программист', 'Программист'),
                        ('Учитель', 'Учитель'),
                        ('Дизайнер', 'Дизайнер'),
                        ('Аналитик данных', 'Аналитик данных'),
                        ('Бухгалтер', 'Бухгалтер'),
                        ('Менеджер', 'Менеджер'),
                        ('Маркетолог', 'Маркетолог'),
                        ('HR-специалист', 'HR-специалист'),
                        ('Менеджер по продажам', 'Менеджер по продажам'),
                        ('Переводчик', 'Переводчик'),
                    ],
                    max_length=50
                )),
                ('specialty_title', models.CharField(
                    help_text='Например: Python Backend Developer',
                    max_length=120
                )),
                ('profession_level', models.CharField(blank=True, max_length=50)),
                ('experience_years', models.PositiveIntegerField(default=0)),
                ('previous_workplace', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(default='Казахстан', max_length=100)),
                ('city', models.CharField(
                    choices=[
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
                    ],
                    max_length=50
                )),
                ('bachelor_done', models.BooleanField(default=False)),
                ('bachelor_university', models.CharField(
                    blank=True,
                    choices=[
                        ('КБТУ', 'КБТУ'),
                        ('КазНУ им. аль-Фараби', 'КазНУ им. аль-Фараби'),
                        ('ЕНУ им. Л.Н. Гумилева', 'ЕНУ им. Л.Н. Гумилева'),
                        ('SDU University', 'SDU University'),
                        ('Astana IT University', 'Astana IT University'),
                        ('Satbayev University', 'Satbayev University'),
                        ('Nazarbayev University', 'Nazarbayev University'),
                        ('МУИТ', 'МУИТ'),
                        ('Narxoz University', 'Narxoz University'),
                        ('KIMEP University', 'KIMEP University'),
                        ('Алматинский университет энергетики и связи', 'Алматинский университет энергетики и связи'),
                        ('КазАТУ', 'КазАТУ'),
                        ('Карагандинский университет', 'Карагандинский университет'),
                        ('КазУМОиМЯ имени Абылай хана', 'КазУМОиМЯ имени Абылай хана'),
                        ('КазНПУ имени Абая', 'КазНПУ имени Абая'),
                        ('Университет Сулеймана Демиреля', 'Университет Сулеймана Демиреля'),
                        ('Торайгыров университет', 'Торайгыров университет'),
                        ('Северо-Казахстанский университет', 'Северо-Казахстанский университет'),
                        ('Кокшетауский университет им. Ш. Уалиханова', 'Кокшетауский университет им. Ш. Уалиханова'),
                        ('Западно-Казахстанский университет', 'Западно-Казахстанский университет'),
                    ],
                    max_length=120
                )),
                ('bachelor_start_year', models.PositiveIntegerField(blank=True, null=True)),
                ('bachelor_end_year', models.PositiveIntegerField(blank=True, null=True)),
                ('master_done', models.BooleanField(default=False)),
                ('master_university', models.CharField(
                    blank=True,
                    choices=[
                        ('КБТУ', 'КБТУ'),
                        ('КазНУ им. аль-Фараби', 'КазНУ им. аль-Фараби'),
                        ('ЕНУ им. Л.Н. Гумилева', 'ЕНУ им. Л.Н. Гумилева'),
                        ('SDU University', 'SDU University'),
                        ('Astana IT University', 'Astana IT University'),
                        ('Satbayev University', 'Satbayev University'),
                        ('Nazarbayev University', 'Nazarbayev University'),
                        ('МУИТ', 'МУИТ'),
                        ('Narxoz University', 'Narxoz University'),
                        ('KIMEP University', 'KIMEP University'),
                        ('Алматинский университет энергетики и связи', 'Алматинский университет энергетики и связи'),
                        ('КазАТУ', 'КазАТУ'),
                        ('Карагандинский университет', 'Карагандинский университет'),
                        ('КазУМОиМЯ имени Абылай хана', 'КазУМОиМЯ имени Абылай хана'),
                        ('КазНПУ имени Абая', 'КазНПУ имени Абая'),
                        ('Университет Сулеймана Демиреля', 'Университет Сулеймана Демиреля'),
                        ('Торайгыров университет', 'Торайгыров университет'),
                        ('Северо-Казахстанский университет', 'Северо-Казахстанский университет'),
                        ('Кокшетауский университет им. Ш. Уалиханова', 'Кокшетауский университет им. Ш. Уалиханова'),
                        ('Западно-Казахстанский университет', 'Западно-Казахстанский университет'),
                    ],
                    max_length=120
                )),
                ('master_specialty', models.CharField(blank=True, max_length=150)),
                ('phd_done', models.BooleanField(default=False)),
                ('phd_university', models.CharField(
                    blank=True,
                    choices=[
                        ('КБТУ', 'КБТУ'),
                        ('КазНУ им. аль-Фараби', 'КазНУ им. аль-Фараби'),
                        ('ЕНУ им. Л.Н. Гумилева', 'ЕНУ им. Л.Н. Гумилева'),
                        ('SDU University', 'SDU University'),
                        ('Astana IT University', 'Astana IT University'),
                        ('Satbayev University', 'Satbayev University'),
                        ('Nazarbayev University', 'Nazarbayev University'),
                        ('МУИТ', 'МУИТ'),
                        ('Narxoz University', 'Narxoz University'),
                        ('KIMEP University', 'KIMEP University'),
                        ('Алматинский университет энергетики и связи', 'Алматинский университет энергетики и связи'),
                        ('КазАТУ', 'КазАТУ'),
                        ('Карагандинский университет', 'Карагандинский университет'),
                        ('КазУМОиМЯ имени Абылай хана', 'КазУМОиМЯ имени Абылай хана'),
                        ('КазНПУ имени Абая', 'КазНПУ имени Абая'),
                        ('Университет Сулеймана Демиреля', 'Университет Сулеймана Демиреля'),
                        ('Торайгыров университет', 'Торайгыров университет'),
                        ('Северо-Казахстанский университет', 'Северо-Казахстанский университет'),
                        ('Кокшетауский университет им. Ш. Уалиханова', 'Кокшетауский университет им. Ш. Уалиханова'),
                        ('Западно-Казахстанский университет', 'Западно-Казахстанский университет'),
                    ],
                    max_length=120
                )),
                ('phd_specialty', models.CharField(blank=True, max_length=150)),
                ('has_personal_projects', models.BooleanField(default=False)),
                ('projects_link', models.URLField(blank=True)),
                ('spoken_languages', models.JSONField(blank=True, default=list)),
                ('hard_skills', models.TextField(blank=True, help_text='Навыки, инструменты, технологии')),
                ('about_me', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='resumes',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employer', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='favorites',
                    to=settings.AUTH_USER_MODEL
                )),
                ('resume', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='liked_by',
                    to='core.resume'
                )),
            ],
            options={'unique_together': {('employer', 'resume')}},
        ),
    ]