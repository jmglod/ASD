class Element:
    def __init__(self, data, ptr=None):
        self.data = data
        self.next = ptr


class LinkedList:
    def __init__(self):
        self.head = None

    def destroy(self):
        self.head = None

    def add(self, data):
        if self.head:
            second = self.head
            self.head = Element(data, second)
        else:
            self.head = Element(data)

    def append(self, data):
        if self.head is None:
            self.head = Element(data)
        else:
            iterator = self.head
            while iterator.next:
                iterator = iterator.next
            # iterator.next == None
            iterator.next = Element(data)

    def remove(self):
        if self.head:
            self.head = self.head.next
        else:
            self.head = None
        # second = self.head.next
        # self.head = second

    def remove_end(self):
        if self.head:
            if self.head.next:
                iterator = self.head
                prev = None
                while iterator.next:
                    prev = iterator
                    iterator = iterator.next
                if prev:
                    prev.next = None

            else:
                self.head = None

    def is_empty(self):
        if self.head:
            return False
        else:
            return True

    def length(self):
        if self.head:
            counter = 1
            iterator = self.head
            while iterator.next:
                iterator = iterator.next
                counter += 1
            return counter
        else:
            return 0

    def get(self):
        return self.head.data

    def display(self):
        if self.head:
            iterator = self.head
            while iterator.next is not None:
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

    for el in lista[:3]:
        link.append(el)
    for el in lista[3:]:
        link.add(el)

    link.display()
    link.remove()
    print(link.get())
    link.remove_end()
    link.display()
    link.destroy()
    print(link.is_empty())
    link.remove()
    link.append(lista[0])
    link.remove_end()
    print(link.is_empty())
