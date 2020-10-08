import tkinter as tk
from tkinter import ttk, messagebox
import time
from algorithm import *
# Hard size for the show

HEIGHT = 600
WIDTH = 600
SIDE = 24 # Size of 1 cell
# colers

# Check at that location is the wall
def isWall(a, row, col):
	return a[row][col] == 1

#Check at that location is the starting point
def isStart(a, row, col):
	return a[row][col] == -2

#Check at that spot is the end point
def isGoal(a, row, col):
	return a[row][col] == 2

#Reset coordinates within allowable range
def setInRange(a, row, col):
	if row < 0:
		row = 0
	if row >= len(a):
		row = len(a)-1
	if col < 0:
		col = 0
	if col >= len(a[0]):
		col = len(a[0])-1
		
	return row, col

# The program has 3 main classes
# - Board: Used to draw walls, erase walls, ...
# - ProcessBoard: inherit Board, have more functions to find a way, draw a path, delete a path
# - OptionBoard: run, delete, select algorithm, link with ProcessBoard button
	
#Board
class Board(tk.Frame): #Extends the frame of tkinter
	def __init__(self, root, h = HEIGHT, w=WIDTH):
		
		super().__init__(root, width=h, height=w)

		
		self.canvas = tk.Canvas(self, width = WIDTH, height=HEIGHT, bg='white')
		
		heightMatrix = h//SIDE
		widthMatrix = w//SIDE

		self.a = [[0] * (heightMatrix) for i in range(widthMatrix)] #Match of Board
		
		
		#0 is to go, 1 is not to go
		
		#Initialize start and end point
		self.startNode = Node(None, (heightMatrix//2, 0))
		self.endNode = Node(None, (heightMatrix//2, widthMatrix-1))
		
		#Set position for start, end
		startRow, startCol = self.startNode.position
		endRow, endCol = self.endNode.position
	
		self.a[startRow][startCol] = -2 #The starting point is valid -2
		self.a[endRow][endCol] = 2 #The end point is valid 2
		
		#List contains wall positions
		self.wallList = []
		
		
		
	def drawBoard(self):
	
		self.pack(side='left')
		self.canvas.pack()
		
		#Draw horizontal and vertical lines to form the board
		
		#Draw horizontal lines
		x1 = 0
		x2 = WIDTH
		for k in range(0, HEIGHT+1, SIDE):
			y1 = k
			y2 = k
			self.canvas.create_line(x1, y1, x2, y2)
			
		#Draw vertical lines
		y1 = 0
		y2 = HEIGHT
		for k in range(0, WIDTH+1, SIDE):
			x1 = k
			x2 = k
			self.canvas.create_line(x1, y1, x2, y2)
			
		#Color start and end points
		self.highlight(self.startNode.position[0], self.startNode.position[1], 'green')
		self.highlight(self.endNode.position[0], self.endNode.position[1], 'orange')
		
		
	#Create actions with users	
	def setUI(self):
		
		# Click event handling
		self.canvas.bind("<Button-1>", self.callbackClick)


	#Delete user action	
	def disableUI(self):
		
		self.canvas.unbind("<Button-1>")
		self.canvas.unbind("<B1-Motion>")

	#Update the start and end point when manipulated
	def updateStart(self, row, col):
		self.a[row][col] = -2
		self.startNode.position = (row, col)
		
	def updateGoal(self, row, col):
		self.a[row][col] = 2
		self.endNode.position = (row, col)
	
	
	#Fill clicked 1 cell
	def highlight(self, row, col, color):
		
		#The essence is to create another colored rectangle in that position
		x0 = col * SIDE
		y0 = row * SIDE

		x1 = (col + 1) * SIDE
		y1 = (row + 1) * SIDE
		
		#If gray, set value and add position to wallList
		if color == 'darkslategray':
			self.a[row][col] = 1
			self.wallList.append((row, col))
			
		#If it is green then updateStar
		elif color == 'green':
			self.updateStart(row, col)
			
		#If the color is orange, updateGoal	
		elif color == 'orange':
			self.updateGoal(row, col)
			
		self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black', tags='rect')
	
		
	#Remove color 1 cell
	def hide(self, row, col):
		
		#If it's a wall, delete the position in wall List
		if self.a[row][col] == 1:
			self.wallList.remove((row, col))
			
				
		#Set value 
		self.a[row][col] = 0
		
		#The fact is to create a white rectangle in that position
		x0 = col * SIDE
		y0 = row * SIDE

		x1 = (col + 1) * SIDE
		y1 = (row + 1) * SIDE

		self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')
				
	#Function to draw walls, remove walls, ... when the user manipulates
	def callbackClick(self, event):
		
		self.canvas.focus_set()
		
		#Get the row and column values clicked
		row, col = int((event.y) / SIDE), int((event.x) / SIDE)
		
		row, col = setInRange(self.a, row, col)
			
		
		
		#If you click on the start or end point hold will drag the point
		if isStart(self.a, row, col):
			self.canvas.bind("<B1-Motion>", self.dragStart)
		
		elif isGoal(self.a, row, col):
			self.canvas.bind("<B1-Motion>", self.dragGoal)
		
		else:
		
			#Neu click on the wall to hold will delete the wall
			if isWall(self.a, row, col):
				self.hide(row, col)
				self.canvas.bind("<B1-Motion>", self.deleteWall)
				
			#Neu click on the empty box to hold will create a wall
			else:
				self.highlight(row, col, 'darkslategray')
				self.canvas.bind("<B1-Motion>", self.createWall)
				
	#NOTE: Feel this function a bit cumbersome, probably can make smoother
		
# Drag the starting point
	def dragStart(self, event):
	
		self.canvas.focus_set()
		
		# Old point
		oldRow = self.startNode.position[0]
		oldCol = self.startNode.position[1]
		
		#New point
		row, col = int((event.y) / SIDE), int((event.x) / SIDE)
		row, col = setInRange(self.a, row, col)
		
		# If eligible, then drag points by applying new embellishments and removing old points
		if not isWall(self.a, row, col) and (oldRow, oldCol) != (row, col) and not isGoal(self.a, row, col):
			self.highlight(row, col, 'green')
			self.hide(oldRow, oldCol)
	
	# Drag the end point
	def dragGoal(self, event):
	
		self.canvas.focus_set()
		
		#Old point
		oldRow = self.endNode.position[0]
		oldCol = self.endNode.position[1]
		
		#new point
		row, col = int((event.y) / SIDE), int((event.x) / SIDE)
		
		row, col = setInRange(self.a, row, col)
			
		# If eligible, then drag points by applying new embellishments and removing old points
		if not isWall(self.a, row, col) and (oldRow, oldCol) != (row, col) and not isStart(self.a, row, col):
			self.highlight(row, col, 'orange')
			self.hide(oldRow, oldCol)
		
#NOTE: Feels that the above 2 functions can be pooled	

	#Tạo wall
	def createWall(self, event):

		self.canvas.focus_set()
		
		#Lấy giá trị dòng và cột được click
		row, col = int((event.y) / SIDE), int((event.x) / SIDE)
		row, col = setInRange(self.a, row, col)
			
		#Nếu đủ điều kiện thì tô màu ô đó
		if not isWall(self.a, row, col) and not isStart(self.a, row, col) and not isGoal(self.a, row, col):
			self.highlight(row, col, 'darkslategray')
			
	
	# Erase wall
	def deleteWall(self, event):

		self.canvas.focus_set()
		
		# Get the row and column values clicked
		row, col = int((event.y) / SIDE), int((event.x) / SIDE)
		
		row, col = setInRange(self.a, row, col)
		
		# If the point is wall, delete that box
		if isWall(self.a, row, col):
			self.hide(row, col)
		
	
	
#================================================================================================================================	
	
class ProcessBoard(Board):
	def __init__(self, root):
		
		
		
		super().__init__(root)
		
		
		#Order browsing route
		self.traversal = []
		
		
		#Way
		self.path = []
		
		# The algorithm used, default is A *
		self.algo = "A* Search (Mahattan)"

		# During the run, do not click Run
		self.button = None	# Link to the Run button on the Option Board
	
	# Function handle when click Run
	def findPath(self):
		
		# Delete old paths before drawing new paths
		self.clearPath()
		
		#Temporary variable
		traversal, path = 0, 0
		
		#Choosing algorithm
		if self.algo == "A* Search (Mahattan)":
		
			traversal, path = astar(self.a, self.startNode.position, self.endNode.position)
		
		elif self.algo == "A* Search (Euclide)":
		
			traversal, path = astar(self.a, self.startNode.position, self.endNode.position, "Euclide")
		
		elif self.algo == "Dijkstra Search":
			traversal, path = ucs(self.a, self.startNode.position, self.endNode.position)
			
		elif self.algo == "Breadth First Search" :
			traversal, path = bfs(self.a, self.startNode.position, self.endNode.position)
			
		else:
			traversal, path = dfs(self.a, self.startNode.position, self.endNode.position)
		
		#NOTE: The above is too cumbersome, can be compacted
		
		# Can't find the way to output the notification
		if path == -1:
			messagebox.showerror(message='No path', title='Error')
		
		else:
			self.traversal = traversal
			self.path = path
			
			
			# Draw the path
			self.drawSearch()
		


	# Function delete all when clicking Clear All		
	def clearAll(self):

		# Erase wall
		# Delete first element until empty
		
		while self.wallList != []:
			self.hide(self.wallList[0][0], self.wallList[0][1])
			
		#Clear the way
		self.clearPath()
		
	# Clear the way
	def clearPath(self):
	
		# Clear all path boxes color
		for x in self.path:
			if x != self.startNode.position and x != self.endNode.position and not isWall(self.a, x[0], x[1]):
				self.hide(x[0], x[1])
		self.path = []		# Reset empty
		
	# Clear all browser cells color
		for x in self.traversal:
			if x != self.startNode.position and x != self.endNode.position and not isWall(self.a, x[0], x[1]):
				self.hide(x[0], x[1])
		self.traversal = []	# Reset empty
			
			
	#NOTE: The upper function is too long


	# Link to the Run button on the Option Board
	def linkto(self, optionBoard):
		self.button = optionBoard.runButton

	# Function to draw paths
	def drawSearch(self, i=0, j=1):
		#Do not manipulate during drawing
		
		self.button.config(state = "disable")	# Paralyze the Run button
		self.disableUI()						# List manipulation Board
	
		# Draw the route, when finished drawing, draw the path
		if i >= len(self.traversal)-1:
			if j >= len(self.path)-1:
			
				# This section is the end of drawing
				self.button.config(state = "active") 	# Make the Run button clickable
				self.setUI()							# Make the Board work
				#self.canvas.after_cancel(self.doPath)
				return
			else:
				self.highlight(self.path[j][0], self.path[j][1], 'blue') 
				self.canvas.after(0, lambda: self.drawSearch(i, j+1))
		else:
			self.highlight(self.traversal[i][0], self.traversal[i][1], '#f7df2e')
			self.canvas.after(5, lambda: self.drawSearch(i+1))
		
		
	
#================================================================================================================================

#BoardOption
class OptionBoard(tk.Frame):
	def __init__(self, root, h=HEIGHT, w=WIDTH//3):
		
		
		#Frame next to Main Board
		super().__init__(root, width=h, height=w)
		self.pack(side='left')
		
		
		self.process = None
		
		
		#Button Run
		self.runButton = None
		
	
		#Button Clear All
		self.clearButton = None
		
		
		
		#Button Clear Path
		self.clearPathButton = None
				
		#Combobox selects algorithm
		self.algoBox = ttk.Combobox(self, 
                            values=[
                                    "A* Search (Mahattan)",
									"A* Search (Euclide)",									
                                    "Dijkstra Search",
                                    "Breadth First Search",
                                    "Depth First Search"])
		
		self.algoBox.current(0)
		self.algoBox.bind("<<ComboboxSelected>>", self.chooseAlgo)
		
		
		
	#
	def drawOptionBoard(self):
		self.pack(side='left')
		self.runButton.pack(fill='x', padx=10)
		self.clearButton.pack(fill='x', padx=10)
		self.clearPathButton.pack(fill='x', padx=10)
		self.algoBox.pack(fill='x', padx=10)

	
	#The algorithm sets the algorithm when the algorithm is clicked
	def chooseAlgo(self, event):
			self.process.algo = self.algoBox.get()
	
	# Link with Process Board to run the route corresponding to the selected algorithm
	def linkto(self, processBoard):
		self.process = processBoard
		self.runButton = tk.Button(self, text='Run', width = 10, command = self.process.findPath)
		self.clearButton = tk.Button(self, text='Clear All', width = 10, command = self.process.clearAll)
		self.clearPathButton = tk.Button(self, text='Clear Path', width = 10, command=self.process.clearPath) 
		


#================================================================================================================================

def main():


	root = tk.Tk()
	root.geometry('770x603+300+50') 
	root.resizable(False, False)	# Fixed size for windows
	root.title("Pathfinding Visualizer")
	
	
	
	process_board = ProcessBoard(root)
	process_board.drawBoard()
	process_board.setUI()
	
	
	option_board = OptionBoard(root)
	
	
	option_board.linkto(process_board)
	option_board.drawOptionBoard()
	
	
	process_board.linkto(option_board)
	
	
	root.mainloop()

if __name__ == "__main__":
	main()
	










