import uuid
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse

from users.models import Account


class HideProduct(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_hidden=True)


class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    slug = models.CharField(max_length=150, null=False, blank=False)
    is_hidden = models.BooleanField(default=False, help_text='o = default, 1 = Hidden')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    active_object = HideProduct()

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Category)
def save_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)
    slug = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to='images/', null=True, blank=True)
    small_description = models.CharField(max_length=250, null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text='o = default, 1 = Hidden')
    create_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    delete_object = HideProduct()

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"slug": self.slug})

    @property
    def get_image_url(self):
        if self.product_image:
            return self.product_image.url
        else:
            return ''

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Product)
def save_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)
    cart_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @property
    def total_of_items(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.subtotal for item in cartitems])
        return total

    @property
    def cartquantity(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product.name

    @property
    def subtotal(self):
        total = self.quantity * self.product.selling_price
        return total






