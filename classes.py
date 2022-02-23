"""
THINGS TO DO:

1. For all elimination
2. Add statement array to group? Set of equalities we can pick from at any time?
3. What other information needs to be stored the whole time?
4. Foreground (element names) vs background/concrete (all elements have inverses)?

"""
import copy

class group:
    # TRUTHS for all classes - need to add more here
    identity_identifier = 'e'
    elements = {}
    groupProperties = {} 
    elementProperties = {} # make it easy to change sublevels (i.e. assume something, reach a contradiction, then remove this assumption from the group)
    binaryOperator = ""
    groupName = ""

    def __init__(self, name, binOp, additionalGroupProperties = None, additionalElementProperties = None):
        self.groupName = name
        self.binaryOperator = binOp
        self.elements.update({self.identity_identifier:self.identity(self.identity_identifier,self)}) # 'e' for now - maybe give user ability to change later?
        if additionalGroupProperties != None:
            self.groupProperties.update(additionalGroupProperties)
        if additionalElementProperties != None:
            self.elementProperties.update(additionalElementProperties)

    # basic functions

    def __repr__(self):
        return "group(" + self.groupName + ")"
    def __eq__(self,other):
        return self.groupName == other.groupName
    def __mul__(self,other): # group cartesian product. Worry about this later
        newName = self.groupName + "x" + other.groupName
        newProperties = list(set(self.properties) & set(other.properties))
        return group(newName, [self.binaryOperator,other.binaryOperator], newProperties)

    # access functions - just for testing, will remove later

    def getIdentity(self):
        return self.elements[self.identity_identifier]
    
    def getName(self):
        return self.groupName
    
    def getBinOp(self):
        return self.binaryOperator
    
    def getElements(self):
        return self.elements

    def getProperties(self):
        return self.properties

    # group functions

    # declare new element in group with elementName
    def newElement(self,elementName):
        if elementName not in self.elements:
            self.elements.update({elementName:self.element(elementName,self)})
        else:
            print("Sorry, that element already exists!")

    # create new element that is elem1 operated on with elem2
    def mulElements(self, elem1, elem2): # should this return an equation?
        if elem1 == self.identity_identifier or elem2 == self.identity_identifier:
            print("Sorry, multiplying by the identity doesn't do anything!")
        else:
            try:
                gelem1 = self.elements[elem1]
                gelem2 = self.elements[elem2]
                result = gelem1 * gelem2
                self.elements.update({result:self.element(result,self)}) # is this the right?
            except:
                print("Sorry, one or both of these elements are not in the group!")

    def addGroupProperty(self, property, propertyName):
        self.groupProperties[propertyName] = property

    def addElementProperty(self, property, elementName):
        if elementName in self.elements or elementName == self.identity_identifier:
            self.elementProperties[elementName] = property
        else:
            print("That element doesn't exist!")

    class element:
        def __init__(self, elementName, g): # passing g might be the only way to go :(
            self.elementName = elementName
            self.parentGroup = g # make this a list of parent groups, elements can be in multiple groups
        def __repr__(self):
            return self.elementName
        def __eq__(self,other):
            return self.elementName == other.elementName
        def __mul__(self,other): # use this function in the mulElements from Group class above?
            binOp = self.parentGroup.binaryOperator
            if binOp in other.elementName and '(' != other.elementName[0]:
                return self.elementName + binOp + "(" +other.elementName + ")"
            elif binOp in self.elementName and ')' != self.elementName[-1]:
                return "(" + self.elementName + ")" + binOp + other.elementName
            else:
                return self.elementName + binOp + other.elementName
        def fullDescription(self):
            return self.elementName + " in group " + self.parentGroup.groupName
        def exp(self, pow):
            return self ** pow
    
    class identity(element):
        def __init__(self, elementName, g):
            super().__init__(elementName, g)
            pg = self.parentGroup
            lh = group.equation([group.element('x',pg),'*',self],pg)
            rh = group.equation([group.element('x',pg)],pg)
            statement = group.statement(lh,rh,pg)
            idnty = group.forall([group.element('x',pg)],statement,pg)
            pg.addElementProperty(idnty,elementName)

    class generator(element):
        def __init__(self, elementName, g):
            super().__init__(elementName, g)
            pg = self.parentGroup
            lh = group.equation([group.element('x',pg)],pg)
            rh = group.equation([self,'**',1],pg) # need to change 1 to be there exists an integer k
            statement = group.statement(lh,rh,pg) # also how can I add '**' as an operator?
            gnrtr = group.forall([group.element('x',pg)],statement,pg)
            pg.addElementProperty(gnrtr, elementName)

    class equation: # ['a','*','b'] is a * b
        def __init__(self,sequence, group):
            self.expr = sequence # check for invalid equations?
            self.parentGroup = group
        def __repr__(self):
            repr = ""
            for elem in self.expr:
                repr += str(elem)
            return repr
        def replace(self, dict): # take x=y, replace x with a, to return a=y
            selfcopy = copy.deepcopy(self)
            for i in range(len(selfcopy.expr)):
                for elem1 in dict:
                    if isinstance(selfcopy.expr[i],group.element) and selfcopy.expr[i] == group.element(elem1,self.parentGroup):
                        selfcopy.expr[i] = dict[elem1]
            return selfcopy

    class statement: # these are equalities. Are there other types of properties? >, <, /=, etc.
        def __init__(self, lhside, rhside, group):
            self.leftHandSide = lhside
            self.rightHandSide = rhside
            self.bothSides = [self.leftHandSide,self.rightHandSide] # store both sides to quickly check if x=y is the same as y=x
            self.parentGroup = group
        def __repr__(self):
            return str(self.leftHandSide) + " = " + str(self.rightHandSide)
        def __eq__(self, other):
            return (self.leftHandSide == other.leftHandSide) and (self.rightHandSide == other.rightHandSide)
        def replace(self, replaceDict):
            for x in replaceDict:
                if group.element(x,self.parentGroup) in self.leftHandSide.expr:
                    self.leftHandSide = self.leftHandSide.replace({x:group.element(replaceDict[x],self.parentGroup)})
                if group.element(x,self.parentGroup) in self.rightHandSide.expr:
                    self.rightHandSide = self.rightHandSide.replace({x:group.element(replaceDict[x],self.parentGroup)})
            return group.statement(self.leftHandSide,self.rightHandSide, self.parentGroup)

    class forall:
        def __init__(self, elements, statement, group): # i don't want to pass groupName here
            self.elems = elements
            self.expr = statement 
            self.group = group
        def __repr__(self):
            return 'forall(' + str(self.elems) + ' in ' + group.getName(self.group) + ', ' + str(self.expr) + ')'
        def __eq__(self,other):
            return self.elems == other.elems and self.group == other.group and self.expr == other.expr
        #
        def access(self, replaceDict): # {'x':'a','y':'b', etc.} replace 'x' with 'y', then get access to the equation
            accesscopy = copy.deepcopy(self)
            return accesscopy.expr.replace(replaceDict)

    class thereexists:
        def __init__(self, elements, statement, group): # i don't want to pass groupName here
            self.elems = elements
            self.expr = statement 
            self.group = group
            self.utilizedBy = None
        def __repr__(self):
            return 'there exists(' + str(self.elems) + ' in ' + group.getName(self.group) + ', ' + str(self.expr) + ')'
        def __eq__(self,other):
            return self.elems == other.elems and self.group == other.group and self.expr == other.expr
        #
        def access(self, replaceDict): # {'x':'a','y':'b', etc.} replace 'x' with 'y', then get access to the equation
            if self.utilizedBy == None:
                accesscopy = copy.deepcopy(self)
                self.utilizedBy = list(replaceDict.keys())
                return accesscopy.expr.replace(replaceDict)
            else:
                print("There exists only applies once in your proof!")

"""
Notes:

1. Need to deal with cartesian product of groups
2. Implementing guard rails is difficult - take C++ approach?
3. Seperate identity and group element class? They have same properties, but
identity has some additional shortcuts that would be nice to have.
4. How can the relationship between elements and group be concrete?
5. CyclicGroup extends Group, identity extends groupElement, genereator extends groupElement?

"""