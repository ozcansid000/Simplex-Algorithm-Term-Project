#Link
#https://www.youtube.com/watch?v=upgpVkAkFkQ&t=957s4

from cmu_112_graphics1 import *
import copy
from TP_classes import *
#-------------------------------------------------------------------------------
#SIMPLEX ALGORITHM
#-------------------------------------------------------------------------------

#check negative RHS in constraints
def negRightSide(matrix):
    rows = len(matrix)
    values = []
    for row in range(rows-1):
        values.append(matrix[row][-1])
    if min(values)<0:
        return True
    else:
        return False

    #check negative constraint coefficients
def negConstraintCoef(matrix):
    cols = len(matrix[0])
    values = []
    for col in range(cols-1):
        values.append(matrix[-1][col])
    if min(values)<0:
        return True
    else:
        return False 
      
#find negative elements in last row and column and return their indexes
def negsR(matrix):
    rows, cols = len(matrix),len(matrix[0])
    indexesR = []          #RHS negative indices
    values = []
    for row in range(rows):     
        value = matrix[row][-1]
        if value <= 0:
            indexesR.append(row)
            values.append(value)
    if len(indexesR) == 0:
        return None
    minValue = min(values)
    index = values.index(minValue) 
    return indexesR[index]

def negsB(matrix):
    rows, cols = len(matrix), len(matrix[0])
    mFinal = 1000
    rowFinal = None
    for row in range(rows):
        m = min(matrix[row])
        if m<mFinal:
            mFinal = m
            if m<=0:
                rowFinal = row
    return rowFinal

#Find pivot values    
def findPivotsR(matrix):
    pivots = []
    negElementRowFinal = negsR(matrix)
    rows, cols = len(matrix), len(matrix[0])
    rowValuesMid = []
    colValuesMid = []
    for col in range(cols-1):
        rowValuesMid.append(matrix[negElementRowFinal][col])
        colValuesMid.append(col)
    minValueMiddleCol = min(rowValuesMid)
    indexMinValue = rowValuesMid.index(minValueMiddleCol) 
    indexMidCol = colValuesMid[indexMinValue]
    for row in range(rows-1):        
        valueMid = matrix[row][indexMidCol]
        valueFinal = matrix[row][-1]
        if valueMid**2>0 and valueFinal/valueMid>0:
            ratio = valueFinal/valueMid
            pivots.append(ratio)  
        else:
            pivots.append(10000)
    minRatio = min(pivots) 
    index = pivots.index(minRatio)  
    return [index, indexMidCol]    #returns index of smallest ratio

def findPivotsB(matrix):   
    pivots = []
    negElementColFinal = negsB(matrix)
    rows, cols = len(matrix), len(matrix[0])
    rowValuesMid = []
    colValuesMid = []
    for row in range(rows-1):
        colValuesMid.append(matrix[row][negElementColFinal])
        rowValuesMid.append(row)
    minValueMiddleRow = min(colValuesMid)
    indexMinValue = colValuesMid.index(minValueMiddleRow)
    indexMidRow = rowValuesMid[indexMinValue]
    for col in range(cols-1):       
        valueMid = matrix[indexMidRow][col]
        valueFinal = matrix[-1][col]
        if valueMid != 0:
            ratio = valueFinal/valueMid            
            if ratio > 0:
                pivots.append(ratio)  
        else:
            pivots.append(10000)
    minRatio = min(pivots) 
    index = pivots.index(minRatio)
    return [indexMidRow, index]        #returns index of smallest ratio

#pivotting and finding optimal basis
def pivot(row, col, matrix):     
    rows, cols = len(matrix), len(matrix[0])
    newMatrix = [[0]*cols for row in range(rows)]
    pivotRow = matrix[row]
    if matrix[row][col] != 0:        #checks if element can be pivoted on
        r = []
        for element in pivotRow:
            r.append(element*(1/matrix[row][col]))
        for ro in range(rows):
            value = matrix[ro][col]
            completeRo = matrix[ro]
            if completeRo == pivotRow:
                continue
            else:
                rCopy = copy.copy(r)
                for i in range(len(rCopy)):
                    rCopy[i] = completeRo[i]-rCopy[i]*value
                for co in range(cols):
                    newMatrix[ro][co] = rCopy[co]
        for elementR in range(len(r)):
            newMatrix[row][elementR] = r[elementR]
        return newMatrix  
    else:
        print("Cannot pivot on element")
        return None        
    
#convert inputted numbers to numbers to plug into matrix
def inputToList(input):  
    input = input.split(',')
    if 'G' in input:
        input.remove("G")
        newInput = []
        for num in input:
            newInput.append(float(num)*(-1))
        return newInput
    if 'L' in input:
        input.remove('L')
        newInput = []
        for num in input:
            newInput.append(float(num)*(1))
        return newInput     #returns the important numbers       

#If max problem, convert to min. Min is standard in linear programs
def makeMin(matrix):
    cols = len(matrix[0])
    newRow = []
    for col in range(cols-2):
        newRow.append(matrix[-1][col]*(-1))
    matrix[-1] = newRow
    matrix[-1][-1] = -1*matrix[-1][-1]
    return matrix

#create correct number of variables. Helper for output
def createVariables(matrix):
    rows, cols = len(matrix), len(matrix[0])
    numVariables = cols-rows-1
    variables = []
    for var in range(numVariables):
        variables.append(f'x {str(var+1)}')
    return variables

#add constraints from inputs

#first check if it is a valid output
def isValidConstraint(matrix):
    rows, cols = len(matrix), len(matrix[0])
    constraint= []
    for row in range(rows):
        sum = 0
        for col in range(cols):
            sum += matrix[row][col]*matrix[row][col]
        if sum == 0:
            constraint.append(sum)
    if constraint != [] and len(constraint)>1:
        return True
    return False

#if is a valid constraint then add to matrix  
def addConstraint(matrix, input): #may need to add filter
    if isValidConstraint(matrix):
        rows, cols = len(matrix), len(matrix[0])
        numVariables = cols - rows-1
        for row in range(rows):
            sum = 0
            for col in range(cols):
                sum += matrix[row][col]**2 #turn to float?
            if sum == 0:
                rowF = matrix[row]
                rowIndex = row
                break
        input = inputToList(input)
        for num in range(len(input)-1):
            rowF[num] = input[num]
        rowF[-1] = input[-1]
        rowF[numVariables+rowIndex] = 1

# add objective

# first check if valid objective function
def isValidObjective(matrix):
    rows, cols = len(matrix), len(matrix[0])
    objective = []
    for row in range(rows):
        sum = 0
        for col in range(cols):
            sum += matrix[row][col]**2
        if sum == 0:
            objective.append(sum)
    if len(objective)==1:
        return True
    return False

def addObjective(matrix, input):        #may need to add filter
    if isValidObjective(matrix):
        input = [float(num) for num in input.split(',')]
        rows = len(matrix)
        row = matrix[rows-1] #convert out of numpy
        for num in range(len(input)-1):
            row[num] = input[num]*(-1)
        row[-2] = 1
        row[-1] = input[-1]
    #add else add more constraints, incorporate in app maybe not needed.

#To maximize
def maxProblem(matrix):
    count = 0
    while negRightSide(matrix):
        if count>30:
            return None
        matrix = pivot(findPivotsR(matrix)[0], findPivotsR(matrix)[1], matrix)
        count+=1
    count = 0
    while negConstraintCoef(matrix):
        if count>30:
            return None
        matrix = pivot(findPivotsB(matrix)[0], findPivotsB(matrix)[1], matrix)
        count +=1
        if matrix == None:
            return None     #cannot optimize problem
    rows, cols = len(matrix), len(matrix[0])
    numVariables = cols-rows-1
    objectiveValue = dict()
    for i in range(numVariables):
        currentCol = []
        for row in range(rows):
            currentCol.append(matrix[row][i])
        if sum(currentCol) == max(currentCol):
            for num in range(len(currentCol)):
                if currentCol[num] == max(currentCol):
                    objectiveValue[createVariables(matrix)[i]] = matrix[num][-1]
                    break
                elif num == len(currentCol)-1:
                    objectiveValue[createVariables(matrix)[i]] = 0
    objectiveValue['max'] = matrix[-1][-1]
    return objectiveValue

    #To minimize
def minProblem(matrix):
    matrix = makeMin(matrix)
    rows, cols = len(matrix), len(matrix[0])
    numVariables = cols-rows-1
    count = 0
    while negRightSide(matrix)==True:
        if count>=30:
            return None
        matrix = pivot(findPivotsR(matrix)[0], findPivotsR(matrix)[1], matrix)
        count +=1
    count = 0
    while negConstraintCoef(matrix)==True:
        if count>=30:
            return None
        matrix = pivot(findPivotsB(matrix)[0], findPivotsB(matrix)[1], matrix)
        count+=1
    objectiveValue = dict()
    for i in range(numVariables):
        currentCol = []
        for row in range(rows):
            currentCol.append(matrix[row][i])
        if sum(currentCol) == max(currentCol):
            for num in range(len(currentCol)):
                if currentCol[num] == max(currentCol):
                    objectiveValue[createVariables(matrix)[i]] = matrix[num][-1]
                    break
                elif num == len(currentCol)-1:
                    objectiveValue[createVariables(matrix)[i]] = 0
    objectiveValue['min'] = matrix[-1][-1]*(-1)
    return objectiveValue

#creates initial matrix with correct dimensions
def createMatrix(var, cons):
    rows, cols = cons+1, (cons + var+2)
    matrix = [([0]*cols) for row in range(rows)]
    return matrix

# test cases
m = createMatrix(2,2)
addConstraint(m,'2,-1,G,10')
addConstraint(m,'1,1,L,20')
addObjective(m,'5,10,0')
print(maxProblem(m))

# m = createMatrix(2,5)
# addConstraint(m,'3,2,L,100')
# addConstraint(m,'2,4,L,120')
# addConstraint(m,'1,1,L,60')
# addConstraint(m,'1,0,G,0')
# addConstraint(m,'0,1,G,0')
# addObjective(m, '200,300,0')
# print(maxProblem(m))

# # m = createMatrix(2,4)
# # addConstraint(m,'2,5,G,30')
# # addConstraint(m,'-3,5,G,5')
# # addConstraint(m,'8,3,L,85')
# # addConstraint(m,'-9,7,L,42')
# # addObjective(m,'2,7,0')
# # print(minProblem(m))

#------------------------------------------------------------------------------
#APPSTARTED
#-------------------------------------------------------------------------------

def appStarted(app):
    app.startPage = True
    app.constraintPage = False
    app.objectivePage = False
    app.problemChoicePage = False
    app.flowModel = False
    app.numVariables = None
    app.numConstraints = None
    app.width = 1000
    app.height = 1000
    app.matrix = []
    app.constraints = []
    app.max = False
    app.min = False
    app.transsport = False
    app.asssignment = False
    app.general = False
    app.transport = False
    app.assignment = False
    app.objective = None
    app.output = None
    app.restart = False

def keyPressed(app, event):
    #User adding constraints
    if app.constraintPage == True and event.key == 'a':
        while app.numConstraints>0:
            constraint = app.getUserInput("Type in constraints coefficients in form: variable coefficients separated by commas, G/L, constraint(number)")
            if constraint != None:
                addConstraint(app.matrix, constraint)
                app.constraints += [constraint]
                app.numConstraints -= 1
    #User adding objective function
    if app.objectivePage == True and event.key == 'a':
        objective = None
        while objective == None:
            objective = app.getUserInput("Type objective coefficients separated by commas. Include constant")
        app.objective = objective
        addObjective(app.matrix, objective)

def mousePressed(app, event):
    #switch from startPage to constraintPage
    if event.x in range(app.width) and event.y in range(app.height) and app.startPage == True:     
        app.startPage = False
        app.constraintPage = True
        app.flowModel = True
        while app.numVariables == None:
            app.numVariables = int(app.getUserInput("Enter number of variables"))
        while app.numConstraints == None:
            app.numConstraints = int(app.getUserInput("Enter number of constraints"))
        rows, cols = app.numConstraints+1, (app.numConstraints + app.numVariables+2)
        #create matrix from user input
        app.matrix = [([0]*cols) for row in range(rows)] 

    #switch from constrainPage to objectivePage
    if app.constraintPage ==True and event.x in range(210, 300) and event.y in range(670, 690):
        app.constraintPage = False
        app.objectivePage = True  

    #switch from objectivePage to problemChoice page
    if app.objectivePage == True:
        if app.restart == True and event.x in range(app.width):
            appStarted(app)
        if event.x in range(750,1000) and event.y in range(400,800):      
            app.transsport = True                               
        if event.x in range(750,1000) and event.y in range(400):                  
            app.asssignment = True
        if event.x in range(210, 300) and event.y in range(650, 670):
            app.objectivePage = False
            app.problemChoicePage = True
        if event.x in range(400, 450):
            app.max = True
            if app.transsport == False and app.asssignment == False:            
                app.output = maxProblem(app.matrix)
                if app.output == None:
                    app.restart = True
        if event.x in range(500, 550):
            app.min = True
            if app.transsport == False and app.asssignment == False:            
                app.output = minProblem(app.matrix)
                if app.output == None:
                    app.restart = True

    #switching from problemChoicePage to flowModelPage
    if app.problemChoicePage == True:
        if event.x in range(300, 700):
            app.problemChoicePage = False
            app.flowModel = True
        if event.y in range(50,250) and event.x in range(300,700):
            app.general = True
        if event.y in range(300,500) and event.x in range(300, 700):
            app.transport = True
        if event.y in range(550, 750) and event.x in range(300,700):
            app.assignment = True

#helper to draw constraints
def drawConstraint(constraint, app):
    text = ''
    count = 1
    for num in constraint.split(','):
        if count > app.numVariables:
            if num == 'G':
                text+=('>=')
            elif num == 'L':
                text+=('<=')
            else:
                text+=(f' {num}')
            count+=1
            continue
        text+= f'({num})x{count} '
        if count == app.numVariables:
            count+=1
            continue
        text+="+"
        count+=1
    return text

#helper to draw objective
def drawObjective(objective, app):
    text = ''
    count = 0
    for num in objective.split(','):
        count+=1
        if count == app.numVariables+1:
            break
        text+= f'({num})x{count}+'
    text = text[:-1]
    return text

#Draws each page
def redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'grey')
    if app.startPage == True:                               #drawing start page
        canvas.create_text(app.width/2, app.height/4, 
                                    text = "Optimization for Business",
                                    font = 'Arial 50')
        canvas.create_rectangle(3*app.width/8, 5*app.height/9, 
                                    5*app.width/8, 6*app.height/8
                                    , width = 5, fill = "white")
        canvas.create_text(4*app.width/8, 5*app.height/8+30,
                            text = "Start", 
                            font = "Arial 50")
        canvas.create_rectangle(0,0, app.width, app.height, width = 25)
    if app.constraintPage == True:                          #drawing constraint page
        canvas.create_text(app.width/2, app.height/8-20, text = "press 'a' to add constraints")
        canvas.create_rectangle(app.width/5, app.height/8, 4*app.width/5, 
                    7*app.height/8, width = 3, fill = "white")
        nextButton = Button(210, 670, 300, 690,'white', 'Next')
        nextButton.redraw(app, canvas)

    if app.objectivePage == True:                           #drawing objective page
        canvas.create_text(app.width/2, app.height/8-20, text = "press 'a' to add objective")
        canvas.create_rectangle(app.width/5, app.height/8, 4*app.width/5, 
                        7*app.height/8, width = 3, fill = "white")
        #Draw out constraints      
        constraintCount = 1
        if app.restart == True:
            canvas.create_text(app.width/2, 650, text = "No optimal solution available, click anywhere to restart")
        count=0
        for con in app.constraints:
            count+=1
            text = drawConstraint(con, app)
            if len(con)>15:                            #shrinks text
                fontC= 'Arial 10'
            else:
                fontC = 'Arial 20'
            if count<6:
                canvas.create_text(300, 120, text = 'Constraints', font= 'Arial 24')
                canvas.create_text(350, 120+constraintCount*40, text = text, font = fontC)
                constraintCount+=1  
            if count>=7:
                canvas.create_text(350, 120+280, text = '...') 
        if app.objective != None:   
            text = drawObjective(app.objective, app) 
            if len(text)>25:                #shrinks text
                fontO = 'Arial 10'
            else:
                fontO = 'Arial 20'
            canvas.create_text(300, app.height/2, text = "Objective", font = 'Arial 24')   
            canvas.create_text(350, app.height/2+30, text = text, font = fontO)         
        maxButton = Button(400, 460, 450, 510, 'white', 'Max')
        minButton = Button(500, 460, 550, 510, 'white', 'Min')
        doneButton = Button(210, 650, 300, 670, 'white', 'Done')
        if app.max == True:
            maxButton.fill = 'grey'
        if app.min == True:
            minButton.fill = 'grey'
        if app.objective != None:
            maxButton.redraw(app, canvas)
            minButton.redraw(app, canvas)
        doneButton.redraw(app, canvas)       
    
    if app.problemChoicePage == True:
        canvas.create_text(500, 25, text = "Select type of problem")
        generalButton = Button(300, 50, 700, 250, 'white', 'General')
        transportButton = Button(300, 300, 700, 500, 'white', 'Transport')
        assignmentButton = Button(300, 550, 700, 750, 'white', 'Assignment')
        generalButton.redraw(app, canvas)
        transportButton.redraw(app, canvas)
        assignmentButton.redraw(app, canvas)

    if app.flowModel == True:
        if app.general == True:
            graph = FlowChart(app.output, 'general')
            graph.drawFlow(app, canvas)
        if app.transport == True:
            graph = FlowChart(app.output, 'transport')
            graph.drawFlow(app, canvas)
        if app.assignment == True:
            graph = FlowChart(app.output, 'assignment')
            graph.drawFlow(app, canvas)

runApp(width=1000, height=800)       