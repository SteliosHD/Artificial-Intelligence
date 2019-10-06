#!python
# Checks if a string containg (),{},[] is balanced
#   using the stack impemanted in Mystack
import MyStack as mst

left_brackets = ['(', '[', '{']
right_brackets = [')', ']', '}']

def check(_string):
    """
        A function that checks if an expression(string) that contains '(),{},[]'
        is well balenced and prints an answer based on that.
    """
    checkStack = mst.myStack()
    for ch in _string:  # loop the whole string
        if ch in left_brackets:     # push until you find a right bracket and only push brackets
            checkStack.push(ch)
        elif ch in right_brackets:  # found a right bracket if stack is empty string is left-unbalanced
            try :
                checkStack.pop()
            except IndexError:      # except IndexError stack is empty
                print'expression : ', _string,'left-unbalanced'
                break
    else:   # only after not breaking the loop
        if checkStack.isEmpty(): # if the stack is empty string then is balanced
            print 'expression : ', _string,' is balanced'
        else:
            print 'expression : ', _string,' is right-unbalanced' # else the string is right-unbalanced

""" run as main for testing """
if __name__=='__main__':
    check('()')
    check('({[]})')
    check(')')
    check('(')
    check('()[]')
    check('([)')
    check('(])')
    check("{a+x*[(a/x-3)-4]+2x+4}")
    check("{a+x*(a/x-3)-4]+2x+4}")
