import copy

exec(compile(source=open('classes.py').read(), filename='classes.py', mode='exec'))


g = group('G','*')


# add elements a,b to group

g.newElement('a')
g.newElement('b')
g.mulElements('a','b')
g.mulElements('a*b','a')
g.mulElements('(a*b)*a','a')
print(g.elements) #- this works, yay!


lh = group.equation([g.element('x',g),'*',g.element('x',g)],g)
rh = group.equation([g.getIdentity()],g)
statement = group.statement(lh,rh,g)

p1 = group.forall([g.element('x',g)],statement,g)
# print(p1) # this works!
g.addGroupProperty(p1, "p1")

#print(g.groupProperties['p1'].access({'x':'a'})) # this works too!

#print(g.elementProperties)
