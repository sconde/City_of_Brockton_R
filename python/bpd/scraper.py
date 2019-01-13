'''
File: scraper.py
Author: Sidafa Conde
Email: sconde@umassd.edu
Purpose: Brockton PD scraper
'''
from bs4 import BeautifulSoup
from datetime import datetime
import urllib

class Scraper():
    main_link = "http://www.brocktonpolice.com/category/police-log/"
    bp_wp_content = "http://www.brocktonpolice.com/wp-content/uploads"

    def __init__(self, year):
        self.year = year
        self.year_link = bp_wp_content+'/'+str(year)
        self.all_months = [self.year_link+'/'+str(x).zfill(2) for x in range(1,13)]
        self.date_time = datetime.strptime(str(year),'%Y')
        self.all_pdfs = []

    def get_month_pdf(self, mth_int=1):
        '''
        inspect the link of each months and update `all_pdfs` with pdfs links
        '''
        record_date = self.date_time
        record_date = record_date.replace(month=mth_int)
        # print(record_date)
        mth_dt_lin = self.year_link+'/'+str(mth_int).zfill(2)
        all_pdfs = self._get_list_of_pdfs_in_mth(mth_dt_lin)
        self.all_pdfs.extend(all_pdfs)

    def _get_list_of_pdfs_in_mth(self, site_link):
        page = urllib.request.urlopen(site_link)
        soup_pg= BeautifulSoup(page, features="lxml")
        soup_li = soup_pg.findAll('li')
        soup_li = map(lambda x: x.string.strip(), soup_li)
        all_pdfs = filter(lambda x: x.endswith('.pdf'), soup_li)
        all_pdfs = map(lambda x: site_link+'/'+x, all_pdfs)
        return list(all_pdfs)

    def download_all_pdf(self, path_to_save):
        for pdf_url in self.all_pdfs:
            filename = '-'.join(pdf_url.split('/')[-3:])
            urllib.request.urlretrieve(pdf_url, path_to_save+filename)

