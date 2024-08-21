from django.contrib.auth.models import AbstractUser
from django.db import models
from courses import models as cmodels

class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)

    def add_bonus(self, amount):
        self.amount += amount
        self.save()

    def subtract_bonus(self, amount):
        if self.amount < amount:
            raise ValueError("Недостаточно средств на балансе.")
        self.amount -= amount
        self.save()

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions', null=True)
    course = models.ForeignKey(cmodels.Course, on_delete=models.CASCADE, related_name='subscriptions', null=True)
    purchased_at = models.DateTimeField(auto_now_add=True, null=True)


    # TODO

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

class StudentGroup(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(cmodels.Group, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'group')
        verbose_name = 'Студент в группе'
        verbose_name_plural = 'Студенты в группах'

    def __str__(self):
        return f"{self.user} в группе {self.group}"
