from random import sample

def sweep(array):
    buffer=[]
    for i in range(0,len(array)):
        if(array[i] =='\x00'):
            print("caracter removido")
        else:
            buffer.append(array[i])
    st = ""
    for i in buffer:
        st += i
    return st

# convert bits to character
def bitsToChar(array):
    integer = 0
    c = ''
    for i in range(0,7):
        integer += array[6-i]*(2**i)
    c = chr(integer)
    #print(chr(integer))
    return c  

# convert Character to bits
def charToBits(character):
    decNumber = ord(character)
    array = []
    while decNumber > 0:
        rem = decNumber % 2
        array.append(rem)
        decNumber = decNumber // 2
    size = len(array)
    # additional bits, in the ASC-2 table
    # 7 is the maximun bits that can be used
    for i in range(0,7):
        if(i<(7-size)):
            array.append(0)
    #print(array)
    array.reverse()
    return array

# convert any "string" to binary array
def stringToBinary(fileName): 
    aux = []
    aux2 = []
    array = []
    # open file where are "strings"
    with open(fileName,"r") as txt:
        for i in txt:
            aux.append(i)
    for i in aux:
        for j in i:
            aux2.append(j)
    st = sweep(aux2)
    #print(aux2)
    #print(st)
    for i in aux2:
        for j in charToBits(i):
            array.append(j)
    file_ = open(fileName,"w")
    file_.write(st)
    return array #return binary array

def fileToString(fileName):
    array=[]
    with open(fileName,"r") as original:
        for i in original:
            array.append(i)
    return array

# convert binary wave for binary square wave
def convertToSquare(array):
    aux = []
    for i in array:
        for j in range(0,20):
            aux.append(i)
    return aux

# apply NRZ-L coding
def NRZ_L(array, reverse): 
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

# convet Txt file
def convert_txt(fileName):
    before=[]
    after=[]
    before = stringToBinary(fileName)#original signal
    after = NRZ_L(before,False)#signal encoded by NRZ_L 
    return before,after

# add noise according to a percentage
def add_noise(array, percent):

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

# write in a file the signal after apply noise
def writeNoise(array):
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
    file_ = open("../data/noise.txt", "w")
    file_.write(string_)