from django.db import models

# faculty model
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=10)
    name_css_class = models.CharField(max_length=200)
    image = models.CharField(max_length=100)

    def __str__(self):
        return self.name

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
        ('others', 'Others'),
        ('indian', 'Indian'),
        ('beverages', 'Beverages')
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


