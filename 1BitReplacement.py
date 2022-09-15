#Code to change 1 lsb
cover_image = 1000100010001000100010001000100010001000100010001000100010001000
payload = 11111111
expected_output = 1000100110001001100010011000100110001001100010011000100110001001

pay_list = [int(x) for x in str(payload)]
cover_list = [int(x) for x in str(cover_image)]
cover_str = str(cover_image)

modulo = 1
counter = 8
x=int()

for iteration, i in enumerate(cover_str):
    if modulo % counter == 0:
        if len(pay_list) < x:
            break
        else:
            cover_list[iteration] = pay_list[int(x)]
            x = x+1
            modulo+=1
    else:
        modulo+=1 

listToStr = ''.join([str(elem) for elem in cover_list])
print(listToStr)

#Code to change 2 lsb
cover_image = 1000100010001000100010001000100010001000100010001000100010001000
payload = 1111111111111111
expected_output = 10001011

pay_list = [int(x) for x in str(payload)]
cover_list = [int(x) for x in str(cover_image)]
cover_str = str(cover_image)

modulo = 1
counter = 8
x=int()

for iteration, i in enumerate(cover_str):
    if modulo % counter == 0:
        if len(pay_list) < x:
            break
        else:
            cover_list[iteration-1] = pay_list[int(x)]
            cover_list[iteration] = pay_list[int(x)+1]
            x = x+2
            modulo+=1
    else:
        modulo+=1 

listToStr = ''.join([str(elem) for elem in cover_list])
print(listToStr)



