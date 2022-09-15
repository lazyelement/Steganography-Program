choice = input("Hello, choose number of bits you want to change\n")
choice = int(choice)

if choice == 1:
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

elif choice == 2:
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

elif choice == 3:
    #Code to change 3 lsb
    cover_image = 1000100010001000
    payload = 11111111
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
                cover_list[iteration-2] = pay_list[int(x)]
                cover_list[iteration-1] = pay_list[int(x)+1]
                cover_list[iteration] = pay_list[int(x)+2]
                x = x+3
                modulo+=1
        else:
            modulo+=1 

    listToStr = ''.join([str(elem) for elem in cover_list])
    print(listToStr)
    
elif choice == 4:
    #Code to change 4 lsb
    cover_image = 10001000100010001000100010001000
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
                cover_list[iteration-3] = pay_list[int(x)]
                cover_list[iteration-2] = pay_list[int(x)+1]
                cover_list[iteration-1] = pay_list[int(x)+2]
                cover_list[iteration] = pay_list[int(x)+3]
                x = x+3
                modulo+=1
        else:
            modulo+=1 

    listToStr = ''.join([str(elem) for elem in cover_list])
    print(listToStr)

elif choice == 5:
    #Code to change 5 lsb
    cover_image = 10001000100010001000100010001000
    payload = 11111111111111111111
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
                cover_list[iteration-4] = pay_list[int(x)]
                cover_list[iteration-3] = pay_list[int(x)+1]
                cover_list[iteration-2] = pay_list[int(x)+2]
                cover_list[iteration-1] = pay_list[int(x)+3]
                cover_list[iteration] = pay_list[int(x)+4]
                x = x+5
                modulo+=1
        else:
            modulo+=1 

    listToStr = ''.join([str(elem) for elem in cover_list])
    print(listToStr)

elif choice == 6:
    #Code to change 6 lsb
    cover_image = 1000100010001000
    payload = 111111111111
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
                cover_list[iteration-5] = pay_list[int(x)]
                cover_list[iteration-4] = pay_list[int(x)+1]
                cover_list[iteration-3] = pay_list[int(x)+2]
                cover_list[iteration-2] = pay_list[int(x)+3]
                cover_list[iteration-1] = pay_list[int(x)+4]
                cover_list[iteration] = pay_list[int(x)+5]
                x = x+6
                modulo+=1
        else:
            modulo+=1 

    listToStr = ''.join([str(elem) for elem in cover_list])
    print(listToStr)

elif choice == 7:
    #Code to change 7 lsb
    cover_image = 1000100010001000
    payload = 11111111111111
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
                cover_list[iteration-6] = pay_list[int(x)]
                cover_list[iteration-5] = pay_list[int(x)+1]
                cover_list[iteration-4] = pay_list[int(x)+2]
                cover_list[iteration-3] = pay_list[int(x)+3]
                cover_list[iteration-2] = pay_list[int(x)+4]
                cover_list[iteration-1] = pay_list[int(x)+5]
                cover_list[iteration] = pay_list[int(x)+6]
                x = x+7
                modulo+=1
        else:
            modulo+=1 

    listToStr = ''.join([str(elem) for elem in cover_list])
    print(listToStr)






