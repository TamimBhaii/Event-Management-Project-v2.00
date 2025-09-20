from django.db import models
from django.conf import settings
from django.urls import reverse

def event_image_path(instance, filename):
    return f"events/{instance.organizer.username}/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=300, blank=True)

    # Cloudinary তে image save হবে (upload_to শুধু path define করবে)
    image = models.ImageField(
        upload_to=event_image_path,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="RSVP",
        related_name="rsvped_events",
        blank=True
    )

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"pk": self.pk})

    def can_be_deleted_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return user.is_superuser or (self.organizer == user)


class RSVP(models.Model):
    ATTENDING = "attending"
    INTERESTED = "interested"
    STATUS_CHOICES = [
        (ATTENDING, "Attending"),
        (INTERESTED, "Interested"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=INTERESTED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.event} ({self.status})"
