from kpi.models import Region, Zone, Woreda, Kebele


class GeographyChecker():

    def get_or_create_region(self, label):
        region = Region.objects.filter(label=label)
        if region.count() > 0:
            return region[0]
        else:
            region = Region(name=label.strip().lower(), label=label)
            region.save()
            return region

    def get_or_create_zone(self, label, region):
        zone = Zone.objects.filter(label=label, region=region)
        if zone.count() > 0:
            return zone[0]
        else:
            zone = Zone(name=label.strip().lower(), label=label, region=region)
            zone.save()
            return zone

    def get_or_create_woreda(self, label, zone):
        woreda = Woreda.objects.filter(label=label, zone=zone)
        if woreda.count() > 0:
            return woreda[0]
        else:
            woreda = Woreda(name=label.strip().lower(), label=label, zone=zone)
            woreda.save()
            return woreda

    def get_or_create_kabele(self, label, woreda):
        kabele = Kebele.objects.filter(label=label, woreda=woreda)
        if kabele.count() > 0:
            return kabele[0]
        else:
            kabele = Kebele(name=label.strip().lower(), label=label, woreda=woreda)
            kabele.save()
            return kabele
