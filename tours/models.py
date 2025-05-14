from django.db import models
from django.conf import settings

class Tour(models.Model):
    tour_operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='my_tours'
    )
    title = models.CharField(max_length=50)
    description = models.TextField()
    photo = models.ImageField(upload_to='tours/', null=True, blank=True)
    tour_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('registration','Регистрация'),('closed','Закрыт')],
        default='registration'
    )
    max_participants = models.PositiveIntegerField(
        default=10,
        help_text='Максимальное количество участников'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def booking_count(self):
        return self.bookings.count()
    
    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    status = models.CharField(
        max_length=20,
        choices=[('pending','Ожидает'),('approved','Подтверждено'),('declined','Отклонено')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} — {self.tour.title}"