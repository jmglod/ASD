# podwójnie wiązana i przy okazji zapętlona
import psutil
import os
class Element:
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def destroy(self):
        iterator = self.head
        while iterator is not None:
            temp = iterator
            iterator = iterator.next
            temp.data = None
            temp.next = None
            temp.prev = None
        self.head = None
        self.tail = None

    def add(self, data):
        if self.head:
            if self.tail:
                second = self.head
                self.head = Element(data, second, self.tail)
                self.tail.next = self.head
                second.prev = self.head
            else:
                self.tail = self.head
                self.head = Element(data)
                self.head.next = self.tail
                self.head.prev = self.tail
                self.tail.next = self.head
                self.tail.prev = self.head
        else:
            self.head = Element(data)
            self.head.prev = self.head
            self.head.next = self.head

    def append(self, data):
        if self.head:
            if self.tail:
                temp = self.tail
                self.tail = Element(data, self.head, temp)
                self.head.prev = self.tail
                temp.next = self.tail
            else:
                self.tail = Element(data)
                self.head.prev = self.tail
                self.head.next = self.tail
                self.tail.prev = self.head
                self.tail.next = self.head

        else:
            self.head = Element(data)
            self.head.prev = self.head
            self.head.next = self.head


    def remove(self): # usuwanie z początku
        if self.head and self.tail:
            if self.head.next != self.tail:
                self.head = self.head.next
                self.tail.next = self.head
                self.head.prev = self.tail
                if self.tail == self.head:
                    self.tail.next = None
                    self.tail.data = None
                    self.tail.prev = None
            else:
                self.head = None
                self.tail = None
        else:
            self.head = None
            self.tail = None

    def remove_end(self): # usuwanie z końca
        if self.head and self.tail:
            if self.head.next != self.tail:
                self.tail = self.tail.prev
                self.head.prev = self.tail
                self.tail.next = self.head
                if self.tail == self.head:
                    self.tail.next = None
                    self.tail.data = None
                    self.tail.prev = None
            else:
                self.head = None
                self.tail = None
        else:
            self.head = None
            self.tail = None

    def is_empty(self):
        if self.head or self.tail:
            return False
        else:
            return True

    def length(self):
        if self.head:
            if self.tail:
                counter = 2
                iterator = self.head
                iterator = iterator.next
                while iterator.next != self.head:
                    iterator = iterator.next
                    counter += 1
                return counter
            else:
                return 1
        else:
            return 0

    def get(self):
        return self.head.data

    def display(self):
        if self.head:
            iterator = self.head
            print("->", iterator.data)
            iterator = iterator.next
            while iterator.next != self.head:
                print("->", iterator.data)
                iterator = iterator.next
            print("->", iterator.data)


lista = [('AGH', 'Kraków', 1919),
         ('UJ', 'Kraków', 1364),
         ('PW', 'Warszawa', 1915),
         ('UW', 'Warszawa', 1915),
         ('UP', 'Poznań', 1919),
         ('PG', 'Gdańsk', 1945)]

if __name__ == '__main__':
    link = LinkedList()

    # for el in lista[:3]:
    #     link.append(el)
    # for el in lista[3:]:
    #     link.add(el)
    #
    # link.display()
    # print(link.length())
    # link.remove()
    # print(link.get())
    # link.remove_end()
    # link.display()
    # link.destroy()
    # print(link.is_empty())
    # link.remove()
    # link.append(lista[0])
    # link.remove_end()
    # print(link.is_empty())


    # print(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024)
    # for i in range(300000):
    #     for el in lista:
    #         link.append(el)
    #         link.append(i)
    # print(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024)
    # link.destroy()
    # print(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024)

    link.append(1)
    link.add(1)
    link.append(1)
    print(link.length())
    link.remove()
    print(link.length())
    link.remove()
    print(link.length())
    link.remove()
    print(link.length())
    link.remove()

