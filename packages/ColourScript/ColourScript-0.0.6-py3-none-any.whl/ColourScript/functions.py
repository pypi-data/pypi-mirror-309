from time import sleep

class text:
    def __init__(self, message):
        self.message = message
        print(self.message)

    def reset(self):
        print('\033[0;0m')
    def plain(self):
        print('\033[0;0m' + str(self))
    def red(self):
        print('\033[31m' + str(self))
    def green(self):
        print('\033[32m' + str(self))
    def yellow(self):
        print('\033[33m' + str(self))
    def blue(self):
        print('\033[34m' + str(self))
    def purple(self):
        print('\033[35m' + str(self))
    def cyan(self):
        print('\033[36m' + str(self))
    def white(self):
        print('\033[38m' + str(self))
    def black(self):
        print('\033[30m' + str(self))
    def customcode(self, code):
        print(f"\033[{code}m"+ str(self))
    def bold(self):
        print('\033[1m'+str(self))
    def underline(self):
        print('\033[4m'+str(self))
    def italic(self):
        print('\033[3m'+str(self))
    def strikethrough(self):
        print('\033[9m'+str(self))
    def orange(self):
        print('\033[38;5;202m' + str(self))

class pause:
    def __init__(self):
        sleep(int(self) / 1000)
    def secs(self):
        sleep(int(self))
    def mins(self):
        sleep(int(self) * 60)
