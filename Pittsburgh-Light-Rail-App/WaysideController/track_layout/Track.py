class Block():
    def __init__(self, id):
        self.left = []
        self.right = []
        self.hasSwitch = False
        self.switch = None
        self.id = id

    def setRightNode(self, block):
        ## Check for duplicate blocks
        for i in self.right:
            if i.id == block.id:
                return
        self.right.append(block)

    def setLeftNode(self, block):
        ## Check for duplicate blocks
        for i  in self.left:
            if i.id == block.id:
                return
        self.left.append(block)

    def printBlock(self):
        print("Left")
        for i in self.left:
            print(f'\t{i.id}')

        print("Right")
        for i in self.right:
            print(f'\t{i.id}')

    def getNeighbors(self):
        if self.hasSwitch:

            if len(self.left) == 2:
                return (self.left[int(self.switch)], self.right[0])
            if len(self.right) == 2:
                return (self.left[0], self.right[int(self.switch)])
        else:
            return (self.left[0], self.right[0])

class Track():
    def __init__(self, name, size):
        self.trackName = name

        self.blocks = []
        self.switches = {}

        for i in range(size):
            self.blocks.append(Block(i+1))

    def getNumBlocks(self):
        return len(self.blocks)

    def getBlock(self, blockNum):
        return self.blocks[blockNum-1]

    def getInfo(self, blockNum):
        self.blocks[blockNum-1].printBlock()

    def confSwitch(self, id, blockNum):
        self.switches[id] = blockNum

    def setSwitch(self, id, val=None):
        if id not in self.switches:
            print("Error in switch lookup")
            return

        blockNum = self.switches[id]
        block = self.getBlock(blockNum)

        if block.hasSwitch:
            if val != None:
                block.switch = val
            else:
                block.switch = not block.switch

    def getNextBlock(self, curr, prev):
        neighbors = self.blocks[curr-1].getNeighbors()
        if neighbors[0].id == prev:
            return neighbors[1]

        if neighbors[1].id == prev:
            return neighbors[0]

        return -1



