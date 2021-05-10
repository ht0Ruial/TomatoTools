import requests
import base64
import string
from re import findall, compile
from random import random
from urllib.request import quote, unquote
from bs4 import BeautifulSoup
from ThirdPartyScripts.jjdecode import JJDecoder
from ThirdPartyScripts.jjencode import JJEncoder
from ThirdPartyScripts.Buddha import DecryptFoYue, DecryptRuShiWoWen


def cry_post(url, cry_data):
    try:
        res = requests.post(url, cry_data)
    except:
        result = "[-] 无法请求在线接口，请检查您的网络状态！".encode()
        return result
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'html.parser')
        result = soup.find('pre').text.encode()
    else:
        result = '0'  # 返回str类型使try报错，执行except
    return result


def en_base16(cryptostr):
    result = base64.b16encode(cryptostr.encode())
    return result


def en_base32(cryptostr):
    result = base64.b32encode(cryptostr.encode())
    return result


def en_base64(cryptostr):
    result = base64.b64encode(cryptostr.encode())
    return result


def en_base85(cryptostr):
    result = base64.b85encode(cryptostr.encode())
    return result


def en_base91(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_base91b"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def en_base92(cryptostr):
    url = "http://ctf.ssleye.com/ctf/base92_en"
    data = {"text": cryptostr, "flag": "base92", "encode_flag": "ascii"}
    result = cry_post(url, data)
    return result


def en_base36(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_base36b"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def en_base58(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_base58b"
    data = {"text": cryptostr, "flag": "char", "encode_flag": "utf8"}
    result = cry_post(url, data)
    return result


def en_base62(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_base62b"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def de_base16(cryptostr):
    result = base64.b16decode(cryptostr.encode())
    return result


def de_base32(cryptostr):
    result = base64.b32decode(cryptostr.encode())
    return result


def de_base36(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_base36d"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def de_base58(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_base58d"
    data = {"text": cryptostr, "flag": "char", "encode_flag": "utf8"}
    result = cry_post(url, data)
    return result


def de_base62(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_base62d"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def de_base64(cryptostr):
    result = base64.b64decode(cryptostr.encode())
    return result


def de_base85(cryptostr):
    result = base64.b85decode(cryptostr.encode())
    return result


def de_base91(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_base91d"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def de_base92(cryptostr):
    url = "http://ctf.ssleye.com/ctf/base92_de"
    data = {"text": cryptostr, "flag": "base92", "encode_flag": "ascii"}
    result = cry_post(url, data)
    return result


def rot5(cryptostr):
    result = ''
    ascii_num = string.digits
    lookup_tuple = {}

    for i in range(len(ascii_num)):
        lookup_tuple[ascii_num[i]] = ascii_num[i-5]

    for i in cryptostr:
        if i not in lookup_tuple:
            b = i
        else:
            b = lookup_tuple[i]
        result += b
    return result.encode()


def rot13(cryptostr):
    result = ''
    ascii_case = string.ascii_lowercase
    ascii_case_up = string.ascii_uppercase
    lookup_tuple = {}
    lookup_tuple_up = {}

    for i in range(len(ascii_case)):
        lookup_tuple[ascii_case[i]] = ascii_case[i-13]
    for i in range(len(ascii_case_up)):
        lookup_tuple_up[ascii_case_up[i]] = ascii_case_up[i-13]

    for i in cryptostr:
        if i not in lookup_tuple and i not in lookup_tuple_up:
            b = i
        elif i in lookup_tuple:
            b = lookup_tuple[i]
        else:
            b = lookup_tuple_up[i]
        result += b
    return result.encode()


def rot18(cryptostr):
    result = rot13(rot5(cryptostr).decode())
    return result


def rot47(cryptostr):
    result = ''
    for i in cryptostr:
        if ord(i) > 126 or ord(i) < 33:
            b = i
        elif ord(i) >= 80:
            b = chr(ord(i) - 47)
        else:
            b = chr(ord(i) + 47)
        result += b
    return result.encode()


def de_Shellcode(cryptostr):
    dd = []
    cc = cryptostr.split('\\x')[1:]
    for i in cc:
        dd.append(chr(int(i.upper(), 16)))
    result = ''.join(dd).encode()
    return result


def en_Shellcode(cryptostr):
    dd = []
    for i in cryptostr:
        dd.append(r"\x{}".format((hex(ord(i)))[2:]))
    result = ''.join(dd).encode()
    return result


def de_XXencode(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_xxdecode"
    data = {"text": cryptostr, "encode_flag": "utf8"}
    result = cry_post(url, data)
    return result


def en_XXencode(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_xxencode"
    data = {"text": cryptostr, "encode_flag": "utf8"}
    result = cry_post(url, data)
    return result


def de_UUencode(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_uudecode"
    data = {"text": cryptostr, "encode_flag": "utf8"}
    result = cry_post(url, data)
    return result


def en_UUencode(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_uuencode"
    data = {"text": cryptostr, "encode_flag": "utf8"}
    result = cry_post(url, data)
    return result


def de_Handycode(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_hdcode_de"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def en_Handycode(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_hdcode_en"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def de_Tapcode(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_tapcode_de"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def en_Tapcode(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_tapcode_en"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def de_Morse(cryptostr):
    Morse_dic = {
        '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5',
        '-....': '6', '--...': '7', '---..': '8', '----.': '9', '.-': 'a', '-...': 'b',
        '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h', '..': 'i',
        '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p',
        '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w',
        '-..-': 'x', '-.--': 'y', '--..': 'z', '--.....': '`', '------.': '~', '-.-.--': '!',
        '.--.-.': '@', '-...--': '#', '.-...': '&', '...-..-': '$', '-..-.-': '%', '-.----.': '^',
        '-.-.-.': ';', '-.--.': '(', '-.--.-': ')', '-....-': '-', '..--.-': '_', '-...-': '=',
        '.-.-.': '+', '-.--.--': '[', '-.---.-': ']', '----.--': '{', '-----.-': '}',
        '---...': ':', '.----.': "'", '.-..-.': '"', '--..--': ',', '.-.-.-': '.', '----..': '<',
        '-----.': '>', '-..-.': '/', '..--..': '?'
    }
    if '/' in cryptostr:
        cryptostr.replace('/', ' ')
    cc = []
    for i in cryptostr.lower().split(' '):
        cc.append(Morse_dic.get(i))
    result = ''.join(cc).encode()
    return result


def en_Morse(cryptostr):
    Morse_dic = {
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.', 'a': '.-', 'b': '-...',
        'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.', 'h': '....', 'i': '..',
        'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
        'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--',
        'x': '-..-', 'y': '-.--', 'z': '--..', '`': '--.....', '~': '------.', '!': '-.-.--',
        '@': '.--.-.', '#': '-...--', '&': '.-...', '$': '...-..-', '%': '-..-.-', '^': '-.----.',
        ';': '-.-.-.', '(': '-.--.', ')': '-.--.-', '-': '-....-', '_': '..--.-', '=': '-...-',
        '+': '.-.-.', '[': '-.--.--', ']': '-.---.-', '{': '----.--', '}': '-----.-', ':': '---...',
        "'": '.----.', '"': '.-..-.', ',': '--..--', '.': '.-.-.-', '<': '----..', '>': '-----.',
        '/': '-..-.', '?': '..--..'
    }
    cc = []
    for i in cryptostr.lower():
        cc.append(Morse_dic.get(i))
    result = ' '.join(cc).encode()
    return result


def de_Baconian(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ba_decrypt"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def en_Baconian(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ba_encrypt"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def de_yunyin(cryptostr):
    dic = list(string.ascii_uppercase)
    cc = []
    c2 = [i for i in cryptostr.split('0')]
    for i in c2:
        c3 = 0
        for j in i:
            c3 += int(j)
        cc.append(dic[c3 - 1])
        result = ''.join(cc).encode()
    return result


def en_yunyin(cryptostr):
    cc = []
    dic = list(string.ascii_uppercase)
    for i in cryptostr:
        res = ''
        num = dic.index(i.upper())+1
        if num >= 8:
            res += int(num/8)*'8'
        if num % 8 >= 4:
            res += int(num % 8/4)*'4'
        if num % 4 >= 2:
            res += int(num % 4/2)*'2'
        if num % 2 >= 1:
            res += int(num % 2/1)*'1'
        cc.append(res)
    result = '0'.join(cc).encode()
    return result


def de_Atbash(cryptostr):
    url = "http://ctf.ssleye.com/ctf/atbash_decrypt"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def en_Atbash(cryptostr):
    url = "http://ctf.ssleye.com/ctf/atbash_encrypt"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def de_Polybius(cryptostr):
    Polybius_dic = {
        '11': 'A', '12': 'B', '13': 'C', '14': 'D', '15': 'E', '21': 'F', '22': 'G',
        '23': 'H', '24': 'I', '25': 'K', '31': 'L', '32': 'M', '33': 'N', '34': 'O',
        '35': 'P', '41': 'Q', '42': 'R', '43': 'S', '44': 'T', '45': 'U', '51': 'V',
        '52': 'W', '53': 'X', '54': 'Y', '55': 'Z'
    }
    list = findall(r'.{2}', cryptostr)
    cc = [Polybius_dic[i] for i in list]
    dd = ''.join(cc)
    if 'I' in dd:
        ee = dd.replace('I', 'J')
    result = ("{}\n{}".format(dd, ee)).encode()
    return result


def en_Polybius(cryptostr):
    Polybius_dic = {
        'A': '11', 'B': '12', 'C': '13', 'D': '14', 'E': '15',
        'F': '21', 'G': '22', 'H': '23', 'I': '24', 'J': '24', 'K': '25',
        'L': '31', 'M': '32', 'N': '33', 'O': '34', 'P': '35',
        'Q': '41', 'R': '42', 'S': '43', 'T': '44', 'U': '45',
        'V': '51', 'W': '52', 'X': '53', 'Y': '54', 'Z': '55'
    }
    result = ''
    for i in cryptostr:
        result += Polybius_dic.get(i.upper())
    return result.encode()


def de_Quoted(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_decode"
    data = {"text": cryptostr, "flag": "quoted", "encode_flag": "utf8"}
    result = cry_post(url, data)
    return result


def en_Quoted(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_encode"
    data = {"text": cryptostr, "flag": "quoted", "encode_flag": "utf8"}
    result = cry_post(url, data)
    return result


def de_AAencode(cryptostr):
    url = "http://www.atoolbox.net/Api/GetAADecode.php"
    data = {"code": cryptostr}
    try:
        result = requests.post(url, data).content
    except:
        return "[-] 无法请求在线接口，请检查您的网络状态！".encode()
    if result.decode() == cryptostr:
        return '0'
    if result[-1:] == b";":
        result = result[:-1]
    return result


def en_AAencode(cryptostr):
    url = "http://www.atoolbox.net/Api/GetAAEncode.php"
    data = {"code": cryptostr}
    try:
        result = requests.post(url, data).content
    except:
        return "[-] 无法请求在线接口，请检查您的网络状态！".encode()
    if result.decode() == cryptostr:
        return '0'
    return result


def de_Brainfuck(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_brainfuck_de"
    data = {"text": cryptostr, "encode_flag": "utf8"}
    result = cry_post(url, data)
    return result


def en_Brainfuck(cryptostr):
    url = "http://ctf.ssleye.com/ctf/ctf_brainfuck_en"
    data = {"text": cryptostr, "encode_flag": "utf8"}
    result = cry_post(url, data)
    return result


def de_Emoji(cryptostr):
    url = "http://www.atoolbox.net/Api/GetBase100.php"
    data = {"c": cryptostr, "t": "decode"}
    try:
        result = requests.get(url, data).content.decode(
        ).strip().replace('\n', '')[1:-1].encode()
    except:
        result = "[-] 无法请求在线接口，请检查您的网络状态！".encode()
    return result


def en_Emoji(cryptostr):
    url = "http://www.atoolbox.net/Api/GetBase100.php"
    data = {"c": cryptostr, "t": "encode"}
    try:
        result = requests.get(url, data).content.decode(
        ).strip().replace('\n', '')[1:-1].encode()
    except:
        result = "[-] 无法请求在线接口，请检查您的网络状态！".encode()
    return result


def en_JJencode(cryptostr):
    result = (JJEncoder(cryptostr).encoded_text).encode()
    return result


def de_JJencode(cryptostr):
    result = JJDecoder(cryptostr)
    return result


def de_JSfuck(cryptostr):
    url = "http://ctf.ssleye.com/ctf/jsfuck_decrypt"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def en_JSfuck(cryptostr):
    url = "http://ctf.ssleye.com/ctf/jsfuck_encrypt"
    data = {"text": cryptostr}
    result = cry_post(url, data)
    return result


def en_Jother(cryptostr):
    a = Jother()
    result = (a.toScript(cryptostr)).encode()
    return result


def de_Jother(cryptostr):
    result = "暂不支持Jother解密，但可以在浏览器按F12打开console，输入密文后回车，可得到解密结果".encode()
    return result


def de_Socialism(cryptostr):
    values = '富强民主文明和谐自由平等公正法治爱国敬业诚信友善'
    duo = []
    for i in cryptostr:
        num = values.index(i)
        if num == -1:
            continue
        elif num & 1:
            continue
        else:
            duo.append(num >> 1)
    hexs = []
    i = 0
    while(i < len(duo)):
        if duo[i] < 10:
            hexs.append(duo[i])
        elif duo[i] == 10:
            i += 1
            hexs.append(duo[i] + 10)
        else:
            i += 1
            hexs.append(duo[i] + 6)
        i += 1
    res = ''.join([hex(i)[2:].upper() for i in hexs])
    if len(res) == 0:
        return 0
    splited = []
    for i in range(len(res)):
        if i & 1 == 0:
            splited.append('%')
        splited.append(res[i])
    result = unquote(''.join(splited))
    return result.encode()


def en_Socialism(cryptostr):
    values = '富强民主文明和谐自由平等公正法治爱国敬业诚信友善'
    strs = "0123456789ABCDEF"
    pattern = compile(r"[A-Za-z0-9\-\_\.\!\~\*\'\(\)]")
    str1 = ''
    for i in cryptostr:
        if pattern.match(i) == None:
            str1 += quote(i.encode())
        else:
            str1 += hex(ord(i))[2:]

    concated = str1.replace('%', '').upper()
    duo = []
    for i in concated:
        n = strs.index(i)
        if n < 10:
            duo.append(n)
        elif random() >= 0.5:
            duo.append(10)
            duo.append(n-10)
        else:
            duo.append(11)
            duo.append(n-6)
    result = ''.join([values[2*i]+values[2*i+1] for i in duo])
    return result.encode()


def de_Buddha(cryptostr):
    try:
        result = DecryptFoYue(cryptostr).encode()
    except:
        result = DecryptRuShiWoWen(cryptostr)
    return result


def de_Buddha_FoYue(cryptostr):
    result = DecryptFoYue(cryptostr).encode()
    return result


def de_Buddha_RuShiWoWen(cryptostr):
    result = DecryptRuShiWoWen(cryptostr)
    return result


def en_Buddha(cryptostr):
    url = "https://www.keyfc.net/bbs/tools/tudou.aspx"
    data = {"orignalMsg": cryptostr, "action": "Encode"}
    try:
        a = requests.post(url, data)
        result = ((requests.post(url, data).text)[28:-24]).encode()
    except:
        result = "[-] 无法请求在线接口，请检查您的网络状态！".encode()
    return result


def de_Caesar(cryptostr):
    str1 = string.ascii_lowercase
    str2 = string.ascii_uppercase

    dd = []
    for keys in range(1, 26):
        cc = []
        for i in cryptostr:
            if i in str1:
                cc.append(str1[(str1.index(i)+keys) % 25])
            elif i in str2:
                cc.append(str2[(str2.index(i)+keys) % 25])
            else:
                cc.append(i)
        dd.append(''.join(cc))
    result = '\n'.join(dd)
    return result.encode()


def en_Caesar(cryptostr, key):
    str1 = string.ascii_lowercase
    str2 = string.ascii_uppercase
    cc = []
    keys = int(key) % 25
    for i in cryptostr:
        if i in str1:
            cc.append(str1[str1.index(i)+int(keys)])
        elif i in str2:
            cc.append(str2[str2.index(i)+int(keys)])
        else:
            cc.append(i)
    result = ''.join(cc)
    return result.encode()



def en_Fence(cryptostr, key):
    cc = ''
    for i in range(0, int(key)):
        for j in range(i, len(cryptostr), int(key)):
            if j < len(cryptostr):
                cc += cryptostr[j]
    result = cc.encode()
    return result


def de_Fence(cryptostr):
    cc = []
    for space in range(2, len(cryptostr)):
        s = ""
        if len(cryptostr) % space == 0:
            key = len(cryptostr) // space
        else:
            key = len(cryptostr) // space + 1
        for i in range(0, key):
            for j in range(i, len(cryptostr), key):
                if j < len(cryptostr):
                    s += cryptostr[j]
        cc.append(s)
    result = '\n'.join(cc)
    return result.encode()


def en_a1z26code(cryptostr):
    str1 = string.ascii_lowercase
    s = ""
    for i in cryptostr.lower():
        s += "-{}".format(str1.index(i) + 1)
    result = s[1:].encode()
    return result


def de_a1z26code(cryptostr):
    str1 = string.ascii_lowercase
    res = cryptostr.split("-")
    result = ""
    for i in res:
        result += str1[int(i)-1]
    return result.encode()


def de_Url(cryptostr):
    result = unquote(cryptostr)
    return result.encode()


def en_Url(cryptostr):
    result = quote(cryptostr)
    return result.encode()


def de_010(cryptostr):
    result = ''
    cc = cryptostr.split(" ")
    for i in cc:
        result += chr(int(i,2))
    return result.encode()


def en_010(cryptostr):
    result = ''
    for i in cryptostr:
        result += " {}".format(bin(ord(i))[2:])
    return result[1:].encode()

