from decimal import Decimal
from enum import Enum
from django.db import models
from django.conf import settings

from userAuth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(default="football-bg.jpg")
    captain = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='team_captain', null=True, blank=True)
    team_location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('captain', 'Captain'),
        ('player', 'Player'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_players')  # ForeignKey to Team
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='player_images/')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')
    player_location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class FutsalKit(models.Model):
    SIZE_CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
        ('XXXL', 'Triple Extra Large'),
        ('4XL', 'Four Extra Large'),
        ('5XL', 'Five Extra Large'),
    )

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='kits/', default="logo/futsal-pro.png")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class OrderStatus(Enum):
    PENDING = 'PENDING'
    VERIFIED = 'VERIFIED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    REJECTED = 'REJECTED'

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    kit = models.ForeignKey(FutsalKit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=10, choices=[(tag.value, tag.value) for tag in OrderStatus], default=OrderStatus.PENDING.value)
    payment_status = models.CharField(max_length=10, default="Pending", null=False)
    pidx = models.CharField(max_length=20, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.kit.price
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.kit)