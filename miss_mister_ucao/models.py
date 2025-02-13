from django.db import models

class Miss(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="miss_photos/")  # Stocker les photos
    description = models.TextField()

    def __str__(self):
        return self.name

class Vote(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)  # Un vote par IP
    miss = models.ForeignKey(Miss, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote pour {self.miss.name} de {self.ip_address}"
