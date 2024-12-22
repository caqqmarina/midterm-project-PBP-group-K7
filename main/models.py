from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# faculty model
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=10)
    colors = models.CharField(max_length=200)  
    image = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_css_class(self):
        colors = self.colors.split(',')
        if len(colors) == 1:
            return f"mb-4 rounded-full bg-{colors[0]}-500 py-0.5 px-2.5 border border-transparent text-xs text-white transition-all shadow-sm w-20 text-center"
        elif len(colors) == 2:
            return f"mb-4 rounded-full py-0.5 px-2.5 border border-transparent text-xs text-white transition-all shadow-sm w-20 text-center bg-gradient-to-r from-{colors[0]}-600 to-{colors[1]}-600"
        elif len(colors) == 3:
            return f"mb-4 rounded-full py-0.5 px-2.5 border border-transparent text-xs text-white transition-all shadow-sm w-20 text-center bg-gradient-to-r from-{colors[0]}-600 via-{colors[1]}-500 to-{colors[2]}-500"
        else:
            return "mb-4 rounded-full py-0.5 px-2.5 border border-transparent text-xs text-white transition-all shadow-sm w-20 text-center"

# canteen model
class Canteen(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='canteens')
    image = models.CharField(max_length=100)
    price = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name} ({self.faculty.name})"

# stall model
class Stall(models.Model):
    CUISINE_CHOICES = [
        ('indonesian', 'Indonesian'),
        ('chinese', 'Chinese'),
        ('western', 'Western'),
        ('japanese', 'Japanese'),
        ('korean', 'Korean'),
        ('indian', 'Indian'),
        ('beverages', 'Beverages'),
        ('dessert', 'Dessert'),
        ('others', 'Others'),
    ]

    name = models.CharField(max_length=100)
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE, related_name='stalls')
    cuisine = models.CharField(max_length=50, choices=CUISINE_CHOICES, default='others')

    def __str__(self):
        return f"{self.name} (Canteen: {self.canteen.name})"

# product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stall = models.ForeignKey(Stall, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
        # return f"{self.name} - {self.price} (Stall: {self.stall.name})"

# product review model
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'user']

class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ['user', 'product']