from PIL import Image, ImageFilter
import os
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError


class Brand(models.Model):
    """Brands of the products: Red dragon, ,Intel, Logitech etc."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Categories of the products: Mouse, Keyboard etc."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def positive_validator(value):
    if value < 0:
        raise ValidationError(f'O número {value} não é positivo.')


class Product(models.Model):
    """Product informations"""
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    short_description = models.TextField(max_length=255)
    detailed_description = models.TextField()
    image = models.ImageField(
        upload_to='product_images/%Y/%m/', blank=True, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[positive_validator])
    discount_price = models.DecimalField(
        default=0.0, max_digits=10, decimal_places=2,
        validators=[positive_validator])

    class Meta:
        ordering = ["category"]

    @staticmethod
    def update_image(image, new_height=600, new_width=800):
        # updating image size and quality
        img_path = os.path.join(settings.MEDIA_ROOT, image.name)
        opened_image = Image.open(img_path)
        new_img = opened_image.resize(
            (new_height, new_width), Image.Resampling.BICUBIC)
        new_img.save(fp=img_path, optimize=True, quality=50)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
        if self.image:
            self.update_image(self.image)
