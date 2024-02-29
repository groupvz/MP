from mutagen.mp3 import MP3

class Song:
    def __init__(self,file):
        self.path = str(file)
        audio = MP3(file)
        self.title = str(audio["TIT2"])
        self.artist = str(audio["TPE1"])
        self.album = str(audio["TALB"])
        self.duration = audio.info.length
class Node:
    def __init__(self,data):
        self.data = Song(data)
        self.next = None
        self.prev = None

class List_song:
    def __init__(self):
        self.head = None
        self.tail = None 
        self.lenght = 0 

    def copy(self):
        new_list = List_song()
        current = self.head
        while current:
            new_list.addToTail(current.data.path)
            current = current.next
        return new_list      

    def addToHead(self, val): # thêm một nút có giá trị x vào đầu .
        new_node = Node(val)  
        if not self.head:
            self.head = new_node
            self.tail = self.head
        else:
            new_node.next =self.head
            self.head = new_node
            self.head.next.prev = new_node
        self.lenght += 1

    def addToTail(self, val): # thêm một nút có giá trị x vào cuối .
        new_node = Node(val)
        if not self.head:
            self.head = new_node
            self.tail = self.head
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.lenght += 1
    def addAfter(self, node, node_to_add):
        node_to_add.next = node.next
        node_to_add.prev = node
        node.next = node_to_add
        

    def changee(self, node, node_to_change):
        # Check if the node_to_change is the same as the node or if either node is None
        if node_to_change is node or not node or not node_to_change:
            return

        # Disconnect node_to_change from its current position
        if node_to_change.prev:
            node_to_change.prev.next = node_to_change.next
        if node_to_change.next:
            node_to_change.next.prev = node_to_change.prev

        # Update node_to_change's pointers to insert it after node
        node_to_change.next = node.next
        node_to_change.prev = node

        # Update node's pointers to link to node_to_change
        if node.next:
            node.next.prev = node_to_change
        node.next = node_to_change 

    def deleteAfter(self,node):  
        
        if  node is self.head:
            self.head == node.next
            del node
             
        elif node is self.tail:
            self.tail == node.prev
            del node
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            del node
             