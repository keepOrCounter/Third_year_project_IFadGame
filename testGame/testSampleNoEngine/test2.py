from pynput.keyboard import Key, Controller
import time
import pynput

keyboard = Controller()
class eventKeyboard():
    """
    pressed(key) is a internal function for key board listener, please do not
        invoke!
    NOTICE!!!  pressed(key) would check whether main program is down every 10 sec,
        to make it continous working, call activeFlagSet(newFlag=1) to reactive the working status.


    StartListener(): start the listener, also safe for any unterminate listener.
    terminate(): end the listener

    statusGet(): return listener status, 0 for initiated, 1 for started, >=2 for specific keys were pressed,
        -1 for terminated.
    """

    def __init__(self) -> None:

        self.keyValue = -1
        self.timeIntervalStart = 0
        self.timeIntervalEnd = 0
        
        self.keysIntervalStart = 0
        self.keysIntervalEnd = 0
        
        self.activeFlag = -1
        self.keyPressed = pynput.keyboard.Listener(on_press = self.pressed)
        # self.counter = 0
        # self.shortcutThread = False
        
        self.__status = 0
        self.subFunctionDead = False
        self.shortcutFlag = False
        self.recordKey = []
        self.recordedshortcut = {"Key.alt_lz": 2} # Key.alt_lz is default shortcut

        self.keyboard_key_dict = {
    "\x01" : ['ctrl','a'],
    "\x02" : ['ctrl','b'],
    "\x03" : ['ctrl','c'],
    "\x04" : ['ctrl','d'],
    "\x05" : ['ctrl','e'],
    "\x06" : ['ctrl','f'],
    "\x07" : ['ctrl','g'],
    "\x08" : ['ctrl','h'],
    "\t"   : ['ctrl','i'],
    "\n"   : ['ctrl','j'],
    "\x0b" : ['ctrl','k'],
    "\x0c" : ['ctrl','l'],
    "\r"   : ['ctrl','m'],
    "\x0e" : ['ctrl','n'],
    "\x0f" : ['ctrl','o'],
    "\x10" : ['ctrl','p'],
    "\x11" : ['ctrl','q'],
    "\x12" : ['ctrl','r'],
    "\x13" : ['ctrl','s'],
    "\x14" : ['ctrl','t'],
    "\x15" : ['ctrl','u'],
    "\x16" : ['ctrl','v'],
    "\x17" : ['ctrl','w'],
    "\x18" : ['ctrl','x'],
    "\x19" : ['ctrl','y'],
    "\x1a" : ['ctrl','z'],
    "\x1f" : ['ctrl','shift','-'],
    '<186>'  : ['ctrl',';'],
    "<187>"  : ['ctrl','='],
    "<189>"  : ['ctrl','-'],
    "<192>"  : ['ctrl','`'],
    "<222>"  : ['ctrl',r"'"],
    "<48>"   : ['ctrl','0'],
    "<49>"   : ['ctrl','1'],
    "<50>"   : ['ctrl','2'],
    "<51>"   : ['ctrl','3'],
    "<52>"   : ['ctrl','4'],
    "<53>"   : ['ctrl','5'],
    "<54>"   : ['ctrl','6'],
    "<55>"   : ['ctrl','7'],
    "<56>"   : ['ctrl','8'],
    "<57>"   : ['ctrl','9'],
    "~"    : ['shift', '`'],
    "!"    : ['shift', '1'],
    "@"    : ['shift', '2'],
    "#"    : ['shift', '3'],
    "$"    : ['shift', '4'],
    "%"    : ['shift', '5'],
    "^"    : ['shift', '6'],
    "*"    : ['shift', '7'],
    "("    : ['shift', '8'],
    ")"    : ['shift', '9'],
    "_"    : ['shift', '-'],
    "+"    : ['shift', '='],
    ":"    : ['shift', ';'],
    "\'"   : ['shift', "'"],
    "<"    : ['shift', ","],
    "{"    : ['shift', "["],
    "}"    : ['shift', "]"],
    "|"    : ['shift', "\\"],
    "?"    : ['shift', "/"],
}

    def pressed(self,key):
        # if self.subFunctionDead:
        #     return True
        # self.keyPressReset = time.time()
        # try:
        #     self.recordKey.append("{}".format(key.char))
        # except:
        #     self.recordKey.append("{}".format(key))
        # print(self.recordKey)
        print(key)
        # print(key)
        if str(key) == "<105>":
            self.keyValue = 2
        elif str(key) == "Key.enter":
            self.keyValue = 3
        elif str(key) == "<102>":
            self.keyValue = 4
        elif str(key) == "<100>":
            self.keyValue = 5
        elif str(key) == "<105>":
            self.keyValue = 6
        elif str(key) == "<105>":
            self.keyValue = 7

        # elif str(key) == "1":
        # 	self.keyValue = 0
        # 	self.terminate()
        # self.recordKey = []
        # if len(self.recordKey) == 2:
        #     # print("recordKey",self.recordKey[0])
        #     if self.recordKey[0] == "Key.ctrl_l" or self.recordKey[0] == "Key.ctrl_r":
        #         # print("---------------------")
        #         if self.recordKey[1] in self.keyboard_key_dict.keys():
        #             # print(key)
        #             # print("The recordKey is " + str(self.keyboard_key_dict[self.recordKey[1]]))
        #             # print("Record the shortcut key.")
        #             self.recordKey[1] = copy.copy(self.keyboard_key_dict[self.recordKey[1]][1])

        #     elif self.recordKey[0] == "Key.shift" or self.recordKey[0] == "Key.shift_r":
        #         # print("+++++++++++++++++++=")
        #         if self.recordKey[1] in self.keyboard_key_dict.keys():
        #             # print("The recordKey is " + str(self.keyboard_key_dict[self.recordKey[1]]))
        #             # print("Record the shortcut key.")
        #             self.recordKey[1] = copy.copy(self.keyboard_key_dict[self.recordKey[1]][1])

        #     if self.shortcutFlag == False:
        #         # print("call target functions, not finished yet.")
        #             # else:
        #             #     # print(type(self.recordKey[0]))
        #             #     print("The recordKey is " + self.recordKey[0] + " + " + self.recordKey[1])
        #             #     print("Record the shortcut key.")
        #             #     print("sssssssssssssssssssssss")
        #             tem = self.recordKey[0] + self.recordKey[1]
        #             if tem in self.recordedshortcut.keys():
        #                 print(self.recordedshortcut[tem])
        #                 self.__status = self.recordedshortcut[tem] # Change status if user triggered a shortcut
        

    # def released(self,key):
    #     if self.subFunctionDead:
    #         return True
    #     self.keyPressReset = time.time()
    #     try:
    #         tem = str(key.char)
    #     except:
    #         tem = str(key)
            
    #     if tem in self.keyboard_key_dict.keys():
    #         tem=self.keyboard_key_dict[tem][1]
            
    #     if self.shortcutFlag and len(self.recordKey) == 2: # record shortcut
    #         if len(list(self.recordedshortcut.keys())) == 0:
    #             self.recordedshortcut[self.recordKey[0] + self.recordKey[1]] = 2
    #         else:
    #             if (self.recordKey[0] + self.recordKey[1]) not in self.recordedshortcut.keys():
    #                 self.recordedshortcut[self.recordKey[0] + self.recordKey[1]] = \
    #                     self.recordedshortcut[list(self.recordedshortcut.keys())[-1]] + 1
    #         # print(self.recordedshortcut)
    #         self.shortcutFlag = False
        
    #     # print("Released!!!",self.recordKey)
    #     # try:
    #     #     self.recordKey.remove("{}".format(key.char))
    #     # except:
    #     if len(self.recordKey) > 0:
    #         try:
    #             self.recordKey.remove("{}".format(tem))
    #         except:
    #             self.recordKey.clear()
        
        # if time.time() - self.timeIntervalStart > 10.0:
        #     if self.activeFlag == -1: # check if main thread is active, if not, kill sub thread
        #         self.subFunctionDead = True
        #         self.__status = -1
        #         self.recordKey.clear()
        #         return False
        #     else:
        #         self.activeFlag = -1
        #         self.timeIntervalStart = time.time()
        # if key == pynput.keyboard.Key.esc:
        #     return False

        
    def StartListener(self) -> None:

        if self.__status == -1:
            self.terminate()
            self.keyPressed = pynput.keyboard.Listener(on_press=self.pressed)
            
        self.__status = 1
        self.keyPressed.start()
        self.timeIntervalStart = time.time()
        self.begin = time.time() - 5
        self.keyPressReset = time.time()
        self.recordKey = []
        # self.subFunctionDead = False

    def terminate(self) -> None:
        self.keyPressed.stop()

    def keyGet(self) -> str:
        tem = self.keyValue
        self.keyValue = -1
        return tem


t = eventKeyboard()
t.StartListener()

tiger = 3.94
IV4H = 2.95
IV4DH = 3.24
hunter = 2.35
centurion = 2.57
T28 = 6.67
crusader = 2.57
IS_2 = 4.6
tiger1 = 4.05

while True:
    # 按下 "9" 键并增加一些延迟
    time.sleep(1/60)
    kkey = t.keyGet()
    if kkey == 2:
        print("!!!!!!!!!!!")
        # time.sleep(IV4DH)
        # keyboard.press('9')
        # time.sleep(0.035)  # 可以根据需要调整延迟时间
        # keyboard.release('9')
    elif kkey == 3:
        keyboard.press('Key.enter')
        time.sleep(0.035)  # 可以根据需要调整延迟时间
        keyboard.release('Key.enter')
    elif kkey == 4:
        keyboard.press('Key.right')
        time.sleep(0.035)  # 可以根据需要调整延迟时间
        keyboard.release('Key.right')
    elif kkey == 5:
        keyboard.press('Key.left')
        time.sleep(0.035)  # 可以根据需要调整延迟时间
        keyboard.release('Key.left')
    elif kkey == 6:
        keyboard.press('Key.up')
        time.sleep(0.035)  # 可以根据需要调整延迟时间
        keyboard.release('Key.up')
    elif kkey == 7:
        keyboard.press('Key.down')
        time.sleep(0.035)  # 可以根据需要调整延迟时间
        keyboard.release('Key.down')
    elif kkey == 8:
        keyboard.press('Key.left')
        time.sleep(0.035)  # 可以根据需要调整延迟时间
        keyboard.release('Key.left')
