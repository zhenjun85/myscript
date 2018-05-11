import re
import sys

INPUT_TYPE_MOTION = 1
INPUT_TYPE_KEY = 2

ACTION_DOWN = '0'
ACTION_UP = '1'
ACTION_MOVE = '2'

class InputEvent:
    def __init__(self, eventTime = 0, action = 0, x = 0, y = 0, keycode = 0, inputType = 0):
        self.eventTime = eventTime
        self.action = action
        self.x = x
        self.y = y
        self.keycode = keycode
        self.inputType = inputType

    def __str__(self):
        if self.inputType == INPUT_TYPE_KEY:
            return 'KeyEvent time=%s Action=%s keycode=%d' % (self.eventTime, self.action, self.keycode)
        else:
            return 'MotionEvent time=%s Action=%s x=%d y=%d' % (self.eventTime, self.action, self.x, self.y)



def parseLog(fileName):
    eventTime = 0
    action = 0
    posX = 0
    posY = 0
    inputEvents = []
    motionTime = re.compile(r'.*InputDispatcher:.*notifyMotion - eventTime=(\d+).*action=0x(\d)')
    motionPos = re.compile(r'.*InputDispatcher:.*x=(\d+).*y=(\d+)')

    keyTime = re.compile(r'.*InputDispatcher:.*notifyKey - eventTime=(\d+).*action=0x(\d).*keyCode=(\w+)')

    motionEventPos = False
    with open(fileName) as file:
        for line in file.readlines():
            #print(line)

            #parse Motion Event
            motionEventMatch = motionTime.match(line)
            if motionEventMatch:
                eventTime = motionEventMatch.group(1)
                action = motionEventMatch.group(2)
                motionEventPos = True
            if motionEventPos:
                matchPos = motionPos.match(line)
                if matchPos:
                    posX = int(matchPos.group(1))
                    posY = int(matchPos.group(2))
                    inputEvents.append(InputEvent(eventTime=int(eventTime), action=action, x = posX, y = posY, inputType=INPUT_TYPE_MOTION))
                    motionEventPos = False

            #parse Key Event
            keyEventMatch = keyTime.match(line)
            if keyEventMatch:
                inputEvents.append(InputEvent(eventTime=int(keyEventMatch.group(1)),
                        action=keyEventMatch.group(2), keycode=int(keyEventMatch.group(3), 16), inputType=INPUT_TYPE_KEY))

    return inputEvents




#exit(1)

def genShellCommand(inputEvents):
    downTime = None
    lastEventUpTime = None
    lastEvent = None
    startTracing = False
    isMoving = False
    firstAction = True

    shellCommands = []

    for i in inputEvents:
        #print(i)
        if i.action == ACTION_DOWN:
            if firstAction:
                firstAction = False
            else:
                sleepTime = (i.eventTime - lastEventUpTime) / 1000000000
                if sleepTime == 0:
                    sleepTime = 1
                shellcommand = 'sleep %d' % sleepTime
                #print(shellcommand)
                shellCommands.append(shellcommand)

            startTracing = True
            downTime = i.eventTime
            lastEvent = i
        elif i.action == ACTION_UP:
            costTime = i.eventTime - downTime
            lastEventUpTime = i.eventTime
            #print('costTime= %s ms' % (costTime / 1000000))
            if i.inputType == INPUT_TYPE_KEY:
                shellcommand = 'adb shell input keyevent %d' % i.keycode
                #print(shellcommand)
                shellCommands.append(shellcommand)
                #print('adb shell input keyevent %d' % i.keycode)
            elif isMoving:
                shellcommand = 'adb shell input swipe %d %d %d %d %d' % (lastEvent.x, lastEvent.y, i.x, i.y, costTime / 1000000)
                #print(shellcommand)
                shellCommands.append(shellcommand)
            else:
                shellcommand = 'adb shell input tap %d %d' % (i.x, i.y)
                #print(shellcommand)
                shellCommands.append(shellcommand)

            startTracing = False
            isMoving = False
        elif i.action == ACTION_MOVE:
            isMoving = True
    return shellCommands




def main():

    if sys.argv.__len__() == 2:
        inputEvents = parseLog(sys.argv[1])
        commands = genShellCommand(inputEvents)
        print('The shell commands is:')
        for i in commands:
            print(i)
    else:
        print('Wrong useage, please input the log path')
if __name__ == '__main__':
    main()
