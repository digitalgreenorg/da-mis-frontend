import threading
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
import xlwt

from kpi.models import Region, Zone, Woreda, Kebele


class Command(BaseCommand):
    help = '''This command fills data from db to formated excel '''

    def add_arguments(self, parser):
        parser.add_argument('-f',
                            dest='filename',
                            default='result.xlsx')

    # generate the excel for the given command line arguments
    def handle(self, *args, **options):
        if options.get('filename') != None:
            filename = options.get('filename')
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet('result', cell_overwrite_ok=True)
            sheet.write(0,0,"list_name")
            sheet.write(0,1,"name")
            sheet.write(0,2,"label")
            sheet.write(0,3,"region")
            sheet.write(0,4,"zone")
            sheet.write(0,5,"woreda")

            regions = Region.objects.all()
            i=1
            for region in regions:
                sheet.write(i,0,"region")
                sheet.write(i,1,region.name)
                sheet.write(i,2,region.label)
                i=i+1

            zones = Zone.objects.all()
            i=i+1
            for zone in zones:
                sheet.write(i,0,"zone")
                sheet.write(i,1,zone.name)
                sheet.write(i,2,zone.label)
                sheet.write(i,3,zone.region.name)
                i = i + 1

            woredas = Woreda.objects.all()
            i=i+1
            for woreda in woredas:
                sheet.write(i,0,"woreda")
                sheet.write(i,1,woreda.name)
                sheet.write(i,2,woreda.label)
                sheet.write(i,4,woreda.zone.name)
                i = i + 1

            kebeles = Kebele.objects.all()
            i=i+1
            for kebele in kebeles:
                sheet.write(i,0,"kebele")
                sheet.write(i,1,kebele.name)
                sheet.write(i,2,kebele.label)
                sheet.write(i,5,kebele.woreda.name)
                i = i + 1

            workbook.save(filename+'.xls')
