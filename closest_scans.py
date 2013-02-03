from glob import glob
import os, re
import pandas
from dateutil import parser
from datetime import datetime

def get_scans(data_dir, id, scantype):
    """FDG, FDG2, NIFDFDG2, PIB, COG_S#, NIFDPIB"""
    globstr = os.path.join(data_dir, id, scantype.upper() + '*')
    files = glob(globstr)
    files.sort()
    if len(files) < 1:
        print 'No %s scans found.'%scantype
    return files
    
def parse_date(filename):
    datestring = filename.split('_')[-1]
    date = parser.parse(datestring)
    return date

def date_delta(dt1, dt2):
    delta = dt2 - dt1 
    return abs(delta.days)

def find_closest(filelist, ref_date = datetime.now()):
    closest = None
    for filename in filelist:
        date = parse_date(filename)
        time_diff = date_delta(date, ref_date)
        if not closest:
            closest = (filename, time_diff)
        if time_diff < closest[1]:
            closest = (filename, time_diff)
    return closest

def parse_excel(filename):
    df = pandas.ExcelFile(filename).parse('Sheet1')
    cols = df.columns
    #verify correct column structure
    entries = df.to_records().tolist()
    return entries
