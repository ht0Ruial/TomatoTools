# TomatoTools
[![GitHub stars](https://img.shields.io/github/stars/ht0Ruial/TomatoTools)](https://github.com/ht0Ruial/TomatoTools/stargazers) [![GitHub forks](https://img.shields.io/github/forks/ht0Ruial/TomatoTools)](https://github.com/ht0Ruial/TomatoTools/network) [![GitHub release](https://img.shields.io/github/release/ht0Ruial/TomatoTools.svg)](https://github.com/ht0Ruial/TomatoTools/releases/latest) [![GitHub issues](https://img.shields.io/github/issues/ht0Ruial/TomatoTools)](https://github.com/ht0Ruial/TomatoTools/issues)

TomatoTools 拥有CTF杂项中常见的编码密码算法的加密和解密方式，还具有自动提取flag的能力，以及异常灵活的插件模块。

![](https://4eaa61a63958b1a-1258343929.cos.ap-nanjing.myqcloud.com/image-20210508142729185.png)



目前支持36种编码和密码算法的加密和解密，包括

- Base16/32/36/58/62/64/85/91/92
- ROT5/13/18/47
- AAencode / XXencode / UUencode / JJencode
- Brainfuck / JSFuck / Jother
- Emoji
- 核心价值观编码 / 与佛论禅
- 莫斯密码 / 培根密码 / 云影密码 / 埃特巴什码 / 波利比奥斯方阵密码 / 凯撒密码 / 栅栏密码
- Shellcode / Handycode / URL
- 敲击码 / A1z26密码 / Quoted-printable编码
- 二进制010编码



其中支持31种密文的分析

- Base16/32/36/58/62/64/85/91/92
- XXencode/UUencode/JJencode
- Brainfuck/JSFuck/Jother
- Emoji
- 核心价值观编码/与佛论禅(佛曰)/与佛论禅(如是我闻)
- 莫斯密码(空格)/莫斯密码(斜杠)/培根密码/云影密码/波利比奥斯方阵密码
- Shellcode/Handycode/URL
- 敲击码/A1z26密码/Quoted-printable编码
- 二进制010编码



## 安装与使用

1.克隆项目及安装TomatoTools所需依赖包

```
git clone https://github.com/ht0Ruial/TomatoTools.git
cd TomatoTools
pip3 install -r requirements.txt
```

2.在TomatoTools源码目录下执行

```
python ./TomatoTools.py
```



## 插件编写规范

插件的功能给TomatoTools带来了很强的灵活性，可以在插件管理页面去添加或删除自定义的插件，

这里有一点很重要，用户添加的解密插件是会同步到密文分析模块的，所以添加的解密插件在写法和定义上必须要严谨些，也要更慎重些，因为一旦添加了一个存在语法错误的插件，将可能导致密文分析出错或者无法运行。

![](https://4eaa61a63958b1a-1258343929.cos.ap-nanjing.myqcloud.com/image-20210508165807336.png)

插件里的 *dicts* 是要添加到 *config.json* 中的，而下边定义的函数 *abcdefg* 则是在加解密时调用的函数



编写插件必须遵守以下几点：

1. **文件名** 、dicts里的 **crypto_name**  和 定义的 **函数名** ，三者必须一致
2. 函数只能 *return*   *bytes* 类型的结果



在自定义的插件函数里，如果需要传入密钥的话，插件函数需接收 *cryptostr* 和 *key* 两个值，否则只需接收 *cryptostr* 一个值，而在函数返回值时，不能返回 *str* 类型的值，需用 *str.encode()* 变成 *bytes* 类型后再return结果。

以下为 *dicts* 内各个键的详解，

```python
name # 添加的插件名称
crypto_name # 函数的名称
range # 密码表范围，必须用正则来表示，base16是[0-9a-f]
alphabet_num # 密码表的字符个数，base32[A-Z2-7=]是33个，rot5[0-9]是10个
key # （这里的key可以直接删掉，删掉后默认为False，也可以直接写 False）
    # 针对某些需要输入密钥的才能解密的密文，比如rabbit，此时key的值需为 True
```



**Demo1：**

需要输入密钥 *key* 的插件，

若用户不输入密钥，则调用该函数时，函数接收到的密钥 *key* 为空字符串

```python
# filename: abcdefg.py

dicts={
    "name":"abcdefg加密",
    "crypto_name":"abcdefg",
    "range":"[1-8]",
    "alphabet_num":"8",
    "key":"True"
}

def abcdefg(cryptostr,key):
    #key= ''
    aa = "12345678"
    return aa.encode()

```

**Demo2：**

不需要输入密钥 *key* 的插件

```python
# filename: test.py

dicts={
    "name":"test解密",
    "crypto_name":"test",
    "range":"[1-8]",
    "alphabet_num":"8",
    "key":"False"
}

def test(cryptostr):
    aa = "12345678"
    return aa.encode()
```



