from django.contrib.auth.models import AbstractUser
from django.db import models


DESIGNATION_TYPES = (
        (1, "OCR"),
        (2, "Manager")
    )

class User(AbstractUser):
    phone      = models.IntegerField(blank=True, null=True)
    nid        = models.IntegerField(blank=True, null=True)
    address    = models.CharField(max_length=511, blank=True, null=True)

    designation = models.IntegerField(default=1, choices=DESIGNATION_TYPES)

    @property
    def get_designation(self):
        """
        this method will return full designation string
        :return STR:
        """
        return dict(DESIGNATION_TYPES).get(self.designation)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username