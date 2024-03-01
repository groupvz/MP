from mutagen.mp3 import MP3

#Class to store the song's information
class Song:
    def __init__(self,file):
        self.path = str(file)
        audio = MP3(file)
        self.title = str(audio["TIT2"])
        self.artist = str(audio["TPE1"])
        self.album = str(audio["TALB"])
        self.duration = audio.info.length

#Each song is a node that contains data and a pointer to the next and previous node
class Node:
    def __init__(self,data):
        self.data = Song(data)
        self.next = None
        self.prev = None

#Doubly linked list to store the songs
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None 
        self.lenght = 0 

    def copy(self):
        new_list = DoublyLinkedList()
        current = self.head
        while current:
            new_list.addToTail(current.data.path)
            current = current.next
        return new_list      

    def addToTail(self, val): 
        new_node = Node(val)
        if not self.head:
            self.head = new_node
            self.tail = self.head
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.lenght += 1 