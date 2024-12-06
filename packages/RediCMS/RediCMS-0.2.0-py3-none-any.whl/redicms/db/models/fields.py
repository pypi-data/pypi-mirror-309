from django.db import models

# Mixin to handle extra parameters
class RediCMSFieldMixin:
    def __init__(self, *args, classname=None, label=None, groupid=None, columnspan=None, **kwargs):
        self.classname = classname
        self.groupid = groupid
        self.columnspan = columnspan
        self.customlabel = label or kwargs.get('verbose_name')
        super().__init__(*args, **kwargs)
        if not self.verbose_name and self.customlabel:
            self.verbose_name = self.customlabel

# Custom field classes prefixed with 'R' for RediCMS

class AutoField(RediCMSFieldMixin, models.AutoField):
    pass

class BigAutoField(RediCMSFieldMixin, models.BigAutoField):
    pass

class BigIntegerField(RediCMSFieldMixin, models.BigIntegerField):
    pass

class BinaryField(RediCMSFieldMixin, models.BinaryField):
    pass

class BooleanField(RediCMSFieldMixin, models.BooleanField):
    pass

class CharField(RediCMSFieldMixin, models.CharField):
    pass

class DateField(RediCMSFieldMixin, models.DateField):
    pass

class DateTimeField(RediCMSFieldMixin, models.DateTimeField):
    pass

class DecimalField(RediCMSFieldMixin, models.DecimalField):
    pass

class DurationField(RediCMSFieldMixin, models.DurationField):
    pass

class EmailField(RediCMSFieldMixin, models.EmailField):
    pass

class FileField(RediCMSFieldMixin, models.FileField):
    pass

class FilePathField(RediCMSFieldMixin, models.FilePathField):
    pass

class FloatField(RediCMSFieldMixin, models.FloatField):
    pass

class ImageField(RediCMSFieldMixin, models.ImageField):
    pass

class IntegerField(RediCMSFieldMixin, models.IntegerField):
    pass

class GenericIPAddressField(RediCMSFieldMixin, models.GenericIPAddressField):
    pass

class PositiveBigIntegerField(RediCMSFieldMixin, models.PositiveBigIntegerField):
    pass

class PositiveIntegerField(RediCMSFieldMixin, models.PositiveIntegerField):
    pass

class PositiveSmallIntegerField(RediCMSFieldMixin, models.PositiveSmallIntegerField):
    pass

class SlugField(RediCMSFieldMixin, models.SlugField):
    pass

class SmallIntegerField(RediCMSFieldMixin, models.SmallIntegerField):
    pass

class TextField(RediCMSFieldMixin, models.TextField):
    pass

class TimeField(RediCMSFieldMixin, models.TimeField):
    pass

class URLField(RediCMSFieldMixin, models.URLField):
    pass

class UUIDField(RediCMSFieldMixin, models.UUIDField):
    pass
