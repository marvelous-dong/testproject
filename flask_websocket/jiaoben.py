import re
string1 = "fdsafdsafasdf.png"
string2 = "fdafdsfadsfdsaf.jpeg"
reg = ".png$|.jpeg$"

print(re.findall(reg, string2))