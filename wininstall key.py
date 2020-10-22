"""generates an OEM cd key for windows 95
    DDDYY-OEM-0mmmmmR-eeeee
   D - day      ; from 1 to 366
   Y - year     ; from 95 to 03
   m - middle   ; random
   R - reminder ; complements middle's digisum to a multiple of 7
   e - end      ; random
"""

from random import randint

day = randint(1, 366)
if day < 10:
    day = '00' + str(day)
elif day < 100:
    day = '0' + str(day)
else:
    day = str(day)
year = randint(95, 103)
year = str(year)[-2:]
middle = ''

sum = 0
for i in range(5):
    digit = randint(0, 9)
    middle += str(digit)
    sum += digit
end = str(randint(0, 99999)).zfill(5)
reminder = str(7 - (sum % 7))  # making sure 0, 5 middle digits and this digit sum up to something divisible by 7
code = day + year + '-OEM-0' + middle + reminder + '-' + end
print(code)
