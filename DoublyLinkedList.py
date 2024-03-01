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
    def addAfter(self, node, data_to_add):
        node_to_add = Node(data_to_add)
        node_to_add.prev = node
        node_to_add.next = node.next
        node.next.prev = node_to_add
        node.next = node_to_add
        if node is self.tail:
            node_to_add.next = self.head
            self.head.prev = node_to_add
            self.tail = node_to_add
        return node_to_add

        

    def changenode(self, node, node_to_change):
        if node_to_change is self.head:
            self.head = node_to_change.next
            node_to_change.next.prev = self.tail
            self.tail.next = self.head
        elif node_to_change is self.tail:
            self.tail = node_to_change.prev
            node_to_change.prev.next = self.head
            self.head.prev = self.tail
        else:
            node_to_change.prev.next = node_to_change.next
            node_to_change.next.prev = node_to_change.prev
                
        node_to_change.prev = node
        node_to_change.next = node.next
        node.next.prev = node_to_change
        node.next = node_to_change
        if node is self.tail:
            node_to_change.next = self.head
            self.head.prev = node_to_change
            self.tail = node_to_change



    def delete(self,node):  
        if node is self.head:
            self.head = node.next
            node.next.prev = self.tail
            self.tail.next = self.head
            del node
        elif node is self.tail:
            self.tail = node.prev
            node.prev.next = self.head
            self.head.prev = self.tail
            del node
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            del node

