#!python
# Checks if a string containg (),{},[] is balanced
#   using the stack impemanted in Mystack
import MyStack as mst

 # opening delimeters (must have same order in left and right brackets)
left_brackets = '([{'
 # closing delimeters (must have same order in left and right brackets)
right_brackets = ')]}'

def check(_string):
    """
        A function that checks if an expression(string) that contains '(),{},[]'
        is well balenced and prints an answer based on that.
    """
    checkStack = mst.myStack()
    # loop the whole string
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
