from bpd import parser

bpd_parser = parser.Parser()

pdf1 = 'pdf_files/2015/2015-01-Jan2015.pdf'
text1 = bpd_parser.convert_pdf_to_txt(pdf1).split('\n')

chunck_text = bpd_parser.convert_text_to_df(text1)
df = bpd_parser.get_df(chunck_text)
print(df)
