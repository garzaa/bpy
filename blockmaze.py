import bpy
import mathutils
import random

class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def add(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def sub(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def scale(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)


N = Vec3(0, 1, 0)
S = Vec3(0, -1, 0)
E = Vec3(1, 0, 0)
W = Vec3(-1, 0, 0)
U = Vec3(0, 0, 1)
D = Vec3(0, 0, -1)


class Stack:
    def __init__(self):
        self.content = []

    def push(self, x):
        self.content.append(x)

    def empty(self):
        return len(self.content) == 0

    def pop(self):
        return self.content.pop()

class Cell:
    def __init__(self, x, y, z):
        self.connections = []
        self.visited = False
        self.x = x
        self.y = y
        self.z = z
        self.pos = Vec3(x, y, z)

    def connect(self, other):
        # make connections a vec3 between this and the other
        # this.pos +( other.pos sub this.pos / 2)
        self.connections.append(self.pos.add(other.pos.sub(self.pos).scale(0.5)))
        

class SquareGrid:
    def __init__(self, gridSize: int, cellSize: float, spacing: float):
        self.gridSize = gridSize
        self.cellSize = cellSize
        self.spacing = spacing

        self.xRow = []
        for x in range(gridSize):
            yRow = []
            for y in range(gridSize):
                zRow = []
                for z in range(gridSize):
                    zRow.append(Cell(x, y, z))
                yRow.append(zRow)
            self.xRow.append(yRow)

    def get(self, x, y, z):
        # print(str(x) + " " + str(y) + " " + str(z))
        return self.xRow[x][y][z]


    def get_unvisited_neighbors(self, cell):
        neighbors = []
        for x in self.get_neighbors(cell):
            if not x.visited:
                neighbors.append(x)
        return neighbors

    
    def get_neighbors(self, cell: Cell):
        # TODO: return a list of tuples with neighbors and directions
        neighbors = []
        if cell.x > 0:
            neighbors.append(self.get(cell.x-1, cell.y, cell.z))
        if cell.x < self.gridSize-1:
            neighbors.append(self.get(cell.x+1, cell.y, cell.z))
        if cell.y > 0:
            neighbors.append(self.get(cell.x, cell.y-1, cell.z))
        if cell.y < self.gridSize-1:
            neighbors.append(self.get(cell.x, cell.y+1, cell.z))
        if cell.z > 0:
            neighbors.append(self.get(cell.x, cell.y, cell.z-1))
        if (cell.z < self.gridSize-1):
            neighbors.append(self.get(cell.x, cell.y, cell.z+1))
        return neighbors

            
    def solve(self):
        print("solving")
        stack = Stack()
        # pick initial cell, mark as visited and push to the stack
        currentCell = self.get(random.randint(0, self.gridSize-1), random.randint(0, self.gridSize-1), random.randint(0, self.gridSize-1))
        currentCell.visited = True
        stack.push(currentCell)
        while not stack.empty():
            currentCell = stack.pop()
            currentUnvisitedNeighbors = self.get_unvisited_neighbors(currentCell)
            if len(currentUnvisitedNeighbors) > 0:
                stack.push(currentCell)
                currentNeighbor = currentUnvisitedNeighbors[random.randint(0, len(currentUnvisitedNeighbors)-1)]
                currentNeighbor.connect(currentCell)
                currentCell.connect(currentNeighbor)
                currentNeighbor.visited = True
                stack.push(currentNeighbor)
        print("solved")
    

    def add_cube(self, x, y, z):
        bpy.ops.mesh.primitive_cube_add(location=(x*self.spacing, y*self.spacing, z*self.spacing))
        bpy.ops.transform.resize(value=(self.cellSize, self.cellSize, self.cellSize))

    
    def make(self):
        for x in range(len(self.xRow)):
            for y in range(len(self.xRow[x])):
                for z in range(len(self.xRow[x][y])):
                    # print(str(x) + " " + str(y) + " " + str(z))
                    self.add_cube(x*self.spacing, y*self.spacing, z*self.spacing)
                    # then if there's a connection between self and neighbor, draw a cube between them
                    c: Cell = self.xRow[x][y][z]
                    # eventually, shouldn't add a cube if (positive component)
                    for v in c.connections:
                        # this is a list of vec3s
                        self.add_cube(x+v.x, y+v.y, z+v.z)
                        pass
        
            
grid: SquareGrid = SquareGrid(5, 1, 2)
grid.solve()
grid.make()
