class Network:

    def cable(self):
        print("I am the cable")

    def router(self):
        print("I am the router")

    def switch(self):
        print("I am the switch")

    def wifi(self):
        print("I am wireless")

class TokenRing(Network):

    def cable(self):
        print("I am a token ring network cable")

    def router(self):
        print("I am the token ring router")

class Ethernet(Network):
    def cable(self):
        print("I am an ethernet cable")

    def router(self):
        print("I am an ethernet router")

    def wifi(self):
        print("I am wifi for mac only")

def main():

    windows = TokenRing()
    mac = Ethernet()

    for obj in (windows, mac):
    # '(windows, mac)' is the list of objects to iterate in
        obj.cable()
        obj.router()
        obj.wifi()
        print()

main()
