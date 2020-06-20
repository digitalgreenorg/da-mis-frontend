from django.core.management.base import BaseCommand
import xlrd

from kpi.views.v2.geography import GeographyChecker


class Command(BaseCommand):
    help = '''This command fills data for csv file to db '''

    def add_arguments(self, parser):
        parser.add_argument('-f',
                            dest='filename',
                            default='sample.xlsx')

    # generate the excel for the given command line arguments
    def handle(self, *args, **options):
        if options.get('filename') is not None:
            filename = options.get('filename')
            wb = xlrd.open_workbook(filename)
            sheets = wb.sheet_names()
            for sheet in sheets:
                sheet_to_import = wb.sheet_by_name(sheet)
                for row in range(1, sheet_to_import.nrows):
                    region = GeographyChecker().get_or_create_region(str(sheet_to_import.cell_value(row,1)))
                    zone = GeographyChecker().get_or_create_zone(str(sheet_to_import.cell_value(row,2)), region)
                    woreda = GeographyChecker().get_or_create_woreda(str(sheet_to_import.cell_value(row,3)), zone)
                    kebele = GeographyChecker().get_or_create_kabele(str(sheet_to_import.cell_value(row,4)), woreda)
            print("Imported Locations successfully")
