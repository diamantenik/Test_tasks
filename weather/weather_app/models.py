from django.db import models

class CitySearch(models.Model):
    city = models.CharField(max_length=100)
    session_key = models.CharField(max_length=40)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} ({self.session_key})"
