''''
MalakElGendy (MakeMove,SquareUnderAttack,PossibleMoves,ClassMove,Rook)
HossamKhairy
(ValidMoves,Incheck,CastleRight)
Roshan Helmy
(PawnMoves,Promotion,Enpassant,Castling)
ZiadYakout
(King&QueenMoves,GetSides Moves)
OmarMedhat
(Pinchecks-Bishop-Night)
'''
class GameState():
    def __init__(self):
        #han7ot 2l pieces kolha w 2l -- da morab3 fade
        self.board=[
            ["BR","BN","BB","BQ","BK","BB","BN","BR"],
            ["BP","BP","BP","BP","BP","BP","BP","BP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["WP","WP","WP","WP","WP","WP","WP","WP"],
            ["WR","WN","WB","WQ","WK","WB","WN","WR"]
        ]
        self.moveFunctions={'P':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,
                            'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}
        self.whiteToMove=True
        self.movelog=[]
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)
        self.checkMate=False
        self.staleMate=False
        self.checkk=False
        self.pins=[]
        self.checks=[]
        self.enpassantPossible=()
        self.currentCastleRights=CastleRight(True,True,True,True)
        self.castleRightsLog=[CastleRight(self.currentCastleRights.wks,self.currentCastleRights.bks
                                          ,self.currentCastleRights.wqs,self.currentCastleRights.bqs)]

    # method bt handle 2l moves fe 2l board w t update kol move w 2l tania
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove

        # Update king's location
        if move.pieceMoved == 'WK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'BK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # Handle pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # Handle en passant
        if move.enpassantPossible:
            self.board[move.startRow][move.endCol] = "--"  # Capture the pawn en passant
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.endCol)
        else:
            self.enpassantPossible = ()

        # Handle castling
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # King-side
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--"
            else:  # Queen-side
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"

        # Update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRight(
            self.currentCastleRights.wks, self.currentCastleRights.bks,
            self.currentCastleRights.wqs, self.currentCastleRights.bqs))

# method bt5alene 2arg3 fe move 3amltha (optional tab3an msh 2asasia fe 2l chess)
    def undoMove(self):
        if len(self.movelog)!=0:
            move =self.movelog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteToMove=not self.whiteToMove
            if move.pieceMoved == 'WK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'BK':
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.enpassantPossible:
                self.board[move.endRow][move.endCol]='--'
                self.board[move.startRow][move.endCol]=move.pieceCaptured
                self.enpassantPossible=(move.endRow,move.endCol)
            if move.pieceMoved[1]=='P' and abs(move.startRow-move.endRow)==2:
                self.enpassantPossible=()
            self.castleRightsLog.pop()
            self.currentCastleRights=self.castleRightsLog[-1]
            if move.isCastleMove:
                if move.endCol-move.startCol==2:
                    self.board[move.endRow][move.endCol+1]=self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1]='--'
                else:
                    self.board[move.endRow][move.endCol-2]=self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol + 1]='--'

    def updateCastleRights(self,move):
        if move.pieceMoved=='WK':
            self.currentCastleRights.wks=False
            self.currentCastleRights.wqs=False
        elif move.pieceMoved=='BK':
            self.currentCastleRights.bks=False
            self.currentCastleRights.bqs=False
        elif move.pieceMoved=='WR':
            if move.startRow==7:
                if move.startCol==0:
                    self.currentCastleRights.wqs=False
                elif move.startCol==7:
                    self.currentCastleRights.wks=False
        elif move.pieceMoved=='BR':
            if move.startRow==0:
                if move.startCol==0:
                    self.currentCastleRights.bqs=False
                elif move.startCol==7:
                    self.currentCastleRights.bks=False


# method bt5alene 2ashof 2l valid moves l kol piece w 2ele btt3alm b 2l loon 2l 2a5dar fe 2l board
    def getValidMoves(self):
        tempEnPassantPossible=self.enpassantPossible
        tempCastleRights=CastleRight(self.currentCastleRights.wks,self.currentCastleRights.bks,
                                     self.currentCastleRights.wqs,self.currentCastleRights.bqs)
        moves=self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)

        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove=not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove=not self.whiteToMove
            self.undoMove()
        if len(moves)==0:
            if self.inCheck():
                self.checkMate=True
            else:
                self.staleMate=True
        if self.inCheck():
            self.checkk=True
        self.enpassantPossible=tempEnPassantPossible
        self.currentCastleRights=tempCastleRights
        return moves
# method btshof hal 2l king in check mate wala la2
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
    # bashof hal 2l morab3 da under atack wala la2 b 2ene 2ashof kol 2l possible moves w 2ashof hal wa7da mnhom btsaweh wala la2
    def squareUnderAttack(self,r,c):
        self.whiteToMove=not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove=not self.whiteToMove
        for move in oppMoves:
            if move.endRow==r and move.endCol==c:
                return True
        return False

# bashof kol 2l possible moves hena
    def getAllPossibleMoves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                turn =self.board[i][j][0]
                if(turn=='W' and self.whiteToMove) or (turn=='B' and not self.whiteToMove):
                    piece=self.board[i][j][1]
                    self.moveFunctions[piece](i,j,moves)
        return moves
# 2ele gai ba2a implementation l kol piece mn 2el pieces
    def getPawnMoves(self,r,c,moves):

        piecePinned=False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecePinned=True
                pinDirection=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            if self.board[r-1][c]=='--':
                if not piecePinned or pinDirection==(-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r==6 and self.board[r-2][c]=='--':
                       moves.append(Move((r,c),(r-2,c),self.board))
            if c-1>=0:
                if self.board[r-1][c-1][0]=='B':
                    if not piecePinned or pinDirection == (-1, -1):
                       moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1)==self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board,enpassantPossible=True))

            if c+1<=7:
                if self.board[r-1][c+1][0]=='B':
                    if not piecePinned or pinDirection==(-1,1):
                       moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1)==self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c+1),self.board,enpassantPossible=True))
        else:
            if self.board[r + 1][c] == '--':
                   if not piecePinned or pinDirection == (1, 0):
                       moves.append(Move((r, c), (r + 1, c), self.board))
                       if r == 1 and self.board[r + 2][c] == '--':
                          moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'W':
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1,c-1)==self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c-1),self.board,enpassantPossible=True))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'W':
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r+1,c+1)==self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c+1),self.board,enpassantPossible=True))

    def getRookMoves(self,r,c,moves):
        piecePinned=False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecePinned=True
                pinDirection=(self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1]!='Q':
                    self.pins.remove(self.pins[i])
                break


        directions=((-1,0),(0,-1),(1,0),(0,1))
        enemyColor='B' if self.whiteToMove else 'W'
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0<=endRow <8 and 0<=endCol<8:
                    if not piecePinned or pinDirection==d or pinDirection==(-d[0],-d[1]):
                       endPiece=self.board[endRow][endCol]
                       if endPiece=='--':
                           moves.append(Move((r,c),(endRow,endCol),self.board))
                       elif endPiece[0]==enemyColor:
                           moves.append(Move((r,c),(endRow,endCol),self.board))
                           break
                       else:
                           break
                else:
                    break
    def getKnightMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        knightmoves=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor='W' if self.whiteToMove else 'B'
        for m in knightmoves:
            endRow=r+m[0]
            endCol=c+m[1]
            if 0<=endRow<8 and 0<=endCol<8:
                if not piecePinned:
                   endPiece=self.board[endRow][endCol]
                   if endPiece[0]!=allyColor:
                       moves.append(Move((r,c),(endRow,endCol),self.board))
    def getBishopMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = 'B' if self.whiteToMove else 'W'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection==d or pinDirection==(-d[0],-d[1]):
                       endPiece = self.board[endRow][endCol]
                       if endPiece == '--':
                           moves.append(Move((r, c), (endRow, endCol), self.board))
                       elif endPiece[0] == enemyColor:
                           moves.append(Move((r, c), (endRow, endCol), self.board))
                           break
                       else:
                           break
                else:
                    break
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    def getKingMoves(self,r,c,moves):
        kingMoves=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor='W'if self.whiteToMove else 'B'
        for i in range(8):
            endRow=r+kingMoves[i][0]
            endCol=c+kingMoves[i][1]
            if 0<=endRow<8 and 0<= endCol <8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return  # Cannot castle while in check

        if self.whiteToMove:
            if self.currentCastleRights.wks:  # White king-side
                if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--' and \
                        not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                    moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))
            if self.currentCastleRights.wqs:  # White queen-side
                if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--' and \
                        not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                    moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))
        else:
            if self.currentCastleRights.bks:  # Black king-side
                if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--' and \
                        not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                    moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))
            if self.currentCastleRights.bqs:  # Black queen-side
                if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--' and \
                        not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                    moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    def getKingssideCastleMoves(self,r,c,moves):
        if self.board[r][c+1]=='--'and self.board[r][c+2]=='--':
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove=True))

    def getQueensideCastleMoves(self,r,c,moves):
        if self.board[r][c-1]=='--' and self.board[r][c-2]=='--' and self.board[r][c-3]:
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove=True))
    def checkForPinsAndChecks(self):
        pins=[]
        checks=[]
        inCheck=False
        if self.whiteToMove:
            enemyColor='B'
            allyColor='W'
            startRow=self.whiteKingLocation[0]
            startCol=self.whiteKingLocation[1]
        else:
            enemyColor = 'W'
            allyColor = 'B'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions=((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d=directions[j]
            possiblePin=()
            for i in range(1,8):
                endRow=startRow+d[0]*i
                endCol=startCol+d[1]*i
                if 0<=endRow<8 and 0<=endCol<8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece[0]==allyColor and endPiece[1]!='K':
                        if possiblePin==():
                            possiblePin=(endRow,endCol,d[0],d[1])
                        else:
                            break
                    elif endPiece[0]==enemyColor:
                        type=endPiece[1]
                        if(0<=j<=3 and type=='R')or \
                                (4<=j<=7 and type=='B') or \
                                            (i==1 and type=='P' and ((enemyColor=='W'and 6<=j<=7) or (enemyColor=='B' and 4<=j<=5))) or \
                                (type=='Q') or (i==1 and type=='K'):
                            if possiblePin==():
                                inCheck=True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break;
                        else:
                            break
                else:
                    break
        knightMoves=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for m in knightMoves:
            endRow=startRow+m[0]
            endCol=startCol+m[1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]==enemyColor and endPiece[1]=='N':
                    inCheck=True
                    checks.append((endRow,endCol,m[0],m[1]))
        return inCheck,pins,checks

class CastleRight:
    def __init__(self,wks,bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs
class Move:
    ranksToRow={"1":7,"2":6,"3":5,"4":4,
                "5":3,"6":2,"7":1,"8":0}
    rowToRanks={v:k for k,v in ranksToRow.items()}
    filesToCols={"a":0,"b":1,"c":2,"d":3,
                 "e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in filesToCols.items()}

    def __init__(self,startsq,endsq,board,enpassantPossible=False,isCastleMove=False):
        self.startRow=startsq[0]
        self.startCol=startsq[1]
        self.endRow=endsq[0]
        self.endCol=endsq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.isPawnPromotion= (self.pieceMoved=='WP'and self.endRow==0) or (self.pieceMoved=='BP' and self.endRow==7)
        self.enpassantPossible= enpassantPossible
        if self.enpassantPossible:
            self.pieceCaptured='WP' if self.pieceMoved=='BP'else 'BP'

        self.isCastleMove=isCastleMove
        self.moveID=self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol


    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID==other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)


    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowToRanks[r]




