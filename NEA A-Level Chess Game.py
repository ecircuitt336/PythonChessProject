from pygame import *
from tkinter import *

# Tkinter Initialisation
window = Tk()
window.title("Chess - Account")
window.geometry("512x512")
window.resizable(False, False)
window.configure(bg="#80b3ff")

# Global variables
gridList = [["a","b","c","d","e","f","g","h"],["8","7","6","5","4","3","2","1"]]
pieceObjectList = []
pieceRectList = []
gridRectList = []

selectedPiece = None
previouslyMovedPiece = None
playerOne = True
gameRunning = False

# Global classes
class Piece():
    def __init__(self, screen, colour, startPos, name, currentPos=None, firstMove=True, hasDoubledLastMove=False):
        self.screen = screen
        self.colour = colour
        self.startPos = startPos
        self.name = name
        self.currentPos = currentPos
        self.firstMove = firstMove
        self.hasDoubledLastMove = hasDoubledLastMove

        if self.currentPos == None:
            self.currentPos = self.startPos
        
    # Summon piece on board at startPos
    def summonPiece(self, pieceType):
        # Get design of pieceType and summon it at position startPos
        pieceImg = None
        if self.colour == "White":
            pieceImg = image.load("Design/Pieces/White/" + pieceType + ".png").convert_alpha()
        elif self.colour == "Black":
            pieceImg = image.load("Design/Pieces/Black/" + pieceType + ".png").convert_alpha()
        coordinates = self.startPos
        xStart = coordinates[0]
        yStart = coordinates[1]
        xEnd = 0
        yEnd = 0
        for i in range(len(gridList[0])):
            for j in range(len(gridList[1])):
                if yStart == gridList[1][j]:
                    yEnd = j * 64
            if xStart == gridList[0][i]:
                xEnd = i * 64
        
        pieceObjectList.append(self)
        pieceRectList.append(self.getPosition())
        self.screen.blit(pieceImg, (xEnd,yEnd))
        display.flip()

    # GETTTERS/SETTERS
    def getColour(self):
        return self.colour
    
    def getName(self):
        return self.name

    def getFirstMove(self):
        return self.firstMove

    def getHasDoubledLastMove(self):
        return self.hasDoubledLastMove

    def getCurrentPosition(self):
        return self.currentPos

    def setVoidPosition(self, pieceTaken, enPassant, knight, rook):
        newSurface = Surface((64,64))

        chosenColour = 0
        colour1 = "#f0e68c"
        colour2 = "#c04000"
        for i in range(len(gridRectList)):
            if (gridRectList[i-1][0], gridRectList[i-1][1]) == self.getPosition():
                if self.getPosition()[1] == 512 or self.getPosition()[1] == 384 or self.getPosition()[1] == 256 or self.getPosition()[1] == 128 or self.getPosition()[1] == 0:
                    if i % 2 == 0:
                        newSurface.fill(colour2)
                        chosenColour = 2
                    else:
                        newSurface.fill(colour1)
                        chosenColour = 1
                else:
                    if i % 2 == 0:
                        newSurface.fill(colour1)
                        chosenColour = 1
                    else:
                        newSurface.fill(colour2)
                        chosenColour = 2

        
        if enPassant == True or knight == True:
            if chosenColour == 1:
                newSurface.fill(colour2)
            else:
                newSurface.fill(colour1)

        if rook == True:
            Pos = pieceTaken.getPosition()
            PosX = Pos[0]//64
            PosY = Pos[1]//64

            # If square is dark
            if PosY % 2 != 0 and PosX % 2 == 0:
                if selectedPiece.getColour() == "Black":
                    newSurface.fill(colour2)
            elif PosY % 2 == 0 and PosX % 2 == 1:
                newSurface.fill(colour2)
            # If square is light
            if PosY % 2 == 0 and PosX % 2 == 0:
                if selectedPiece.getColour() == "White":
                    newSurface.fill(colour1)
            elif PosY % 2 != 0 and PosX % 1:
                newSurface.fill(colour1)
                
        
        self.screen.blit(newSurface, pieceTaken.getPosition())    
        
        display.flip()

    def setHasDoubledLastMove(self, val):
        self.hasDoubledLastMove = val
        

    # Detect if piece is being clicked
    def selectPiece(self, index):
        mpos = mouse.get_pos()
        rect = Rect(pieceRectList[index][0], pieceRectList[index][1], 64, 64)
        is_touching = rect.collidepoint(mpos)
        if is_touching:
            if self.colour == "White" and playerOne == True:
                return True
            elif self.colour == "White" and playerOne == False:
                return False
            elif self.colour == "Black" and playerOne == True:
                return False
            elif self.colour == "Black" and playerOne == False:
                return True

    # Get current position on board
    def getPosition(self):
        xStart = self.currentPos[0]
        yStart = self.currentPos[1]
        xEnd = 0
        yEnd = 0
        for i in range(len(gridList[0])):
            for j in range(len(gridList[1])):
                if yStart == gridList[1][j]:
                    yEnd = j * 64
            if xStart == gridList[0][i]:
                xEnd = i * 64
        return (xEnd, yEnd)

    # Convert tuple to gridList coordinate
    def convertCoordinate(self, coord):
        xStart = coord[0]
        yStart = coord[1]
        xNum = int(xStart / 64)
        yNum = int(yStart / 64)
        xEnd = gridList[0][xNum]
        yEnd = gridList[1][yNum]

        return xEnd + yEnd

    # Move piece to coordinate
    def movePiece(self, clickedSquare, pieceType, colour):
        global pieceRectList
        global pieceObjectList
        global previouslyMovedPiece
        
        pieceImg = None
        if colour == "White":
            pieceImg = image.load("Design/Pieces/White/" + pieceType + ".png").convert_alpha()
        elif colour == "Black":
            pieceImg = image.load("Design/Pieces/Black/" + pieceType + ".png").convert_alpha()

        prePosition = self.getPosition()
        for i in range(len(pieceRectList)):
            if (pieceRectList[i-1][0], pieceRectList[i-1][1]) == prePosition:
                del pieceRectList[i-1]
                del pieceObjectList[i-1]
        
        self.currentPos = self.convertCoordinate((clickedSquare.x, clickedSquare.y))
                
        pieceRectList.append(self.getPosition())
        pieceObjectList.append(self)
        newSurface = Surface((64,64))
        colour1 = "#f0e68c"
        colour2 = "#c04000"
        for i in range(len(gridRectList)):
            if (gridRectList[i-1][0], gridRectList[i-1][1]) == prePosition:
                if prePosition[1] == 512 or prePosition[1] == 384 or prePosition[1] == 256 or prePosition[1] == 128 or prePosition[1] == 0:
                    if i % 2 == 0:
                        newSurface.fill(colour2)
                    else:
                        newSurface.fill(colour1)
                else:
                    if i % 2 == 0:
                        newSurface.fill(colour1)
                    else:
                        newSurface.fill(colour2)

        if self.firstMove == True:
            self.firstMove = False

        previouslyMovedPiece = self
                
        
        self.screen.blit(newSurface, (prePosition))
        self.screen.blit(pieceImg, (clickedSquare.x,clickedSquare.y))
        display.flip()

    # Attack another piece
    def takePiece(self, pieceTaken, enPassant=False, knight=False, rook=False):
        global pieceRectList
        global pieceObjectList
        
        for i in range(len(pieceObjectList)):
            if pieceObjectList[i-1] == pieceTaken:
                del pieceRectList[i-1]
                del pieceObjectList[i-1]

        self.setVoidPosition(pieceTaken, enPassant, knight, rook)
        

class Pawn(Piece):
    def __init__(self, screen, colour, startPos):
        Piece.__init__(self, screen, colour, startPos, "Pawn")
        super().summonPiece("Pawn")

    # Check move is legal
    def validateMove(self, clickedSquare):
        currentPos = super().getPosition()
        if super().getColour() == "White":
            # Is clicked square in same file
            if clickedSquare.x == currentPos[0]:
                # Is clicked square one above current square
                if clickedSquare.y == currentPos[1]-64:
                    # Does clicked square contain another piece
                    for piece in pieceObjectList:
                        if piece.getPosition() == (clickedSquare.x, clickedSquare.y):
                            # Illegal move
                            return False
                    # Legal move
                    return True
                else:
                    # Was square clicked the second above pawn
                    if clickedSquare.y == currentPos[1]-128:
                        # Is it first move
                        if super().getFirstMove() == True:
                            # Does a piece occupy clicked square
                            for piece in pieceObjectList:
                                if piece.getPosition() == (clickedSquare.x, clickedSquare.y):
                                    # Illegal move
                                    return False
                            # Legal move
                            super().setHasDoubledLastMove(True)
                            return True
                        else:
                            # Illegal move
                            return False
                    else:
                        # Illegal move
                        return False
            else:
                # Is clicked square in file to left or right of current one
                if clickedSquare.x == currentPos[0]-64 or clickedSquare.x == currentPos[0]+64:
                    # Is clicked square 1 above current square in file
                    if clickedSquare.y == currentPos[1]-64:
                        # Is a piece in clicked square
                        for piece in pieceObjectList:
                            if piece.getPosition() == (clickedSquare.x, clickedSquare.y):
                                # Capture piece and move pawn
                                super().takePiece(piece)
                                return True
                        # Did previously moved pawn move two spaces
                        if previouslyMovedPiece != None:
                            if previouslyMovedPiece.getHasDoubledLastMove() == True:
                                if clickedSquare.x == previouslyMovedPiece.getPosition()[0]:
                                    if clickedSquare.y == previouslyMovedPiece.getPosition()[1]-64:
                                        super().takePiece(previouslyMovedPiece, enPassant=True)
                                        return True
                        # Illegal move
                        return False
                else:
                    # Illegal move
                    return False
                
        else:
            # Is clicked square in same file
            if clickedSquare.x == currentPos[0]:
                # Is clicked square one above current square
                if clickedSquare.y == currentPos[1]+64:
                    # Does clicked square contain another piece
                    for piece in pieceObjectList:
                        if piece.getPosition() == (clickedSquare.x, clickedSquare.y):
                            # Illegal move
                            return False
                    # Legal move
                    return True
                else:
                    # Was square clicked the second above pawn
                    if clickedSquare.y == currentPos[1]+128:
                        # Is it first move
                        if super().getFirstMove() == True:
                            # Does a piece occupy clicked square
                            for piece in pieceObjectList:
                                if piece.getPosition() == (clickedSquare.x, clickedSquare.y):
                                    # Illegal move
                                    return False
                            # Legal move
                            super().setHasDoubledLastMove(True)
                            return True
                        else:
                            # Illegal move
                            return False
                    else:
                        # Illegal move
                        return False
            else:
                # Is clicked square in file to left or right of current one
                if clickedSquare.x == currentPos[0]-64 or clickedSquare.x == currentPos[0]+64:
                    # Is clicked square 1 above current square in file
                    if clickedSquare.y == currentPos[1]+64:
                        # Is a piece in clicked square
                        for piece in pieceObjectList:
                            if piece.getPosition() == (clickedSquare.x, clickedSquare.y):
                                # Capture piece and move pawn
                                super().takePiece(piece)
                                return True
                        # Did previously moved pawn move two spaces
                        if previouslyMovedPiece != None:
                            if previouslyMovedPiece.getHasDoubledLastMove() == True:
                                if clickedSquare.x == previouslyMovedPiece.getPosition()[0]:
                                    if clickedSquare.y == previouslyMovedPiece.getPosition()[1]+64:
                                        super().takePiece(previouslyMovedPiece, enPassant=True)
                                        return True
                        # Illegal move
                        return False
                else:
                    # Illegal move
                    return False

    # Promote pawn
    def promote(self):
        pass
    

class Bishop(Piece):
    def __init__(self, screen, colour, startPos):
        Piece.__init__(self, screen, colour, startPos, "Bishop")
        super().summonPiece("Bishop")
    
    # Check move is legal
    def validateMove(self, clickedSquare):
        currentPos = super().getPosition()
        clickedPos = (clickedSquare.x, clickedSquare.y)
        
        if super().getColour() == "White":
            startFromX = False
            # Get every square from one corner to another corner of bishops diagonal
            for i in range(0,7):
                if clickedPos[0]//64 < clickedPos[1]//64:
                    startFromX = True

                # If diagonal ends on top of board or side
                if startFromX == True:
                    totalHDist = clickedPos[0]//64
                    pieceHDist = totalHDist - currentPos[0]//64

                    # If clicked square is top right diagonal or bottom right diagonal
                    if pieceHDist > 0:
                        # If clicked position is in top right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 - pieceHDist:
                            # Top Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom right diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 + pieceHDist:
                            # Bottom Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                    elif pieceHDist < 0:
                        # If clicked position is in top left diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 + pieceHDist:
                            # Top Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom left diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 - pieceHDist:
                            # Bottom Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                                # There is no other piece in diagonal
                                return True
                else:
                    totalVDist = clickedPos[1]//64
                    pieceVDist = totalVDist - currentPos[1]//64
                    
                    # If clicked square is top right diagonal or top left diagonal
                    if pieceVDist < 0:
                        # If clicked position is in top right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 - pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Top Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom right diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Top Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                    elif pieceVDist > 0:
                        # If clicked position is in bottom right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Bottom Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom left diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 - pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Bottom Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                                # There is no other piece in diagonal
                                return True

                            
        else:

            
            startFromX = False
            # Get every square from one corner to another corner of bishops diagonal
            for i in range(0,7):
                if clickedPos[0]//64 > clickedPos[1]//64:
                    startFromX = True

                # If diagonal ends on top of board or side
                if startFromX == True:
                    totalHDist = clickedPos[0]//64
                    pieceHDist = totalHDist - currentPos[0]//64

                    # If clicked square is top right diagonal or bottom right diagonal
                    if pieceHDist > 0:
                        # If clicked position is in top right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 - pieceHDist:
                            # Top Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom right diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 + pieceHDist:
                            # Bottom Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                    # If clicked square is top left diagonal or bottom left diagonal
                    elif pieceHDist < 0:
                        # If clicked position is in top left diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 + pieceHDist:
                            # Top Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom left diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 - pieceHDist:
                            # Bottom Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                                # There is no other piece in diagonal
                                return True
                else:
                    totalVDist = clickedPos[1]//64
                    pieceVDist = totalVDist - currentPos[1]//64
                    
                    # If clicked square is top right diagonal or top left diagonal
                    if pieceVDist < 0:
                        # If clicked position is in top right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 - pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Top Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in top left diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Top Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                    # If clicked square is bottom right diagonal or bottom left diagonal
                    elif pieceVDist > 0:
                        # If clicked position is in bottom right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Bottom Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom left diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 - pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Bottom Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                                # There is no other piece in diagonal
                                return True
                                    

class Knight(Piece):
    def __init__(self, screen, colour, startPos):
        Piece.__init__(self, screen, colour, startPos, "Knight")
        super().summonPiece("Knight")

    # Check move is legal
    def validateMove(self, clickedSquare):
        currentPos = super().getPosition()
        # Clicked square is -2Y, -X
        if clickedSquare.y == currentPos[1]-128 and clickedSquare.x == currentPos[0]-64:
            for piece in pieceObjectList:
                if (clickedSquare.x, clickedSquare.y) == piece.getPosition():
                    super().takePiece(piece, knight=True)
            return True
        # Clicked square is -2Y, X
        if clickedSquare.y == currentPos[1]-128 and clickedSquare.x == currentPos[0]+64:
            for piece in pieceObjectList:
                if (clickedSquare.x, clickedSquare.y) == piece.getPosition():
                    super().takePiece(piece, knight=True)
            return True
        # Clicked square is 2Y, -X
        if clickedSquare.y == currentPos[1]+128 and clickedSquare.x == currentPos[0]-64:
            for piece in pieceObjectList:
                if (clickedSquare.x, clickedSquare.y) == piece.getPosition():
                    super().takePiece(piece, knight=True)
            return True
        # Clicked square is 2Y, X
        if clickedSquare.y == currentPos[1]+128 and clickedSquare.x == currentPos[0]+64:
            for piece in pieceObjectList:
                if (clickedSquare.x, clickedSquare.y) == piece.getPosition():
                    super().takePiece(piece, knight=True)
            return True
        # Clicked square is -2X, -Y
        if clickedSquare.x == currentPos[0]-128 and clickedSquare.y == currentPos[1]-64:
            for piece in pieceObjectList:
                if (clickedSquare.x, clickedSquare.y) == piece.getPosition():
                    super().takePiece(piece, knight=True)
            return True
        # Clicked square is -2X, Y
        if clickedSquare.x == currentPos[0]-128 and clickedSquare.y == currentPos[1]+64:
            for piece in pieceObjectList:
                if (clickedSquare.x, clickedSquare.y) == piece.getPosition():
                    super().takePiece(piece, knight=True)
            return True
        # Clicked square is 2X, -Y
        if clickedSquare.x == currentPos[0]+128 and clickedSquare.y == currentPos[1]-64:
            for piece in pieceObjectList:
                if (clickedSquare.x, clickedSquare.y) == piece.getPosition():
                    super().takePiece(piece, knight=True)
            return True
        # Clicked square is 2X, Y
        if clickedSquare.x == currentPos[0]+128 and clickedSquare.y == currentPos[1]+64:
            for piece in pieceObjectList:
                if (clickedSquare.x, clickedSquare.y) == piece.getPosition():
                    super().takePiece(piece, knight=True)
            return True
        

class Rook(Piece):
    def __init__(self, screen, colour, startPos):
        Piece.__init__(self, screen, colour, startPos, "Rook")
        super().summonPiece("Rook")

    # Check move is legal
    def validateMove(self, clickedSquare):
        currentPos = super().getPosition()
        # In same file?
        if clickedSquare.x == currentPos[0]:
            for piece in pieceObjectList:
                piecePos = piece.getPosition()
                if piecePos[0] == currentPos[0]:
                    if piece != selectedPiece:
                        # Piece to top
                        if clickedSquare.y < currentPos[1]:
                            if piecePos[1] > clickedSquare.y and piecePos[1] < currentPos[1]:
                                # Piece is in the way
                                return False
                            elif piecePos[1] == clickedSquare.y:
                                # Take piece
                                super().takePiece(piece, rook=True)
                                return True
                        # Piece to bottom
                        elif clickedSquare.y > currentPos[1]:
                            if piecePos[1] < clickedSquare.y and piecePos[1] > currentPos[1]:
                                # Piece is in the way
                                return False
                            elif piecePos[1] == clickedSquare.y:
                                # Take piece
                                super().takePiece(piece, rook=True)
                                return True
            # Piece is not in the way
            return True
                
        # In same rank?             
        elif clickedSquare.y == currentPos[1]:
            for piece in pieceObjectList:
                piecePos = piece.getPosition()
                if piecePos[1] == currentPos[1]:
                    if piece != selectedPiece:
                        # Piece to left
                        if clickedSquare.x < currentPos[0]:
                            if piecePos[0] > clickedSquare.x and piecePos[0] < currentPos[0]:
                                # Piece is in the way
                                return False
                            elif piecePos[0] == clickedSquare.x:
                                # Take piece
                                super().takePiece(piece, rook=True)
                                return True
                        # Piece to right
                        elif clickedSquare.x > currentPos[0]:
                            if piecePos[0] < clickedSquare.x and piecePos[0] > currentPos[0]:
                                # Piece is in the way
                                return False
                            elif piecePos[0] == clickedSquare.x:
                                # Take piece
                                super().takePiece(piece, rook=True)
                                return True
            # Piece is not in the way
            return True

    # Castling
    def castle(self):
        pass

class Queen(Piece):
    def __init__(self, screen, colour, startPos):
        Piece.__init__(self, screen, colour, startPos, "Queen")
        super().summonPiece("Queen")

    # Check move is legal
    def validateMove(self, clickedSquare):
        currentPos = super().getPosition()
        clickedPos = (clickedSquare.x, clickedSquare.y)
        
        if super().getColour() == "White":
            startFromX = False


            # In same file?
            if clickedSquare.x == currentPos[0]:
                for piece in pieceObjectList:
                    piecePos = piece.getPosition()
                    if piecePos[0] == currentPos[0]:
                        if piece != selectedPiece:
                            # Piece to top
                            if clickedSquare.y < currentPos[1]:
                                if piecePos[1] > clickedSquare.y and piecePos[1] < currentPos[1]:
                                    # Piece is in the way
                                    return False
                                elif piecePos[1] == clickedSquare.y:
                                    # Take piece
                                    super().takePiece(piece, rook=True)
                                    return True
                            # Piece to bottom
                            elif clickedSquare.y > currentPos[1]:
                                if piecePos[1] < clickedSquare.y and piecePos[1] > currentPos[1]:
                                    # Piece is in the way
                                    return False
                                elif piecePos[1] == clickedSquare.y:
                                    # Take piece
                                    super().takePiece(piece, rook=True)
                                    return True
                # Piece is not in the way
                return True
                    
            # In same rank?             
            elif clickedSquare.y == currentPos[1]:
                for piece in pieceObjectList:
                    piecePos = piece.getPosition()
                    if piecePos[1] == currentPos[1]:
                        if piece != selectedPiece:
                            # Piece to left
                            if clickedSquare.x < currentPos[0]:
                                if piecePos[0] > clickedSquare.x and piecePos[0] < currentPos[0]:
                                    # Piece is in the way
                                    return False
                                elif piecePos[0] == clickedSquare.x:
                                    # Take piece
                                    super().takePiece(piece, rook=True)
                                    return True
                            # Piece to right
                            elif clickedSquare.x > currentPos[0]:
                                if piecePos[0] < clickedSquare.x and piecePos[0] > currentPos[0]:
                                    # Piece is in the way
                                    return False
                                elif piecePos[0] == clickedSquare.x:
                                    # Take piece
                                    super().takePiece(piece, rook=True)
                                    return True
                # Piece is not in the way
                return True
            
            
            # Get every square from one corner to another corner of bishops diagonal
            for i in range(0,7):
                if clickedPos[0]//64 < clickedPos[1]//64:
                    startFromX = True

                # If diagonal ends on top of board or side
                if startFromX == True:
                    totalHDist = clickedPos[0]//64
                    pieceHDist = totalHDist - currentPos[0]//64

                    # If clicked square is top right diagonal or bottom right diagonal
                    if pieceHDist > 0:
                        # If clicked position is in top right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 - pieceHDist:
                            # Top Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom right diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 + pieceHDist:
                            # Bottom Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                    elif pieceHDist < 0:
                        # If clicked position is in top left diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 + pieceHDist:
                            # Top Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom left diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 - pieceHDist:
                            # Bottom Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                                # There is no other piece in diagonal
                                return True
                else:
                    totalVDist = clickedPos[1]//64
                    pieceVDist = totalVDist - currentPos[1]//64
                    
                    # If clicked square is top right diagonal or top left diagonal
                    if pieceVDist < 0:
                        # If clicked position is in top right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 - pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Top Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom right diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Top Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                    elif pieceVDist > 0:
                        # If clicked position is in bottom right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Bottom Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom left diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 - pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Bottom Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "White":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                                # There is no other piece in diagonal
                                return True

                            
        else:

            
            startFromX = False


            # In same file?
            if clickedSquare.x == currentPos[0]:
                for piece in pieceObjectList:
                    piecePos = piece.getPosition()
                    if piecePos[0] == currentPos[0]:
                        if piece != selectedPiece:
                            # Piece to top
                            if clickedSquare.y < currentPos[1]:
                                if piecePos[1] > clickedSquare.y and piecePos[1] < currentPos[1]:
                                    # Piece is in the way
                                    return False
                                elif piecePos[1] == clickedSquare.y:
                                    # Take piece
                                    super().takePiece(piece, rook=True)
                                    return True
                            # Piece to bottom
                            elif clickedSquare.y > currentPos[1]:
                                if piecePos[1] < clickedSquare.y and piecePos[1] > currentPos[1]:
                                    # Piece is in the way
                                    return False
                                elif piecePos[1] == clickedSquare.y:
                                    # Take piece
                                    super().takePiece(piece, rook=True)
                                    return True
                # Piece is not in the way
                return True
                    
            # In same rank?             
            elif clickedSquare.y == currentPos[1]:
                for piece in pieceObjectList:
                    piecePos = piece.getPosition()
                    if piecePos[1] == currentPos[1]:
                        if piece != selectedPiece:
                            # Piece to left
                            if clickedSquare.x < currentPos[0]:
                                if piecePos[0] > clickedSquare.x and piecePos[0] < currentPos[0]:
                                    # Piece is in the way
                                    return False
                                elif piecePos[0] == clickedSquare.x:
                                    # Take piece
                                    super().takePiece(piece, rook=True)
                                    return True
                            # Piece to right
                            elif clickedSquare.x > currentPos[0]:
                                if piecePos[0] < clickedSquare.x and piecePos[0] > currentPos[0]:
                                    # Piece is in the way
                                    return False
                                elif piecePos[0] == clickedSquare.x:
                                    # Take piece
                                    super().takePiece(piece, rook=True)
                                    return True
                # Piece is not in the way
                return True


            
            # Get every square from one corner to another corner of bishops diagonal
            for i in range(0,7):
                if clickedPos[0]//64 > clickedPos[1]//64:
                    startFromX = True

                # If diagonal ends on top of board or side
                if startFromX == True:
                    totalHDist = clickedPos[0]//64
                    pieceHDist = totalHDist - currentPos[0]//64

                    # If clicked square is top right diagonal or bottom right diagonal
                    if pieceHDist > 0:
                        # If clicked position is in top right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 - pieceHDist:
                            # Top Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom right diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 + pieceHDist:
                            # Bottom Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                    # If clicked square is top left diagonal or bottom left diagonal
                    elif pieceHDist < 0:
                        # If clicked position is in top left diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 + pieceHDist:
                            # Top Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom left diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceHDist and clickedPos[1]//64 == currentPos[1]//64 - pieceHDist:
                            # Bottom Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                                # There is no other piece in diagonal
                                return True
                else:
                    totalVDist = clickedPos[1]//64
                    pieceVDist = totalVDist - currentPos[1]//64
                    
                    # If clicked square is top right diagonal or top left diagonal
                    if pieceVDist < 0:
                        # If clicked position is in top right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 - pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Top Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in top left diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 + pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Top Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]-(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] > piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                    # If clicked square is bottom right diagonal or bottom left diagonal
                    elif pieceVDist > 0:
                        # If clicked position is in bottom right diagonal of current piece
                        if clickedPos[0]//64 == currentPos[0]//64 + pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Bottom Right
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]+(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] < piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                            # There is no other piece in diagonal
                            return True
                        # If clicked position is in bottom left diagonal of current piece
                        elif clickedPos[0]//64 == currentPos[0]//64 - pieceVDist and clickedPos[1]//64 == currentPos[1]//64 + pieceVDist:
                            # Bottom Left
                            for j in range(currentPos[0]//64, 8):
                                jNew = j-((currentPos[0]//64)-1)
                                for piece in pieceObjectList:
                                    piecePos = piece.getPosition()
                                    if piecePos[0] == currentPos[0]-(jNew*64) and piecePos[1] == currentPos[1]+(jNew*64):
                                        # Piece is diagonal
                                        if clickedPos[0] > piecePos[0] and clickedPos[1] < piecePos[1]:
                                            # Piece is not in the way
                                            return True
                                        elif clickedPos == piecePos:
                                            # Piece is on clicked square
                                            if piece.getColour() != "Black":
                                                super().takePiece(piece)
                                                return True
                                        else:
                                            # Piece is in the way
                                            return False
                                # There is no other piece in diagonal
                                return True

class King(Piece):
    def __init__(self, screen, colour, startPos):
        Piece.__init__(self, screen, colour, startPos, "King")
        super().summonPiece("King")

    # Check move is legal
    def validateMove(self, clickedSquare):
        currentPos = self.getPosition()
        
        # If clicked square is -X, -Y
        if clickedSquare.x == currentPos[0]-64 and clickedSquare.y == currentPos[1]-64:
            # Is piece in clicked square
            for piece in pieceObjectList:
                piecePos = piece.getPosition()
                if (piecePos[0], piecePos[1]) == (clickedSquare.x, clickedSquare.y):
                    super().takePiece(piece)
                    return True
            return True

        # If clicked square is -X
        if clickedSquare.x == currentPos[0]-64 and clickedSquare.y == currentPos[1]:
            # Is piece in clicked square
            for piece in pieceObjectList:
                piecePos = piece.getPosition()
                if (piecePos[0], piecePos[1]) == (clickedSquare.x, clickedSquare.y):
                    super().takePiece(piece, knight=True)
                    return True
            return True

        # If clicked square is -X, Y
        if clickedSquare.x == currentPos[0]-64 and clickedSquare.y == currentPos[1]+64:
            # Is piece in clicked square
            for piece in pieceObjectList:
                piecePos = piece.getPosition()
                if (piecePos[0], piecePos[1]) == (clickedSquare.x, clickedSquare.y):
                    super().takePiece(piece)
                    return True
            return True

        # If clicked square is X, -Y
        if clickedSquare.x == currentPos[0]+64 and clickedSquare.y == currentPos[1]-64:
            # Is piece in clicked square
            for piece in pieceObjectList:
                piecePos = piece.getPosition()
                if (piecePos[0], piecePos[1]) == (clickedSquare.x, clickedSquare.y):
                    super().takePiece(piece)
                    return True
            return True

        # If clicked square is X
        if clickedSquare.x == currentPos[0]+64 and clickedSquare.y == currentPos[1]:
            # Is piece in clicked square
            for piece in pieceObjectList:
                piecePos = piece.getPosition()
                if (piecePos[0], piecePos[1]) == (clickedSquare.x, clickedSquare.y):
                    super().takePiece(piece, knight=True)
                    return True
            return True

        # If clicked square is X, Y
        if clickedSquare.x == currentPos[0]+64 and clickedSquare.y == currentPos[1]+64:
            # Is piece in clicked square
            for piece in pieceObjectList:
                piecePos = piece.getPosition()
                if (piecePos[0], piecePos[1]) == (clickedSquare.x, clickedSquare.y):
                    super().takePiece(piece)
                    return True
            return True

        # If clicked square is -Y
        if clickedSquare.x == currentPos[0] and clickedSquare.y == currentPos[1]-64:
            # Is piece in clicked square
            for piece in pieceObjectList:
                piecePos = piece.getPosition()
                if (piecePos[0], piecePos[1]) == (clickedSquare.x, clickedSquare.y):
                    super().takePiece(piece, knight=True)
                    return True
            return True

        # If clicked square is Y
        if clickedSquare.x == currentPos[0] and clickedSquare.y == currentPos[1]+64:
            # Is piece in clicked square
            for piece in pieceObjectList:
                piecePos = piece.getPosition()
                if (piecePos[0], piecePos[1]) == (clickedSquare.x, clickedSquare.y):
                    super().takePiece(piece, knight=True)
                    return True
            return True

    # Called if king is in check
    def inCheck(self):
        pass

    # Called if checkmate
    def checkmate(self):
        pass

def ClearWindowContents():
    childList = window.winfo_children()
    for child in childList:
        child.destroy()

def createChessGrid(screen):
    global gameRunning
    
    gridColour = False
    colour1 = "#f0e68c"
    colour2 = "#c04000"
    selectedFile = -1
    selectedRank = -1
    
    for item in gridList[0]:
        selectedRank += 1
        selectedFile = -1
        for newItem in gridList[1]:
            selectedFile += 1
            if selectedRank % 2 == 0:
                if gridColour == False:
                    square = draw.rect(screen, colour1, Rect(selectedFile*64,selectedRank*64,64,64))
                    gridRectList.append(square)
                    gridColour = not gridColour
                elif gridColour == True:
                    square = draw.rect(screen, colour2, Rect(selectedFile*64,selectedRank*64,64,64))
                    gridRectList.append(square)
                    gridColour = not gridColour
            else:
                if gridColour == False:
                    square = draw.rect(screen, colour2, Rect(selectedFile*64,selectedRank*64,64,64))
                    gridRectList.append(square)
                    gridColour = not gridColour
                elif gridColour == True:
                    square = draw.rect(screen, colour1, Rect(selectedFile*64,selectedRank*64,64,64))
                    gridRectList.append(square)
                    gridColour = not gridColour

    # Summon pieces
    for i in range(len(gridList[0])):
        # Pawns
        pawn = Pawn(screen, "White", gridList[0][i]+"2")
        pawn = Pawn(screen, "Black", gridList[0][i]+"7")
    
    # Kings
    king = King(screen, "White", "e1")
    king = King(screen, "Black", "e8")

    # Queens
    queen = Queen(screen, "White", "d1")
    queen = Queen(screen, "Black", "d8")

    # Bishops
    bishop = Bishop(screen, "White", "c1")
    bishop = Bishop(screen, "White", "f1")
    bishop = Bishop(screen, "Black", "c8")
    bishop = Bishop(screen, "Black", "f8")

    # Knights
    knight = Knight(screen, "White", "b1")
    knight = Knight(screen, "White", "g1")
    knight = Knight(screen, "Black", "b8")
    knight = Knight(screen, "Black", "g8")

    # Rooks
    rook = Rook(screen, "White", "a1")
    rook = Rook(screen, "White", "h1")
    rook = Rook(screen, "Black", "a8")
    rook = Rook(screen, "Black", "h8")

    gameRunning = True
    
    display.flip()

def TwoPlayer():
    global selectedPiece
    global playerOne
    
    # Destroy TKinter window
    window.destroy()

    # Pygame initialisation
    bg_colour = (125,125,125)
    screen_size = (512,512)
    screen = display.set_mode(screen_size)
    display.set_caption("Chess")
    screen.fill(bg_colour)
    display.flip()

    createChessGrid(screen)

    while gameRunning:
        events = event.get()
        for ev in events:
            if ev.type == MOUSEBUTTONUP:
                index=-1
                for piece in pieceObjectList:
                    index += 1
                    if piece.selectPiece(index) == True:
                        selectedPiece = piece
                        
                # Grid square clicked
                if selectedPiece != None:
                    mpos = mouse.get_pos()
                    for square in gridRectList:
                        is_touching = square.collidepoint(mpos)
                        if is_touching == True and (square.x, square.y) != selectedPiece.getPosition():
                            if selectedPiece.validateMove(square):
                                # Move piece to square
                                selectedPiece.movePiece(square, selectedPiece.getName(), selectedPiece.getColour())
                                selectedPiece = None
                                if playerOne == True:
                                    playerOne = False
                                else:
                                    playerOne = True

def HelpMenu():
    ClearWindowContents()

    # Procedures
    def summonClose():
        closeBTN = Button(window, text="X", font="50", bg="#ff0000", fg="#ffffff", command=LoadMenu)
        closeBTN.place(width=50, height=50, x=462, y=0)

    def summonBackButton():
        backBTN = Button(window, text="Back", font="50", bg="#808080", fg="#ffffff", command=HelpMenu)
        backBTN.place(width=50, height=50, x=0, y=0)
    
    def basicMoves():
        ClearWindowContents()
        summonClose()
        summonBackButton()
        
        # Instantiate text labels
        kingMovement = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-The king moves exactly one square horizontally, vertically, or \ndiagonally")
        kingMovement.place(width=480,height=50, x=16, y=50)
        rookMovement = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-A rook moves any number of vacant squares horizontally or vertically")
        rookMovement.place(width=480,height=50, x=16, y=100)
        bishopMovement = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-A bishop moves any number of vacant squares diagonally")
        bishopMovement.place(width=480,height=50, x=16, y=150)
        queenMovement = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-The queen moves any number of vacant squares horizontally, \nvertically, or diagonally")
        queenMovement.place(width=480,height=50, x=16, y=200)
        knightMovement = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-A knight moves to one of the nearest squares not on the same \nrank, file, or diagonal")
        knightMovement.place(width=480,height=50, x=16, y=250)
        pawnMovement = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-A pawn moves straight forward one square, if that square is vacant. \nIf it has not yet moved, a pawn also has the option of moving \ntwo squares straight forward, prodivded both \nsquares are vacant. Pawns cannot move backwards. \nA pawn can capture an enemy piece either of the two \nsquares diagonally in front of the pawn. (See En Passant)")
        pawnMovement.place(width=480,height=125, x=16, y=300)

    def castling():
        ClearWindowContents()
        summonClose()
        summonBackButton()

        # Instantiate text labels
        ruleOne = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-Castling consists of moving the king two\nsquares towards a rook, then\nplacing the rook on the other side of\nthe king, adjacent to it. It is\nnot allowed to move both king and rook in\nthe same time. The following conditions must hold:")
        ruleOne.place(width=480, height=125, x=16, y=50)
        ruleTwo = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-The king and rook involved in castling must\nnot have previously been moved")
        ruleTwo.place(width=480, height=50, x=16, y=175)
        ruleThree = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-There must be no pieces between the king and rook")
        ruleThree.place(width=480, height=50, x=16, y=225)
        ruleFour = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-The king may not currently be under attack, nor may the king\npass through or end up in a square that is under attack")
        ruleFour.place(width=480, height=50, x=16, y=275)
        ruleFive = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-The castling must be kingside or queenside")
        ruleFive.place(width=480, height=50, x=16, y=325)

    def enPassant():
        ClearWindowContents()
        summonClose()
        summonBackButton()

        # Instantiate text labels
        ruleOne = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-When a pawn advances two squares on its inital move and ends\nthe turn adjacent to an enemy pawn on the same rank, it\nmay be captured en passant by the enemy pawn as if it had\nmoved only one square. This capture is legal only on\nthe move immediately following the pawns advance")
        ruleOne.place(width=480, height=125, x=16, y=50)

    def promotion():
        ClearWindowContents()
        summonClose()
        summonBackButton()

        # Instantiate text labels
        ruleOne = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-If a player advances a pawn to its eighth rank, the pawn is promoted\nto a queen, rook, bishop, or knight")
        ruleOne.place(width=480, height=125, x=16, y=50)

    def check():
        ClearWindowContents()
        summonClose()
        summonBackButton()

        # Instantiate text labels
        ruleOne = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-A king is in check when it is under attack by at least one enemy piece.\nWhen a king is in check it is illegal to make a move that places\nor leaves one's king in check")
        ruleOne.place(width=480, height=125, x=16, y=50)

    def checkMate():
        ClearWindowContents()
        summonClose()
        summonBackButton()

        # Instantiate text labels
        ruleOne = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-If a player's king is in check and there is no legal move that\nplayer can make to escape check, then the king is in checkmate.\nThis ends the game and that player loses.")
        ruleOne.place(width=480, height=125, x=16, y=50)

    def resigning():
        ClearWindowContents()
        summonClose()
        summonBackButton()

        # Instantiate text labels
        ruleOne = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-At any time a player may resign. This ends\nthe game and the opponent wins")
        ruleOne.place(width=480, height=125, x=16, y=50)

    def draw():
        ClearWindowContents()
        summonClose()
        summonBackButton()

        # Instantiate text labels
        ruleOne = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-The game ends in a draw if any of these conditions occur:")
        ruleOne.place(width=480, height=50, x=16, y=50)
        ruleTwo = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-The player to move is not in check and has no legal move (stalemate)")
        ruleTwo.place(width=480, height=50, x=16, y=100)
        ruleThree = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-The game reaches a dead position")
        ruleThree.place(width=480, height=50, x=16, y=150)
        ruleFour = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-Both players agree to draw")
        ruleFour.place(width=480, height=50, x=16, y=200)
        ruleFive = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-The same board position has occured 3 times")
        ruleFive.place(width=480, height=50, x=16, y=250)

    def flagFall():
        ClearWindowContents()
        summonClose()
        summonBackButton()

        # Instantiate text labels
        ruleOne = Label(window, bg="#80b3ff", fg="#ffffff", font="50", text="-If a player runs out of time, they lose the game")
        ruleOne.place(width=480, height=50, x=16, y=50)
    
    # Instantiate buttons
    summonClose()
    
    basicMovesBTN = Button(window, text="Basic Moves", font="50", border=5, command=basicMoves)
    basicMovesBTN.place(width=380, height=50, x=66, y=31)
    castlingBTN = Button(window, text="Castling", font="50", border=5, command=castling)
    castlingBTN.place(width=380, height=50, x=66, y=81)
    enPassantBTN = Button(window, text="En Passant", font="50", border=5, command=enPassant)
    enPassantBTN.place(width=380, height=50, x=66, y=131)
    promotionBTN = Button(window, text="Promotion", font="50", border=5, command=promotion)
    promotionBTN.place(width=380, height=50, x=66, y=181)
    checkBTN = Button(window, text="Check", font="50", border=5, command=check)
    checkBTN.place(width=380, height=50, x=66, y=231)
    checkmateBTN = Button(window, text="Checkmate", font="50", border=5, command=checkMate)
    checkmateBTN.place(width=380, height=50, x=66, y=281)
    resigningBTN = Button(window, text="Resigning", font="50", border=5, command=resigning)
    resigningBTN.place(width=380, height=50, x=66, y=331)
    drawBTN = Button(window, text="Drawing", font="50", border=5, command=draw)
    drawBTN.place(width=380, height=50, x=66, y=381)
    flagFallBTN = Button(window, text="Flag-Fall", font="50", border=5, command=flagFall)
    flagFallBTN.place(width=380, height=50, x=66, y=431)

def LoadMenu():
    # Clear contents of previous screen
    ClearWindowContents()
    
    # Instantiate contents of menu
                                    # Buttons
    twoPlayerButton = Button(window, text="2 Player", font="50", border=5, command=TwoPlayer)
    twoPlayerButton.place(width=380, height=75, x=66, y=56)
    AIButton = Button(window, text="AI", font="50", border=5)
    AIButton.place(width=380, height=75, x=66, y=156)
    statisticsButton = Button(window, text="Statistics", font="50", border=5)
    statisticsButton.place(width=380, height=75, x=66, y=256)
    helpButton = Button(window, text="How to Play", font="50", border=5, command=HelpMenu)
    helpButton.place(width=380, height=75, x=66, y=356)

    window.mainloop()






### LOGIN/REGISTER SYSTEM ###
def Login():
    # Procedures
    def errorText(errorString):
        errorHeader = Label(window, bg="#80b3ff", fg="#ff3030", font="32", text=errorString)
        errorHeader.place(width=300,height=20, x=106, y=425)
    
    # Button Commands
    def hashDetails():
        # Hashes reverse username + password
        def hashFunction(stringToHash):
            hashedDetails = ""
            detailsFound = False
            total = 0
            for char in stringToHash:
                total += ord(char)
                total *= ord(char)
                hashvalue = total % 1000000000
                hashvalue **= len(stringToHash)
                hashvalue = hex(hashvalue).upper()
                hashedDetails = hashvalue

            # Compare to file
            detailsFile = open("Details.txt","r")
            for line in detailsFile.readlines():
                if line == usernameInputBox.get() + hashedDetails:
                    detailsFound = True
                    LoadMenu()
            
            if detailsFound == False:
                errorText("Incorrect username or password")

            detailsFile.close()

        # Reverses username + password
        def reverseDetails():
            result = ""
            combinedDetails = usernameInputBox.get() + passwordInputBox.get()
            for char in combinedDetails:
                result = char + result
            
            hashFunction(result)
            
        reverseDetails()

    # Clear window and call Register()
    def startRegister():
        ClearWindowContents()
        Register()
    
    
    # Boxes
    usernameInputBox = Entry(window, border=5, font="100")
    usernameInputBox.place(width=350, height=32, x=81, y=50)
    passwordInputBox = Entry(window, border=5, font="100", show="*")
    passwordInputBox.place(width=350, height=32, x=81, y=150)

    # Headers
    usernameHeader = Label(window, text="Username", bg="#80b3ff", fg="#ffffff", font="32")
    usernameHeader.place(width=70, height=15, x=81, y=30)
    passwordHeader = Label(window, text="Password", bg="#80b3ff", fg="#ffffff", font="32")
    passwordHeader.place(width=70, height=15, x=81, y=130)

    # Buttons
    submitButton = Button(window, text="Submit", font="50", border=5, command=hashDetails)
    submitButton.place(width=100, height=50, x=206, y=250)
    registerButton = Button(window, text="Register new account", font="50", border=5, command=startRegister)
    registerButton.place(width=250, height=50, x=131, y=350)

    window.mainloop()


def Register():
    detailsFile = open("Details.txt","r+")
    lines = detailsFile.readlines()
    
    # Procedures
    def errorText(errorString):
        errorHeader = Label(window, bg="#80b3ff", fg="#ff3030", font="32", text=errorString)
        errorHeader.place(width=300, height=20, x=106, y=475)
    
    # Button Commands
    def submit():
        # Write hashed details to file
        def writeDetails(hashedDetails):
            detailsFile.write("\n" + usernameInputBox.get() + hashedDetails)
            detailsFile.close()
            LoadMenu()
        
        # Hashes reverse username + password
        def hashFunction(stringToHash):
            hashedDetails = ""
            total = 0
            for char in stringToHash:
                total += ord(char)
                total *= ord(char)
                hashvalue = total % 1000000000
                hashvalue **= len(stringToHash)
                hashvalue = hex(hashvalue).upper()
                hashedDetails = hashvalue

            writeDetails(hashedDetails)

        # Reverses username + password
        def reverseDetails():
            result = ""
            combinedDetails = usernameInputBox.get() + passwordInputBox.get()
            for char in combinedDetails:
                result = char + result
            
            hashFunction(result)

        # Check that username doesn't already exist
        def checkUsername():
            usernameExists = False
            if len(lines) > 0:
                for line in lines:
                    if usernameInputBox.get() in line:
                        usernameExists = True
                        errorText("Username already exists")
                if usernameExists == False:
                    reverseDetails()
            else:
                reverseDetails()

        # Check confirm password matches password
        def checkPassword():
            if confirmPasswordInputBox.get() != passwordInputBox.get():
                errorText("Passwords don't match")
            else:
                checkUsername()
            
        checkPassword()

    # Clear window and call Login()
    def startLogin():
        ClearWindowContents()
        Login()
    
    # Boxes
    usernameInputBox = Entry(window, border=5, font="100")
    usernameInputBox.place(width=350, height=32, x=81, y=50)
    passwordInputBox = Entry(window, border=5, font="100", show="*")
    passwordInputBox.place(width=350, height=32, x=81, y=150)
    confirmPasswordInputBox = Entry(window, border=5, font="100", show="*")
    confirmPasswordInputBox.place(width=350, height=32, x=81, y=250)

    # Headers
    usernameHeader = Label(window, text="Username", bg="#80b3ff", fg="#ffffff", font="32")
    usernameHeader.place(width=70, height=15, x=81, y=30)
    passwordHeader = Label(window, text="Password", bg="#80b3ff", fg="#ffffff", font="32")
    passwordHeader.place(width=70, height=15, x=81, y=130)
    confirmPasswordHeader = Label(window, text="Confirm Password", bg="#80b3ff", fg="#ffffff", font="32")
    confirmPasswordHeader.place(width=128, height=15, x=81, y=230)

    # Buttons
    submitButton = Button(window, text="Submit", font="50", border=5, command=submit)
    submitButton.place(width=100, height=50, x=206, y=325)
    loginButton = Button(window, text="Login to account", font="50", border=5, command=startLogin)
    loginButton.place(width=250, height=50, x=131, y=400)
    
    window.mainloop()
    
Login()
