from glob import glob
import os, re
import pandas
from dateutil import parser

def get_cog(subdir):
    globstr = os.path.join(subdir, 'COG_S*')
    allf = glob(globstr)
    allf.sort()
    if len(allf) < 1:
        print 'NO COG: %s'%globstr
        return None
    return allf

def find_closest_cog(date, datadir):
    cogfiles = get_cog(datadir)
    if cogfiles is None:
        return None
    min = 500
    closest = None
    for cog in cogfiles:
        _, cogf = os.path.split(cog)
        cogdate = parser.parse(cogf.split('_')[-1])
        diff = cogdate - date
        if diff.days < min:
            min = abs(diff.days)
            closest = cog
    return closest, min

def check_reindex_spreadsheet(dataframe):
    """ verify subids and dates, rename columns"""
    columns = dataframe.columns
    exaple_data = dataframe.irow(1).values
    
   

def load_parse_data(infile):
    dat = pandas.ExcelFile(infile)
    sheetnames = dat.sheet_names
    try:
        data = dat.parse(sheetnames[0])
        
    

def get_closest_to_date(dataframe, modality):
    """ given a table of LBLID, DATE pairs,
    find closest sample (modality) to DATE,
    returns sampledir, date, abs(timedelta)"""
    

if __name__ == '__main__':

    datadir = '/home/jagust/graph/data/spm_220'
    allscaninfo = glob('%s/B*/func/scan_info'%datadir)
    allscaninfo.sort()

    cogs = []
    for si in allscaninfo:
        for line in open(si):
            if '_1.5_' in line:
                fname = line
                pth, nme = os.path.split(fname)
                subdir, mridate = os.path.split(pth)
                date = parser.parse(mridate.split('_')[-1])
                cog, diff = find_closest_cog(date, subdir)
                cogf = glob('%s/*.xls'%cog)
                cogs.append([cogf[0], diff])

    
    concated = np.concatenate([pandas.ExcelFile(x).parse('sheet1').values for x,y in cogs], axis = 1)
    df = pandas.ExcelFile(x).parse('sheet1')
    newdf = pandas.DataFrame(concated.T,columns = df.index)
    #newdf.to_excel(<filename>.xls)
