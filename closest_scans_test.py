from unittest import TestCase, skipIf, skipUnless
from numpy.testing import (assert_raises, assert_equal, assert_almost_equal)
import os
import closest_scans
from datetime import datetime, date
import pandas

class TestClosestScans(TestCase):
    def test_get_scans(self):
        real_cog = []
        real_fdg = ['data/B99-999/FAKEFDG_2011-1-31', 'data/B99-999/FAKEFDG_2012-3-4']
        cog = closest_scans.get_scans('data', 'B99-999', 'FAKECOG_S')
        fdg = closest_scans.get_scans('data', 'B99-999', 'FAKEFDG')
        assert_equal(cog, real_cog)
        assert_equal(fdg, real_fdg)

    def test_parse_date(self):
        d = closest_scans.parse_date('2013-3-1')
        real_d = datetime(2013, 3, 1)
        assert_equal(d, real_d)

    def test_date_delta(self): 
        d1 = datetime(2011, 2, 25)
        d2 = datetime(2011, 2, 13)
        assert_equal(closest_scans.date_delta(d1, d2), 12)

    def test_find_closest(self):
        fdg = closest_scans.get_scans('data', 'B99-999', 'FAKEFDG')
        closest = closest_scans.find_closest(fdg, datetime(2012, 4, 4))
        assert_equal(closest, ('data/B99-999/FAKEFDG_2012-3-4', 31))

    def test_parse_excel(self):
        expected = [(0, u'B05-201', datetime(2009, 3, 23)), \
                    (1, u'B05-202', datetime(2009, 6, 2)), \
                    (2, u'B05-215', datetime(2008, 10, 6))]
        entries = closest_scans.parse_excel('data/example.xls')
        assert_equal(entries, expected)

    def test_process_excel(self):
        infile = os.path.join('data', 'test.xls')
        outfile = os.path.join('data', 'output.xls')
        closest_scans.process_excel(infile, outfile, 'data', 'FAKEFDG') 
        df = pandas.ExcelFile(outfile).parse('Sheet1')
        entry = df.to_records().tolist()[0]
        expected = (0, u'B99-999', u'data/B99-999/FAKEFDG_2012-3-4', u'2012-03-04', u'2012-04-05', 32.0)
        assert_equal(entry, expected)
        if os.path.exists(outfile):
           os.remove(outfile) 
