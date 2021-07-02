from django.db import models


class Resort(models.Model):
    name = models.CharField(max_length=36)
    description = models.TextField(null=True, blank=True)
    extra_info = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=6)
    street_address_1 = models.CharField(max_length=80,
                                       null=False,
                                       blank=False)
    street_address_2 = models.CharField(max_length=80,
                                       null=True,
                                       blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    scenic = models.BooleanField(default=False, null=True, blank=True)
    family_friendly = models.BooleanField(default=False, null=True, blank=True)
    adult_price = models.DecimalField(max_digits=6,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)
    child_price = models.DecimalField(max_digits=6,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)
    family_price = models.DecimalField(max_digits=6,
                                       decimal_places=2,
                                       null=True,
                                       blank=True)
    x_map_reference = models.DecimalField(max_digits=6,
                                          decimal_places=4,
                                          null=True,
                                          blank=True)
    y_map_reference = models.DecimalField(max_digits=6,
                                          decimal_places=4,
                                          null=True,
                                          blank=True)
    image = models.ImageField(null=True, blank=True)
    image_credit = models.CharField(max_length=64, null=False, blank=False)
    map_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
