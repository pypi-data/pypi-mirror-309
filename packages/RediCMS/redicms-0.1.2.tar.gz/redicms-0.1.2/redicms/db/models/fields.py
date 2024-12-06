from django.db import models

# Mixin to handle extra parameters
class RediCMSFieldMixin():
    def __init__(self, *args, classname=None, label=None, groupid=None, columnspan=None, **kwargs):
        self.classname = classname
        self.groupid = groupid
        self.columnspan = columnspan
        self.customlabel = label or kwargs.get('verbose_name')
        super().__init__(*args, **kwargs)
        if not self.verbose_name and self.customlabel:
            self.verbose_name = self.customlabel

# Custom field classes prefixed with 'R' for RediCMS

class RAutoField(RediCMSFieldMixin, models.AutoField):
    pass

class RBigAutoField(RediCMSFieldMixin, models.BigAutoField):
    pass

class RBigIntegerField(RediCMSFieldMixin, models.BigIntegerField):
    pass

class RBinaryField(RediCMSFieldMixin, models.BinaryField):
    pass

class RBooleanField(RediCMSFieldMixin, models.BooleanField):
    pass

class RCharField(RediCMSFieldMixin, models.CharField):
    pass

class RDateField(RediCMSFieldMixin, models.DateField):
    pass

class RDateTimeField(RediCMSFieldMixin, models.DateTimeField):
    pass

class RDecimalField(RediCMSFieldMixin, models.DecimalField):
    pass

class RDurationField(RediCMSFieldMixin, models.DurationField):
    pass

class REmailField(RediCMSFieldMixin, models.EmailField):
    pass

class RFileField(RediCMSFieldMixin, models.FileField):
    pass

class RFilePathField(RediCMSFieldMixin, models.FilePathField):
    pass

class RFloatField(RediCMSFieldMixin, models.FloatField):
    pass

class RImageField(RediCMSFieldMixin, models.ImageField):
    pass

class RIntegerField(RediCMSFieldMixin, models.IntegerField):
    pass

class RGenericIPAddressField(RediCMSFieldMixin, models.GenericIPAddressField):
    pass

class RPositiveBigIntegerField(RediCMSFieldMixin, models.PositiveBigIntegerField):
    pass

class RPositiveIntegerField(RediCMSFieldMixin, models.PositiveIntegerField):
    pass

class RPositiveSmallIntegerField(RediCMSFieldMixin, models.PositiveSmallIntegerField):
    pass

class RSlugField(RediCMSFieldMixin, models.SlugField):
    pass

class RSmallIntegerField(RediCMSFieldMixin, models.SmallIntegerField):
    pass

class RTextField(RediCMSFieldMixin, models.TextField):
    pass

class RTimeField(RediCMSFieldMixin, models.TimeField):
    pass

class RURLField(RediCMSFieldMixin, models.URLField):
    pass

class RUUIDField(RediCMSFieldMixin, models.UUIDField):
    pass
