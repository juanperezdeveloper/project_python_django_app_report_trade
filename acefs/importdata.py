"""
When run from the command line, this class replaces all the data in the database by importing data from the csv files in
the django_mlds/acefs/data directory.

"""

import os
import sys
import csv

sys.path.append(os.getcwd())

from django.core.management import setup_environ
import settings

setup_environ(settings)

from django_mlds.acefs.models import *

def excelPercentToFloat(string_percent):
    """
    Converts a string with the format "19.7%" w/ or w/o padding to a float

    """
    return float(string_percent.strip()[0:-1])
    
def excelDollarToInt(string_dollar):
    """
    Converts a string with the format "$ 109,850", w/ or w/o padding to an integer.

    """
    return int(''.join(string_dollar.strip()[1:].split(',')))

status_dict = {
    'High School': 'HS',
    'JUCO': 'JC',
    'Undergrad': '4YR'
}

allowed_statuses = status_dict.values()
allowed_positions = ['C', '1B-DH', '2B', '3B', 'SS', 'OF', 'LHP', 'RHP', 'ALL']

def get_statuses(raw_status):
    """
    Helper method to determine status when parsing MLBData input.
    """

    current = None
    statuses = []
    for s in raw_status:
        if s != current and s != '':
            current = s
        try:
            statuses.append(status_dict[current])
        except KeyError, e:
            statuses.append(None)
    return statuses

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def importPrMajorsData():
    """
    Import PrMajors data exported from Supporting Stats tab.

    Export instructions:
     - Increase precision of Supporting Stats!C33:AC58 to 5 places left of the decimal,
     - copy C31:AC58 to a new sheet for export

    """

    reader = csv.reader(open('data/pr-majors.csv', 'rb'), dialect='excel')

    statuses = reader.next()
    positons = reader.next()

    PrMajorsData.objects.all().delete()

    for row in reader:
        draft_cell = row[0]
        for i in range(1,len(row)):

            o = PrMajorsData()
            o.draft_cell = draft_cell
            o.status = get_idx(STATUS_CHOICES, statuses[i].upper())
            o.position = get_idx(POSITION_CHOICES, positons[i].upper())
            o.value = excelPercentToFloat(row[i])
            o.save()

    print 'PrMajorsData: Imported %d data objects' % PrMajorsData.objects.all().count()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def importMLBData():
    """
    Import data exported from MLB Data tab.

    """

    reader = csv.reader(open('data/mlb-data.csv', 'rb'), dialect='excel')

    MLBData.objects.all().delete()

    row = reader.next()
    while row[9].strip()[0:4] != 'YEAR':
        row = reader.next()

    raw_status = row
    statuses = get_statuses(raw_status)
    positons = reader.next()

    for row in reader:

        if row[9] == '':            #Empty row
            continue
        if (len(row[9]) > 3) and (row[9][0:4] == 'YEAR'):   # Status row
            continue
        if row[10][0:3] == 'MLB':   # Position row
            continue

        year = int(row[8])
        draft_cell = int(row[9])

        for idx in range(0, 38):
            status = statuses[idx]
            position = positons[idx]
            if position in allowed_positions:

                o = MLBData()
                o.year = year
                o.draft_cell = draft_cell
                o.status = get_idx(STATUS_CHOICES, status)
                o.position = get_idx(POSITION_CHOICES, position)
                if row[idx].strip()[0:2] == "$-":
                    o.value = None
                else:
                    o.value = excelDollarToInt(row[idx])
                o.save()

    print 'MLBData: Imported %d data objects' % MLBData.objects.all().count()

    
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

def importDOLSalary():
    """
    Import data exported from DOL Salaries tab.

    """
    reader = csv.reader(open('data/dol-salaries.csv', 'rb'), dialect='excel')

    DOLSalary.objects.all().delete()

    for i in range(6):
        discard = reader.next()

    for row in reader:

        o = DOLSalary()
        o.occupation = row[1]
        o.sal10 = excelDollarToInt(row[4])
        o.sal25 = excelDollarToInt(row[5])
        o.sal50 = excelDollarToInt(row[6])
        o.sal75 = excelDollarToInt(row[7])
        o.sal90 = excelDollarToInt(row[8])
        o.save()

    print 'DOLSalary: Imported %d data objects' % DOLSalary.objects.all().count()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

def importCollege():
    """
    Import data exported from Colleges tab.

    Export instructions:
     - Increase precision of College!E2:F1000 to 5 places left of the decimal

    """

    reader = csv.reader(open('data/college.csv', 'rb'), dialect='excel')

    headers = reader.next()

    College.objects.all().delete()

    for row in reader:

        o = College()
        o.school = row[0]
        o.type = row[1]
        o.starting = int(row[2])
        o.mid_career = int(row[3])
        o.start_fx = excelPercentToFloat(row[4])
        o.mid_fx = excelPercentToFloat(row[5])
        o.save()

    print 'College: Imported %d data objects' % College.objects.all().count()


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

def importSlotBonus():
    """
    Import data exported from  Slot Bonuses tab.

    """

    reader = csv.reader(open('data/slot-bonuses.csv', 'rb'), dialect='excel')

    for i in range(2):
        discard = reader.next()

    SlotBonus.objects.all().delete()

    current_draft_cell = 1

    for row in reader:

        o = SlotBonus()
        o.pick = row[0]
        o.amount = excelDollarToInt(row[1])
        if row[2] != '':
            current_draft_cell = int(row[2])
        o.draft_cell = current_draft_cell
        o.save()

    print 'SlotBonus: Imported %d data objects' % SlotBonus.objects.all().count()


def importSigningBonus():

    reader = csv.reader(open('data/exp_sign_bonus.csv', 'rb'), dialect='excel')

    for i in range(2):
        discard = reader.next()

    SigningBonus.objects.all().delete()

    current_draft_cell = 1

    for row in reader:

        if row[0] != '':
            current_draft_cell = int(row[0])
        else:
            status = get_idx(STATUS_CHOICES, row[1].strip().upper())
            if status == None:
                continue
            o = SigningBonus()
            o.draft_cell = current_draft_cell
            o.status = status
            o.amount = excelDollarToInt(row[2])
            o.save()

    print 'SigningBonus: Imported %d data objects' % SigningBonus.objects.all().count()

def importPrOutData():

    PrOutStatus.objects.all().delete()
    PrOutPosition.objects.all().delete()

    reader = csv.reader(open('data/prout.csv', 'rb'), dialect='excel')

    headers = reader.next()

    year = 0
    for row in reader:

        for i in range(1,9):
            position = headers[i]
            pos_idx = get_idx(POSITION_CHOICES, position)

            p = PrOutPosition()
            p.position = pos_idx
            p.year = year
            p.value = float(row[i])
            p.save()

        for i in range(9,12):
            status = headers[i]
            stat_idx = get_idx(STATUS_CHOICES, status)

            p = PrOutStatus()
            p.status = stat_idx
            p.year = year
            p.value = float(row[i])
            p.save()

        year += 1

    print 'PrOutPosition: Imported %d data objects' % PrOutPosition.objects.all().count()
    print 'PrOutStatus: Imported %d data objects' % PrOutStatus.objects.all().count()


if __name__ == '__main__':

    #importPrMajorsData()
    #importMLBData()
    #importDOLSalary()
    #importCollege()
    #importSlotBonus()
    importSigningBonus()
    #importPrOutData()