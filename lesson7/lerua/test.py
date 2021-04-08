from functools import reduce

string = 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_90,w_82,h_82,c_pad,b_white,d_photoiscoming.png/LMCode/18720655.jpg'



import re

def replace_size(string):
    pat = r'h_\w{2}'
    m = re.findall(pat, string)
    s = string.replace(m[0], 'h_2000')
    pat = r'w_\w{2}'
    m = re.findall(pat, s)
    return s.replace(m[0], 'w_2000')

#reduce(lambda s, m: s.replace(m, m + str(m.index('h_2000'))), re.findall(r'h_\w{2}', string), string)
print(replace_size(string))

