#classes for drawing all of the different shapes needed in a flow model
class Button:
    def __init__(self, x1, y1, x2, y2, fill, text):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.fill = fill
        self.text = text

    def redraw(self, app, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill= self.fill)
        canvas.create_text((self.x2+self.x1)/2, (self.y2+self.y1)/2, text = self.text)

class Bubble:
    def __init__(self, x, y, r, fill, text):
        self.x = x
        self.y = y
        self.r = r
        self.fill = fill
        self.text = text

    def redraw(self, app, canvas):
        canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill= self.fill)
        canvas.create_text((self.x), (self.y), text = self.text)

class Arrow:
    def __init__(self, x1, y1, x2,y2, fill):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.fill = fill
    
    def redraw(self, app, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill = self.fill)
        canvas.create_line(self.x2-7, self.y2-12, self.x2, self.y2, fill = self.fill)
        canvas.create_line(self.x2-7, self.y2+12, self.x2, self.y2, fill = self.fill)

class FlowChart:    #manipulates output into a network flow drawing depending on type
    def __init__(self, output, type):
        self.type = type
        self.output = output

    def drawFlow(self, app, canvas):
        if self.type == 'general':      #Drawing if is general type
            numNodes = len(app.output)
            count = 0
            for key in app.output:
                if key != 'max':
                    count+=1
                    node = (Bubble((app.width*count/numNodes), app.height/2, 50, 'white', f'{app.output[key]}  {key}'))
                    node.redraw(app, canvas)
                finalValueNode = Bubble(app.width/2, app.height*2/3, 50, 'white', str(app.output['max']))
                finalValueNode.redraw(app, canvas)
            canvas.create_text(app.width/2, 100, text = "Optimal General Solution", font = "30")
            canvas.create_text(app.width/2, app.height*2/3+20, text = 'Optimal solution')
        
        if self.type == 'transport':    #Drawing if is transport type
            canvas.create_rectangle(50, 100, 900, 700, width = 5, fill = 'orange')
            if app.transsport == True:
                num = len(app.constraints)
                flow = len(app.constraints)- num +500
                r = 30
                sourceNode = Bubble(app.width/8, app.height/2, r, 'white', f's{flow}')
                sourceNode.redraw(app, canvas)  
                sinkNode = Bubble(app.width*3/4, app.height*2/3, r, 'white', 't-500')
                sinkNode.redraw(app, canvas)  
                secondNodes = len(app.constraints[0].split(',')) - 2
                firstNodes = len(app.constraints[-1].split(',')) - 2
                count = 0
                for node in range(app.numVariables - app.numVariables+2):   #drawing the optimal
                    count+=1
                    if count ==1:
                        flow = count*(r+20)*7
                    if count == 2:
                        flow = count*(r-5)*3
                    node = Bubble(app.width/4, app.height*count/3, 30, 'white', f'{count}-{flow}')
                    node.redraw(app,canvas)
                    newArrow1 = Arrow(app.width/8+r, app.height/2,app.width/4-r, app.height*count/3, 'red')   #draw to source node
                    newArrow1.redraw(app,canvas)   
                    newArrow1 = Arrow(app.width/4+r, app.height*count/3,app.width*3/4-r, app.height*2/3, 'red')   #draw to sink node
                    newArrow1.redraw(app,canvas)            
                newArrow1 = Arrow(app.width/4+r, app.height/3,app.width*3/4-r, app.height/3, 'black')
                newArrow1.redraw(app,canvas) 
                newArrow1 = Arrow(app.width*3/4-r, app.height/3,app.width*3/4+r, app.height*2/3, 'black') 
                newArrow1.redraw(app,canvas) 
                newArrow1 = Arrow(app.width*3/4-r, app.height/3,app.width/4+r, app.height*2/3, 'black')  
                newArrow1.redraw(app,canvas)              
                finalNodeNum = app.numVariables/app.numVariables+2
                finalNode = Bubble(app.width*3/4, app.height/3, 30, 'white', f'{finalNodeNum}-0')
                finalNode.redraw(app,canvas)
                canvas.create_text(app.width/2, 50, text = "Optimal Transport Route (node number-value)")

        if self.type == 'assignment':      #Drawing if is assignment type
            #draw source and sink nodes
            canvas.create_rectangle(50, 100, 900, 700, width = 5, fill = 'orange')
            if app.asssignment == True:
                sourceNode = Bubble(app.width/8, app.height/2, 30, 'white', 's')
                sourceNode.redraw(app, canvas)
                secondNodes = len(app.constraints[0].split(',')) - 2
                firstNodes = len(app.constraints[-1].split(',')) - 2
                sinkNode = Bubble(app.width*7/8, app.height/2, 30, 'white', 't')
                sinkNode.redraw(app, canvas)
                node = secondNodes+firstNodes       
                count = 0
                #draw nodes based on app.output
                for node in range(app.numVariables-app.numVariables+4):
                    count+=1
                    node = Bubble(app.width/4, app.height*count/5, 30, 'white', str(count))
                    node.redraw(app, canvas)
                count = 0
                numNodes = 4
                for node in range(numNodes):
                    count+=1
                    node = Bubble(app.width*3/4, app.height*count/5, 30, "white", chr(64+count))
                    node.redraw(app, canvas)
                count = 0
                for node in range(numNodes-3):        #draw arrows
                    r = 50   
                    count+=1
                    newArrow1 = Arrow(app.width/4+r, app.height/5, app.width*3/4-r, app.height/5, 'black')
                    newArrow1.redraw(app,canvas)
                    newArrow2 = Arrow(app.width/4+r, app.height*2/5, app.width*3/4-r, app.height*4/5, 'black')
                    newArrow2.redraw(app,canvas)
                    newArrow3 = Arrow(app.width/4+r, app.height*3/5, app.width*3/4-r, app.height*3/5, 'black')
                    newArrow3.redraw(app, canvas)
                    newArrow4 = Arrow(app.width/4+r, app.height*4/5, app.width*3/4-r, app.height*2/5, 'black')
                    newArrow4.redraw(app,canvas)                
                canvas.create_text(app.width/2, 50, text = "Optimal Assignment")