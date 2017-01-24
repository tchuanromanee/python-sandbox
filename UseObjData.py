class Files:

    def __init__(self, ftype = 'text'): # filetype isinitialized as  text file
        self._ftype='txt'

    def move(self):
        print("file is moving")

    def copy(self):
        print("file is being copied")

    def delete(self):
        print("file is being removed")

    def set_ftype(self, ftype): # Accessor method
        self._ftype = ftype

    def get_ftype(self):
        return self._ftype

def main():
    execs = Files()
    execs.move()
    execs.copy()
    print(execs.get_ftype())

    exec.set_ftype('mov')
    print(execs.get_ftype())
main()
