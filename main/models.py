from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Catalog(models.Model):
    title = models.CharField('Название', max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.IntegerField("Цена")
    photo = models.ImageField(upload_to='photo', blank=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"{self.title}\n{self.price}"

    class Meta:
        verbose_name = "Catalog"
