""" python3 默认使用 unicode 编码 """

# name = '黃楷軒'
# utf8_name = name.encode('utf-8')
# unicode_name = name.encode('unicode_escape')
# print(unicode_name)
# print(utf8_name)

#############################################################################
""" python 16進制轉換 """

# # 在 Python 3.x 版本中，字符串类型默认采用 Unicode 编码，而字节串类型采用 ASCII 编码
# string = 'hello\x01world'
# byte_string = string.encode() # String 字符串转换为 Byte 字節串
# # \\x 表示字符串中插入一个十六进制的字节，{:02x} 表示要用两位十六进制数表示，并且不足两位的要在左侧用 0 填充，例如字节值为 15 时，这个格式化表达式会输出 \x0f
# hex_string = ''.join('\\x{:02x}'.format(b) for b in byte_string)
# print(hex_string)


#############################################################################
""" python sorted """

# a = (("a", 2), ("b", 1), ("c", 4), ("d", 3))
# print(sorted(a, key=lambda x: x[1]))

# import operator

# a = {"a": 2, "b": 1, "c": 4, "d": 3}
# print(sorted(a.items(), key=operator.itemgetter(0)))

#############################################################################
""" python zip """

# arr1 = [1,2,3] 
# arr2 = [4,5,6]

# arr3 = zip(arr1, arr2)

# for item in arr3:
#     print(item)

#############################################################################
""" python all """

# 空字串、0、False 都會是 False
# x = all([1,2,3,False,1])
# print(x)

#############################################################################
""" python any """

# 其中一個為 True 就算 True
# print(any([1,0,"2"]))
# print(any([False,0,""]))

#############################################################################
""" python unicodedata """

# import unicodedata as ud

# # lookup 會回傳符號依據指定的 unicode 字符名稱
# print(ud.lookup('RIGHT CURLY BRACKET'))

# # name 會回傳符號名稱依據指定的 Unicode 符號
# print(ud.name('$'))

# # digit 用來判斷一个 Unicode 字符是否是数字字符
# print(ud.decimal('9'))

# # category 會返回 Unicode 字符的類別
# string = 'hello\x01world\uE000'
# for c in string:
#     if ud.category(c) == 'Cc':
#         print(c, ud.category(c))

# # bidirectional 返回一个字符在 Unicode 中的双向文本方向属性
# print(ud.bidirectional('\u3333'))

#############################################################################
""" python map """

'''import re

def plus_one(x):
    ans = x + str(1)
    return ans

fruit = ['apple', 'orange', 'grape', 'mango']
a = '|'.join(list(map(plus_one, fruit)))
print(a)'''

#############################################################################
""" python enumerate """

# enumerate 对一个 iterable 同时返回下标（index）和值（value），可以指定下标的起点
# list1 = [1,2,3,4,5,6]
# for index, value in enumerate(list1):
#     print(index, value)

#############################################################################
""" python regular expression """

import re
# re 自帶函數都可以嘗試

words = "Hello james, I have 3 apple do you want, please take 2 from me"
word = 'Regular Expression_123'

print(word,'\n')

# 匹配 a、b、c 中的任意一个字符
pattern1 = re.compile(r"[abc]")
print(r"[abc] :", pattern1.findall(word))

# 匹配 a 到 z 中的任意一个小寫字母，可以自定範圍
pattern1 = re.compile(r"[a-z]")
print(r"[a-z] :", pattern1.findall(word))

# ^ 匹配除了的意思
pattern1 = re.compile(r"[^a-z]")
print(r"[^a-z] :", pattern1.findall(word))

# 匹配 A 到 Z 中的任意一个大写字母
pattern1 = re.compile(r"[A-Z]")
print(r"[A-Z] :", pattern1.findall(word))

# 匹配 0 到 9 中的任意一个数字
pattern1 = re.compile(r"[0-9]")
print(r"[0-9] :", pattern1.findall(word))

# 匹配任意一个数字，相当于 [0-9]
pattern1 = re.compile(r"\d")
print(r"\d :", pattern1.findall(word))

# 匹配任意一个非数字字符，相当于 [^0-9]
pattern1 = re.compile(r"\D")
print(r"\D :", pattern1.findall(word))

# 匹配任意一个字母、数字或下划线，相当于 [a-zA-Z0-9_]
pattern1 = re.compile(r"\w")
print(r"\w :", pattern1.findall(word))

# 匹配任意一个非字母、数字或下划线字符，相当于 [^a-zA-Z0-9_]
pattern1 = re.compile(r"\W")
print(r"\W :", pattern1.findall(word))

# 匹配任意一个空白字符，相当于 [\t\n\r\f\v]
pattern1 = re.compile(r"\s")
print(r"\s :", pattern1.findall(word))

# 匹配任意一个非空白字符，相当于 [^\t\n\r\f\v]
pattern1 = re.compile(r"\S")
print(r"\S :", pattern1.findall(word))
