
dicts={
    "name":"斜杠ASCII码转换",
    "crypto_name":"slashASCII",
    "range":"[0-9/]",
    "alphabet_num":"11",
    "key":"False"
}

def slashASCII(cryptostr):
    cc = cryptostr.rsplit("/")
    flag = ''
    for i in cc[1:]:
        flag += chr(int(i))
    return flag.encode()
