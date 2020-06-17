from django.db import models


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
