class FileSystem:
    def convert_to(self):
        print("I am converting to this file system")

    def dynamic_partition(self):
        print("I am changing to a dynamic partition")

    def status(self):
        print("I am currently displaying the status of the system")

    def virtual(self):
        print("I am now a virtual file system")

# Create a class called NTFS which inherits from FileSystem
class NTFS(FileSystem):

    # Override method
    def convert_to(self):
        super().convert_to() # Runs the convert_to method of FileSystem
        print("I have converted to NTFS filesystem")

def main():

    myFileSystem = FileSystem()
    myFileSystem.convert_to()

    myFileSystem2 = NTFS()
    myFileSystem2.convert_to()
    myFileSystem2.status()
    myFileSystem2.virtual()

main()
