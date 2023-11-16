from django.db import models


# Create your models here.
class PublishStateOptions(models.TextChoices):
    # This class defines the choices could be used in state field
    # It shows like this: CONSTANT = 'DB_VALUE', 'USER_DISPLAY_VALUE'
    PUBLISH = "PU", "Publish"
    DRAFT = "DR", "Draft"
