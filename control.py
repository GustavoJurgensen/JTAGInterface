from PyQt5.QtWidgets import*
from PyQt5 import uic,QtWidgets,QtGui
import numpy as np
import signalOperators as sop
import hashlib
import zlib
#class for main window operations
class TextScreen(QDialog):
    def __init__(self):
        super(TextScreen,self).__init__()

        uic.loadUi("textScreen.ui",self)#load file of Qt Designer (textScreen)

        self.setWindowTitle("JTAG Simulation - Comparative")#set title window
        self.setWindowIcon(QtGui.QIcon("jtag.png"))#det icon window

    def makeText(self,fileName):#add text file in text boxes
        #original text
        text1= sop.fileToString(fileName)
        for i in text1:
            self.textBrowser.append(i)
        #with noise text
        text2= sop.fileToString("noise.txt")
        self.textBrowser_2.clear()
        for i in text2:    
            self.textBrowser_2.append(i)
        

class MatplotlibWidget(QMainWindow):
    #binary matrices for slide bar
    Mbefore =[]
    Mafter = []
    Mnoise = []

    def __init__(self):#init application
        
        QMainWindow.__init__(self)#Main window init

        uic.loadUi("interface.ui",self)#load file of Qt Designer (Interface)

        self.setWindowTitle("JTAG Simulation")#set title window
        self.setWindowIcon(QtGui.QIcon("jtag.png"))#det icon window
        
        #slide bar settings
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.updateGraph)#when the value of the bar updated, call the updateGraph function

        #buttons settings. When clicked, they call the your functions
        self.generate.clicked.connect(self.createGraph)
        self.checksum.clicked.connect(self.checksumTest)
        self.crc.clicked.connect(self.crcTest)
        self.comparative.clicked.connect(self.openTextScreen)

    def openTextScreen(self):
        fileName = self.lineEdit.text()
        newWindow.makeText(fileName)
        newWindow.show()
    def updateGraph(self):#Update the graphs according to the slide bar
        value = self.slider.value()#slide bar value
        self.labelSlider.setText(str(value))#print on interface

        #plot original signal graph
        before = sop.convertToSquare(self.Mbefore[value])#convert to square wave
        xb = np.arange(0,len(before))
        self.graph1.canvas.axes.clear()
        self.graph1.canvas.axes.plot(xb, before)
        self.graph1.canvas.axes.set_title('Before JTAG')
        self.graph1.canvas.draw()
        
        #plot encoded signal graph
        after = sop.convertToSquare(self.Mafter[value])
        xa = np.arange(0,len(after))
        self.graph2.canvas.axes.clear()
        self.graph2.canvas.axes.plot(xa, after)
        self.graph2.canvas.axes.set_title('After JTAG - Encoded by NRZ-L')
        self.graph2.canvas.draw()
        if self.checkBox.isChecked():#verify noise checkBox
            #plot encoded signal with noise graph
            noise = sop.convertToSquare(self.Mnoise[value])
            xn = np.arange(0,len(noise))
            self.graph3.canvas.axes.clear()
            self.graph3.canvas.axes.plot(xn, noise)
            self.graph3.canvas.axes.set_title('After Noise')
            self.graph3.canvas.draw()

    def createGraph(self):
        fileName = self.lineEdit.text()#Read file name
        #Restart variables, because is a new graph being generated
        self.Mbefore = []
        self.Mafter = []
        self.Mnoise = []
        before = []
        after=[]
        noise=[]

        #converts txt to binaries
        before,after = sop.convert_txt(fileName)
        
        #Assignment of matrices for each point on the slide bar 0-100
        buffer =[]
        for i in range(0,len(before)):
            buffer.append(before[i])
            if ((i%int(len(before)/100)==0)and i>0) or i==(len(before)-1):
                self.Mbefore.append(buffer)
                buffer =[]
        buffer =[]
        for i in range(0,len(after)):
            buffer.append(after[i])
            if ((i%int(len(after)/100)==0)and i>0) or i==(len(after)-1):
                self.Mafter.append(buffer)
                buffer =[]
        
        noise = after
        if self.checkBox.isChecked():#verify noise checkBox
            inputTextNoise = self.noise_input.text()
            noise = sop.add_noise(noise,float(inputTextNoise))
            
            #write signal in new file txt with noise
            sop.writeNoise(noise)

            buffer =[]
            for i in range(0,len(noise)):
                buffer.append(noise[i])
                if ((i%int(len(noise)/100)==0)and i>0) or i==(len(noise)-1):
                    self.Mnoise.append(buffer)
                    buffer =[] 
        #start graph in position 0            
        self.updateGraph()

    def checksumTest(self):
        fileName = self.lineEdit.text()

        check1 = open(fileName,'rb')
        data1 = check1.read()
        first_md5 = hashlib.md5(data1).hexdigest()

        check2 = open("noise.txt", 'rb')
        data2 = check2.read()
        second_md5 = hashlib.md5(data2).hexdigest()

        if first_md5 == second_md5:
            self.checksumLabel.setText("No errors detected")
        else:
            self.checksumLabel.setText("Errors detected")
            
    def crcTest(self):
        prev = 0
        path1 = self.lineEdit.text()
        path2 = "noise.txt"
        for eachLine in open(path1,"rb"):
            prev = zlib.crc32(eachLine, prev)
        first_crc = "%X"%(prev & 0xFFFFFFFF)
        prev = 0
        for eachLine in open(path2,"rb"):
            prev = zlib.crc32(eachLine, prev)
        second_crc = "%X"%(prev & 0xFFFFFFFF)

        if first_crc == second_crc:
            self.crcLabel.setText("No errors detected")
        else:
            self.crcLabel.setText("Errors detected")

app = QApplication([])#define application
w = MatplotlibWidget()#define window, in this case "Main Window"
newWindow = TextScreen()
w.show()# show window
app.exec_()#execute app
