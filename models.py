from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название факультета')
    description = models.TextField(blank=True, verbose_name='Описание факультета')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название группы')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name='Факультет')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    email = models.EmailField(blank=True, verbose_name='Email')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'