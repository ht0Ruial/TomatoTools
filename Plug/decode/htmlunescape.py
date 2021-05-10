import html 

dicts={
    "name":"HTML实体编码",
    "crypto_name":"htmlunescape",
    "range":"[0-9#&;]",
    "alphabet_num":"13",
    "key":"False"
}

def htmlunescape(cryptostr):
    result = html.unescape(cryptostr)
    return result.encode()
