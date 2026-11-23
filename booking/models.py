from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models


class ProviderProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_profile"
    )
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ServiceOffering(models.Model):

    title= models.CharField(max_length=120)
    description = models.TextField(blank=True)

    duration_minutes = models.PositiveIntegerField()

    price = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.PROTECT,
        related_name="services",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class AvailabilitySlot(models.Model):
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="slots"
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["start_at"]

    # AvailabilitySlot.objects.create() | obj.save()
    def clean(self):
        super().clean()

        if (
            self.start_at is not None
            and self.end_at is not None
            and self.end_at <= self.start_at
        ):
            raise ValidationError({
                "end_at": "End time must be after start time."
            })

    def __str__(self):
        return f"{self.provider_id}: {self.start_at}"