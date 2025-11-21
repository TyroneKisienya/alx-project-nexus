import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product, Order, OrderItem
from django.db import transaction

class Command(BaseCommand):
    help = "Seeds the database with initial data for development"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        # Clear existing data (correct order for FK dependencies)
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        # -----------------------------
        # Create Admin User
        # -----------------------------
        admin, created = User.objects.get_or_create(
            username="skai",
            defaults={"email": "skai@skai.com"}
        )
        if created:
            admin.set_password("postgres")
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()

        # Regular User
        user, created = User.objects.get_or_create(
            username="test",
            defaults={"email": "test@test.com"}
        )
        if created:
            user.set_password("test12345")
            user.save()

        # -----------------------------
        # Categories
        # -----------------------------
        category_names = [
            "Electronics", "Clothing", "Home Appliances", "Toys",
            "Sports", "Health", "Groceries", "Automotive",
            "Books", "Furniture"
        ]

        categories = [Category.objects.create(name=name) for name in category_names]

        # -----------------------------
        # Product Templates
        # -----------------------------
        product_templates = [
            ("Wireless Headphones", 3500),
            ("Smartphone A21", 15000),
            ("4K Television", 55000),
            ("Men's Jacket", 2500),
            ("Kids Toy Car", 1800),
            ("Electric Kettle", 1200),
            ("Bluetooth Speaker", 2000),
            ("Office Chair", 7000),
            ("Running Shoes", 3000),
            ("Protein Powder", 2500),
        ]

        products = []
        for i in range(30):
            name, base_price = random.choice(product_templates)
            price = base_price + random.randint(-500, 1500)
            category = random.choice(categories)

            product = Product.objects.create(
                name=f"{name} {i+1}",
                description=f"Sample description for {name} {i+1}",
                price=price,
                category=category
            )
            products.append(product)

        # -----------------------------
        # Create Sample Orders
        # -----------------------------
        for i in range(3):
            order = Order.objects.create(
                user=user,
                total_amount=0
            )

            total = 0
            order_items_count = random.randint(1, 4)

            for _ in range(order_items_count):
                product = random.choice(products)
                quantity = random.randint(1, 3)

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

                total += product.price * quantity

            order.total_amount = total
            order.save()

        self.stdout.write(self.style.SUCCESS("Database successfully seeded!"))
