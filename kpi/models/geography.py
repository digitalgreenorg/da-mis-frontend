from django.db import models
from django.conf import settings
from django import forms
from django.contrib import admin


class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name",)


class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "region")


class Woreda(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "zone")


class Kebele(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    woreda = models.ForeignKey(Woreda, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "woreda")


class LocationAccess(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='extra_details',
                                on_delete=models.CASCADE)
    regions = models.ManyToManyField(Region)
    zones = models.ManyToManyField(Zone)
    woredas = models.ManyToManyField(Woreda)
    kebeles = models.ManyToManyField(Kebele)


class LocationAccessForm(forms.ModelForm):
    class Meta:
        model = LocationAccess
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LocationAccessForm, self).__init__(*args, **kwargs)
        self.fields['zones'].queryset = Zone.objects.filter(region__in=self.instance.regions)
        self.fields['woredas'].queryset = Woreda.objects.filter(zone__in=self.instance.zones)
        self.fields['kebeles'].queryset = Kebele.objects.filter(woreda__in=self.instance.woredas)


class LocationAccessAdmin(admin.ModelAdmin):
    form = LocationAccessForm
    filter_horizontal = ['zones', 'woredas', 'kebeles']

