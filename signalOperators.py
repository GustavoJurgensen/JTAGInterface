from random import sample
def bitsToChar(array):#convert bits to character
    integer = 0
    c = ''
    for i in range(0,7):
        integer += array[6-i]*(2**i)
    c = chr(integer)
    #print(chr(integer))
    return c  
def charToBits(character):#convert Character to bits
    decNumber = ord(character)
    array = []
    while decNumber > 0:
        rem = decNumber % 2
        array.append(rem)
        decNumber = decNumber // 2
    size = len(array)
    for i in range(0,7):#additional bits, in the ASC-2 table,7 is the maximun bits can be used
        if(i<(7-size)):
            array.append(0)
    #print(array)
    array.reverse()
    return array
def stringToBinary(fileName):#convert any "string" to binary array 
    aux = []
    aux2 = []
    array = []
    with open(fileName,"r") as txt:# open file where are "strings"
        for i in txt:
            aux.append(i)
    for i in aux:
        for j in i:
            aux2.append(j)
    for i in aux2:
        for j in charToBits(i):
            array.append(j)
    #print(array)
    return array#return binary array
def fileToString(fileName):
    array=[]
    with open(fileName,"r") as original:
        for i in original:
            array.append(i)
    return array
def convertToSquare(array):#convert binary wave for binary square wave
    aux = []
    for i in array:
        for j in range(0,20):
            aux.append(i)
    return aux
def NRZ_L(array, reverse):#apply NRZ-L coding 
    after=[]
    if reverse == False:#encoding
        for i in array:
            if int(i) == 0:
                after.append(1)
            else:
                after.append(-1)
    if reverse == True:#decoding
        for i in array:
            if int(i) == 1:
                after.append(0)
            else:
                after.append(1)
    return after
def convert_txt(fileName):#convet Txt file
    before=[]
    after=[]
    before = stringToBinary(fileName)#original signal
    after = NRZ_L(before,False)#signal encoded by NRZ_L 

    return before,after
def add_noise(array, percent):#add noise according to a percentage

    mult =int(len(array)*percent)
    error = sample(range(0,len(array)),mult)
    #print(len(array))
    #print(error)
    #print(len(error))
    for i in error:
        if(array[i]==1):
            array[i]=-1
        else:
            array[i]=1
    return array
def writeNoise(array):#write in a file the signal after apply noise
    array = NRZ_L(array, True)
    buffer = []
    ret = []
    count = 0
    for i in array:
        buffer.append(i)
        count += 1
        if(count%7 == 0):
            ret.append(bitsToChar(buffer))
            #print(buffer)
            count = 0
            buffer = []
    #print(ret)
    string_ = ""
    for i in range(0,len(ret)):
        string_ += ret[i]
    #print(string_)
    file_ = open("noise.txt", "w")
    file_.write(string_)