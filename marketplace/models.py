from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    name = models.CharField(max_length=55, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128, null=False)  # Store hashed passwords
    phone = models.CharField(max_length=15, null=False)
    college_id = models.CharField(max_length=50, unique=True, null=False)
    department = models.CharField(max_length=50, blank=True, null=True)  # Optional field
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def save(self, *args, **kwargs):
        """ Hash password before saving """
        if not self.password.startswith('pbkdf2_'):  # Prevent double hashing
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """ Verify hashed password """
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name




class Product(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("pending", "Pending"),
        ("removed", "Removed"),
    ]

    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)  # Seller
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    year = models.CharField(max_length=20)  # Example: "1st Year", "2nd Year"
    department = models.CharField(max_length=50)  # Example: "Computer Science"
    product_type = models.CharField(max_length=50)  # Example: "Notes"

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.year} - {self.department}"