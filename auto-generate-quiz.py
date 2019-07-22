#!- encoding = utf-8 -!

'''
Author: Dou Liyou
Program Time: 2017-07-14
Version: 1.0

Script using: 
'''

import random
import operateDocx
import datetime

'''
define a method called 'calculate' with 3 parameters: number1, number2 and expression.
the method calculate depend on the expression, this version only support '+' , '-'
other expression will return None
'''


def calculate(Operator, number1, number2):
    if Operator == '+':
        return number1 + number2
    if Operator == '-':
        return number1 - number2
    return -1


def cal(exp):
    if exp.__len__() == 3:
        return calculate(exp[0], exp[1], exp[2])
    if exp.__len__() == 5:
        tmpValue = calculate(exp[0], exp[2], exp[3])
        return calculate(exp[1], tmpValue, exp[4])


'''
this method is used to produce a random int which is between 'begin' and 'end'.

'''


def makeRandomInt(begin, end):
    if begin <= end:
        return random.randint(begin, end)
    else:
        return random.randint(end, begin)


'''
this method is used to produce a operator optionally. which should be '+' or '-'
'''


def makeRandomOper():
    """
    :return: the string of operator
    """
    exp = ['+', '-']
    index = random.randint(0, 1)
    return exp[index]


'''
this method can produce a list which contains one operator and two numbers.

'''


def generateExpression():
    exp = []  # list [operator, first, second]
    exp.append(makeRandomOper())
    exp.append(makeRandomInt(0, 99))
    # the second number need follow more critical rules by using new method
    # produceNum(givenNum,Oper,max)
    exp.append(produceNum(exp[1], exp[0], 199))
    if exp[0] == '+':
        return exp
    if exp[0] == '-':
        if exp[1] > exp[2]:
            return exp
        else:
            two = exp.pop(1)
            one = exp.pop(1)
            exp.append(one)
            exp.append(two)
            return exp


def generateThreeExp():
    exp = []
    exp.append(makeRandomOper())
    exp.append(makeRandomOper())
    exp.append(makeRandomInt(0, 99))
    exp.append(makeRandomInt(0, abs(99 - exp[2])))
    exp.append(makeRandomInt(0, abs(99 - exp[2] - exp[3])))
    if (exp[0] == '+') & (exp[1] == '+'):
        return exp
    else:
        if (exp[2] > exp[3]) & (exp[3] > exp[4]):
            testValue = cal(exp)
            if testValue < 0:
                exp[2] = exp[2] + abs(testValue)
                print(exp)
            return exp
        else:
            for i in range(2, 3):
                for j in range(i + 1, 5):
                    if exp[i] < exp[j]:
                        tmp = exp[i]
                        exp[i] = exp[j]
                        exp[j] = tmp
            # be sure the return value is negative number, modify the first number, confirm it's big enough.
            testValue = cal(exp)
            if testValue < 0:
                exp[2] = exp[2] + abs(testValue)
                print(exp)
            return exp


'''
this method format a expression to style which can be read by a pupil
'''


def formatExpression(exp, with_answer):
    exp_str = ''
    answer = cal(exp) if with_answer else ''
    if exp.__len__() == 3:
        exp_str = f'{exp[1]:3} {exp[0]} {exp[2]:3} = {answer:3}'

    if exp.__len__() == 5:
        exp_str = f'{exp[2]} {exp[0]} {exp[3]} {exp[1]} {exp[4]} = {answer}'
    return exp_str

'''
this method produce a quiz and return quiz as a list.
e.g: [[exp1,exp2,exp3],[res1,res2,res3]]
'''


def generateQuiz(amout):

    quiz = []
    expression = []
    expression_results = []
    quiz.append(expression)
    quiz.append(expression_results)

    for i in range(amout):
        # use this variable r to control 2 or 3 expression
        #        r = random.randint(0,1)
        r = 0
        if r == 0:
            exp = generateExpression()
        else:
            exp = generateThreeExp()
        fexp = formatExpression(exp, with_answer=False)
        fexp_result = formatExpression(exp, with_answer=True)
        expression.append(fexp)
        expression_results.append(fexp_result)
    return quiz


'''
this method produce the number which is useful in the expression,
e.g: give a 45 , then need a number which caculate with given one with add or minus, must not over 10
     1,2,3,4 ; 11,12,13,14 ; 21,22,23,24, 31,32,33,34; 41,42,43,44; 51,52,53,54;    
'''


def produceNum(givenNum, Oper, max):
    allow_carry = True
    nMax = max - givenNum
    if Oper == '+':
        if allow_carry:
            return makeRandomInt(0, max-givenNum)
        else:
            nList = list(str(nMax))
            length = len(nList)
            if length == 1:
                return makeRandomInt(0, nMax)
            elif length > 1:
                m = 0
                for n in nList:
                    m = m * 10 + makeRandomInt(0, int(n))
                return m
    if Oper == '-':



        if allow_carry:
            return makeRandomInt(givenNum, max)
        else:
            nList = list(str(givenNum))
            nLength = len(nList)
            mList = list(str(max))
            mLength = len(mList)
            if nLength == mLength:
                #            print 'exec this line nLength == mLength'
                m = 0
                c = 0
                for n in nList:
                    m = m * 10 + makeRandomInt(int(n), int(mList[c]))

                    c += 1
                return m
            elif nLength < mLength:
                #            print 'exec this line nLength < mLength'
                c = nLength - mLength
                n = 0
                for m in mList:
                    if c < 0:
                        n = n * 10 + makeRandomInt(0, int(m))
                        c += 1
                    else:
                        n = n * 10 + makeRandomInt(int(nList[c]), int(m))
                        c += 1
                return n
            return 0
    return 0


if __name__ == "__main__":
    print('auto generate quiz starts ...')
    # print makeRandomOper()
    # exptmp = generateExpression()
    # print exptmp
    # print formatExpression(exptmp)
    # print calculate(exptmp[0],exptmp[1],exptmp[2])
    # print generateQuiz(5)

    #####generate 2 number expression.

    amountOfQuiz = 1200

    myQuiz = generateQuiz(amountOfQuiz)
    # myQuiz[0] is the list of expression
    # myQuiz[0] is the list of results

    now = datetime.datetime.now()
    suffix = now.strftime('%Y-%B-%d-%I-%M')

    operateDocx.writeDocx(myQuiz[0], f'quizs-{suffix}.docx')
    operateDocx.writeDocx(myQuiz[1], f'quizs_with_answer-{suffix}.docx')
    print('quiz generated! ')

#### test generateThreeExp
# exp = generateThreeExp()
#
# print formatExpression(exp)
# print 'result is : '+ str(cal(exp))
# print produceNum(45,'-',99)