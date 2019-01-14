'''
filename: example_pdfminer.py
stackoverflow: https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
'''
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

class Parser():
    day_start_reg_ex = "^For Date:\s*(\d{2}\/\d{2}\/\d{4})\s*-\s*(\w*)"
    call_reg_ex = "^(\s|\d{2}-\d*)\s*(\d{4})\s*(.*?)\s{2,}(.*)"
    p_call_reg_ex = "^(\s|\d{2}-\d*)\s*(\d{4})\s*(.*?)\s{2,}(.*)"
    location_reg_ex = "^\s*Location/Address:\s*(.*)"
    office_reg_ex = "^\s*ID:\s*(.*)"
    call_taker_reg_ex = "^\s*Call Taker:\s*(.*)"
    disp_clrd_reg_ex = "^\s*Disp-(\d{2}:\d{2}:\d{2})\s*(Arvd-\d{2}:\d{2}:\d{2})?\s*Clrd-(\d{2}:\d{2}:\d{2})"
    was_arrest_made_reg_ex = "^\s*Refer To Arrest:\s*(.*)"
    refer_to_summon_reg_ex = "^\s*Refer To Summons:\s*(.*)$"
    summon_reg_ex = "^\s*Summons:\s*(.*)$"
    arrest_reg_ex = "^\s*Arrest:\s*(.*)$"
    address_reg_ex = "^\s*Address:\s*(.*)$"
    age_reg_ex = "^\s*Arrest:\s*(.*)$"
    charges_reg_ex = "^\s*Charges:\s*(.*)$"

    def __init__(self):
        pass

    def convert_pdf_to_txt(self, path):
        '''
        purpose: convert pdf file located at `path` to a text file using PDfMiner
        '''
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        with open(path, 'rb') as fp:
            # fp = open(path, 'rb')
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            password = ""
            maxpages = 0
            caching = True
            pagenos = set()

            for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
                interpreter.process_page(page)

            text = retstr.getvalue()

            # fp.close()
        device.close()
        retstr.close()
        return text

    def convert_text_to_df(self, txt):
        import re
        txt = [t for t in txt if len(t.split()) > 0]

        call_ind = [i for i,item in enumerate(txt) if re.search(self.call_reg_ex, item)];
        call_ind.append(-1)
        chunks = list(zip(call_ind[:-1],call_ind[1:]))
        chuncked_text = list(map(lambda y: txt[y[0]:y[1]], chunks))
        return chuncked_text

    def _log_chunk(self, this_chunk):
        import re
        import pandas as pd
        # now to parse the chuncks
        # this_chunk = chuncked_text[0]
        m = re.match(self.p_call_reg_ex, this_chunk[0]).groups()
        call_number = m[0]
        callTime = m[1]
        callReason = m[-1]
        callAction = None
        dateOfCall = None
        dayOfCall = None
        location_address_re = re.compile(self.location_reg_ex)
        location_address = list(filter(location_address_re.search, this_chunk))
        location_address = location_address[0] if len(location_address) > 0 else None
        print(f'call number: {call_number}, call_time: {callTime}, call reason: {callReason}  address: {location_address}'
              .format(call_number, callTime,callReason, location_address))
        # return a pandas series for this observation
        # df = pd.DataFrame( columns=['Call Time','Call Reason','Location/Address'])
        data = {'Call Time':callTime, 'Call Reason':callReason, 'Location/Address':location_address}
        return pd.DataFrame(data, index=[call_number])
        # return {call_number : pd.DataFrame([[callTime], [callReason], [location_address]],
                                        # columns=['Call Time','Call Reason','Location/Address'])}

    def get_df(self, chuncked_text):
        import pandas as pd
        A = list(map(self._log_chunk, chuncked_text))
        df = pd.DataFrame()
        for a in A:
            df = df.append(a)
        return df
