#!python
# Instructions
# A stack S of items of type T is a sequence of
# items of type T on which the following
# operations can be defined:
# 1. Initialize the stack S to be the empty stack.
# 2. Determine whether or not the stack S is empty.
# 3. Determine whether or not the stack S is full.
# 4. Push a new item onto the top of stack S.
# 5. If S is nonempty, pop an item from the top of
# stack S.



class myStack:
    """
        Implemantation of Stack using built-in list
        Basic methods : isEmpty, push, pop,
        Extra methods : top, __len__(object method override), isFull

    """
    def __init__(self):
        """ Create an empty stack using an empty list"""
        self.items = []

    def isEmpty(self):
        """Return True if the stack is empty else return False"""
        return len(self.items) == 0

    def push(self,x):
        """ Add the element x on the top of the stack"""
        self.items.append(x)    # add x at the end of the list

    def pop(self):
        """ Removes the top item of the stack or raises an exception if stack is empty"""
        if not self.items:
            raise IndexError('pop from empty Stack')
        return self.items.pop() # pop refers to list.pop()

    # ***************************************************************
    # These methods are optional and are provided for completeness  *
    # ***************************************************************
    def top(self):
        """ Returns the top item without removing it or raise an exception if stack is empty"""
        if not self.items:
            raise IndexError('Stack is empty')
        return self.items[-1] # pop refers to list.pop()

    def __len__(self):
        """ Returns the length(number of elements) of the stack"""
        return (len(self.items))    # using len method of list object

    def isFull(self):
        """ Stack based on lists is never full added only because of the Instructions of the pdf"""
        return False




"""
    The function that checks for balanced expressions
"""
def check(_string):
     # opening delimeters (must have same order in left and right brackets)
    left_brackets = '([{'
     # closing delimeters (must have same order in left and right brackets)
    right_brackets = ')]}'

    """
        A function that checks if an expression(string) that contains '(),{},[]'
        is well balenced and prints an answer based on that.
    """
    checkStack = myStack()
    # loop the whole string if string is empty we consider it as balanced
    for ch in _string:
        # push until you find a right bracket and only push brackets
        if ch in left_brackets:
            checkStack.push(ch)
        elif ch in right_brackets:
            # if stack is empty string is left-unbalanced
            if checkStack.isEmpty():
                print'expression : ', _string,'left-unbalanced none opening delimeter found'
                return False
            # check if it is the same type of delimeter
            if right_brackets.index(ch)!= left_brackets.index(checkStack.pop()):
                print'expression : ', _string,'has a mismatched delimeter '
                return False
    # if the stack is empty string then is balanced else found no delimeter
    if checkStack.isEmpty():
        print 'expression : ', _string,' is balanced'
        return True
    else:
        print 'expression : ', _string,'found no right delimeter to match'
        return False






""" run as main for testing """
if __name__=='__main__':
    print "*"*60
    print "Test for the stack"
    print "*"*60
    adtStack = myStack()
    print 'length is :',len(adtStack)
    print'pushing 1'
    adtStack.push(1)
    print 'length is :',len(adtStack)
    print'pop : ',adtStack.pop()
    print'stack is empty : ', adtStack.isEmpty()
    for el in [1,2,3,4,(1,2),[(1,2),{"one":1}],[1,2,"string"]]:
        print'pushing : ',el
        adtStack.push(el)
        print'top :',adtStack.top()

    for el in range(len(adtStack)):
        print'pop : ',adtStack.pop()
    print'stack is full :', adtStack.isFull()
    print'stack is empty : ', adtStack.isEmpty()
    #print'pop : '
    #adtStack.pop()
    print "*"*60
    print "Test for the balanced expressions"
    print "*"*60
    check('')
    check('()')
    check('({[]})')
    check(')')
    check('(')
    check('()[]')
    check('([)')
    check('(])')
    check('(]')
    check('((((()')
    check("{a+x*[(a/x-3)-4]+2x+4}")
    check("{a+x*(a/x-3)-4]+2x+4}")
