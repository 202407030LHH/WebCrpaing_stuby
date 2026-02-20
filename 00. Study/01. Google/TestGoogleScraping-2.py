import re

p = re.compile("s.n")

def print_match(m):
     if m:
        print("m.group():" ,m.group()) # 일치하는 문자열 반환
        print("m.string():" ,m.string) # 입력받은 문자열 반환
        print("m.start():" ,m.start()) # 일치하는 문자열의 시작 index
        print("m.end():" ,m.end()) # 일치하는 문자열의 끝 index
        print("m.span():" ,m.span()) # 일치하는 문자열의 시작 / 끝 

m = p.match("sun")
print_match(m)

m = p.match("sunny")
print_match(m)

lst=p.findall("sunny")
print(lst)