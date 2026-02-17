from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('DRINK', 'Drink'),
        ('SMOOTHIE', 'Smoothie'),
        ('SNACK', 'Snack'),
        ('STARTER', 'Indian Starter'),
        ('COMBO', 'Combo'),
    ]
    SEASON_CHOICES = [
        ('ALL', 'All Year'),
        ('SUMMER', 'Summer Coolers'),
        ('MONSOON', 'Monsoon Snacks'),
        ('WINTER', 'Winter Warmers'),
    ]
    TEMP_TYPE_CHOICES = [
        ('HOT', 'Hot'),
        ('COLD', 'Cold'),
        ('NA', 'N/A'),
    ]

    MENU_SECTION_CHOICES = [
        ('SHAWARMA_ROLL', 'Chicken Shawarma Roll'),
        ('SHAWARMA_PLATE', 'Chicken Shawarma Plate'),
        ('GRILLED_CHICKEN', 'Grilled Chicken'),
        ('BBQ_CHICKEN', 'Barbeque Chicken'),
        ('TANDOORI_CHICKEN', 'Tandoori Chicken'),
        ('VEG_STARTERS', 'Veg Starters'),
        ('LOADED_FRIES', 'Loaded Fries'),
        ('FUSION_CHAAT', 'Fusion Chaat'),
        ('FAMILY_BOX', 'Family Box'),
        ('PARTY_PACK', 'Party Pack'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu/')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='DRINK')
    menu_section = models.CharField(max_length=20, choices=MENU_SECTION_CHOICES, default='OTHER')
    season = models.CharField(max_length=10, choices=SEASON_CHOICES, default='ALL')
    temp_type = models.CharField(max_length=5, choices=TEMP_TYPE_CHOICES, default='COLD')
    is_special = models.BooleanField(default=False)
    is_seasonal = models.BooleanField(default=False)
    
    # Innovative Features
    spice_level = models.IntegerField(default=0) # 0 to 3
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_season_display()})"

class FranchisePackage(models.Model):
    LOCATION_CHOICES = [
        ('MALL', 'Mall'),
        ('COLLEGE', 'College'),
        ('BEACH', 'Beach'),
        ('HIGHWAY', 'Highway'),
    ]
    
    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    investment_range = models.CharField(max_length=50)
    description = models.TextField()
    setup_time = models.CharField(max_length=50, default="4-6 weeks")
    image = models.ImageField(upload_to='franchise/')

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at the time of order

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('CASH', 'Cash'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='SUCCESS')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.transaction_id}"
