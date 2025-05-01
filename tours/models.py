from django.db import models
from django.conf import settings

class Tour(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    photo = models.ImageField(upload_to='images/tours/', default=None, null=True, blank=True)
    tour_operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tour_date = models.DateField(null=False, blank=False)
    price = models.DecimalField(max_digits=8,
                               decimal_places=2)
    status = models.CharField("Status",
                              choices=[("registration", "Registration"), ("closed", "Closed")],
                              default="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title