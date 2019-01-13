from bpd import scraper


year = 2015
sc_yr = scraper.Scraper(year)
for yr in range(1,13):
    sc_yr.get_month_pdf(yr)

# view the list of pdfs to download
print(sc_yr.all_pdfs)

# download all the pdfs
sc_yr.download_all_pdf('pdf_files/2015/')
