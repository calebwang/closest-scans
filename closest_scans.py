from glob import glob
import os, re
import pandas
from dateutil import parser
from datetime import datetime

def get_scans(data_dir, id, scantype):
    """
    Gets a list of directories for scantype scans under data_dir/id
    scantype:
        FDG, FDG2, NIFDFDG2, PIB, COG_S#, NIFDPIB"""
    if not data_dir:
        data_dir = os.getcwd()
    globstr = os.path.join(data_dir, id, scantype.upper() + '*')
    files = glob(globstr)
    files.sort()
    if len(files) < 1:
        print 'No %s scans found.'%scantype
    return files
    
def parse_date(filename):
    """Grabs a date from a file in format *_YYYY-MM-DD[-HH]"""
    datestring = filename.split('_')[-1]
    date = parser.parse(datestring)
    return date

def parse_id(filename):
    """Grabs LBNL ID from filename"""
    match = re.search('B[0-9]{2}-[0-9]{3}', filename) 
    if match:
        return match.group()
    return None
    
def date_delta(dt1, dt2):
    """gets dt2 - dt1 in days"""
    delta = dt2 - dt1 
    return abs(delta.days)

def find_closest(filelist, ref_date = datetime.now()):
    """Given a list of datestamped files, get the closest one"""
    closest = None
    for filename in filelist:
        date = parse_date(filename)
        time_diff = date_delta(date, ref_date)
        if not closest:
            closest = (filename, time_diff)
        if time_diff < closest[1]:
            closest = (filename, time_diff)
    return closest

def get_closest(data_dir, id, scan_type, ref_date = datetime.now()):
    """Gets the closest scan_type scan under data_dir/id"""
    if not data_dir:
        data_dir = os.getcwd()
    print data_dir
    scans = get_scans(data_dir, id, scan_type)
    closest = find_closest(scans, ref_date)
    return closest

def parse_excel(filename):
    """Parse an excel file"""
    ef = pandas.ExcelFile(filename)
    df = ef.parse(ef.sheet_names[0])
    cols = df.columns
    #verify correct column structure here
    #expect [lbnl id, date]
    entries = df.to_records().tolist()
    if not (parse_id(entries[0][1]) and type(entries[0][2]) == datetime):
        raise TypeError('Infile columns should be in format [lbnl id, date]')
    return entries

def timestamp(filename):
    name, ext = splitext(filename)
    return name + '_' + str(datetime.today()).replace(' ', '-') \
                                             .split('.')[0] + ext

def process_excel(infile, outfile, data_dir, scan_type):
    """Process and write output to outfile for each entry in infile"""
    entries = parse_excel(infile)
    lines = []
    for entry in entries:
        closest = get_closest(data_dir, entry[1], scan_type, entry[2])
        fileloc, tdelta = closest[0], closest[1]
        line = (parse_id(fileloc), fileloc, str(parse_date(fileloc).date()), str(entry[2].date()), tdelta)
        lines.append(line)
    df = pandas.DataFrame(lines, columns = ['lbnl id', 'file path', 'scan date', 'target date', 'time delta'])
    df.to_excel(outfile, sheet_name = 'Sheet1', index = False)

