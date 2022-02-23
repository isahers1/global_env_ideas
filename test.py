class A:
    stuff = []
    other = "here"

    def __init__(self):
        self.stuff.append(5)
        newB = self.B()
    
    def addElement(self, elem):
        self.stuff.append(elem)
    
    def getStuff(self):
        return self.stuff

    def __repr__(self):
        print("YAY!")

    class B:
        def __init__(self):
            A.addElement(A,5)
            print(A.getStuff(A))
         
        def anything(self):
            print(A.other)
        
        def stuff(self):
            print(A.stuff)
        
        def __mul__(self,other):
            print(A.stuff)


d = {5:'a',3:'b'}
print((d.keys()))


