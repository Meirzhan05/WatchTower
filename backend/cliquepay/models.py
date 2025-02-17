from django.db import models
from django.core.validators import RegexValidator

class User(models.Model):
    id = models.CharField(max_length=128, primary_key=True, unique=True)
    cognito_id = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(
        max_length=150, 
        help_text="User's full name (required)",
        default="Unnamed User"
    )
    name = models.CharField(max_length=100)  # username
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=16, 
        blank=True, 
        null=True,
        help_text="Optional phone number in international format"
    )
    avatar_url = models.URLField(null=True, blank=True)
    currency = models.CharField(max_length=10, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
class Friendship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('blocked', 'Blocked'),
    ]
    
    id = models.CharField(max_length=128, primary_key=True, unique=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_friendships')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_friendships')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    action_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_actions')

    class Meta:
        db_table = 'friendships'
        constraints = [
            models.UniqueConstraint(
                fields=['user1', 'user2'],
                name='unique_friendship'
            ),
            models.CheckConstraint(
                check=models.Q(user1__lt=models.F('user2')),
                name='force_user_order'
            )
        ]

class Group(models.Model):
    id = models.CharField(max_length=128, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_groups'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'groups'

    def __str__(self):
        creator = self.created_by.full_name if self.created_by else "Deleted User"
        return f"{self.name} (Created by: {creator})"

class GroupMember(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group_memberships'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'group_members'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'group'],
                name='unique_group_membership'
            )
        ]

    def __str__(self):
        return f"{self.user.full_name} in {self.group.name}"