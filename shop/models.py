from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Food(models.Model):

    name = models.CharField(_("食物名稱"), max_length=50, unique=True)
    price = models.PositiveIntegerField(_("食物價格"))


    def __str__(self):
        return f"{self.name} 價格: {self.price}"


# Food(name="牛奶", price=200).save()
# Food(name="牛肉", price=550).save()