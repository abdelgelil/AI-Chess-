import pygame as p
import chessengine
import ChessAi

#OmarNabill


# Game screen dimensions and constants
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImage():
    pieces = ['WP', 'WR', 'WN', 'WB', 'WK', 'WQ', 'BP', 'BR', 'BN', 'BB', 'BK', 'BQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("image/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def selectGameMode():
    p.init()
    screen = p.display.set_mode((512, 512))
    p.display.set_caption("ChessNull")
    font = p.font.Font(None, 36)

    # Load the background image
    background_image = p.image.load(r"C:\Users\Dell\Downloads\chesssss.png")
    background_image = p.transform.scale(background_image, (512, 512))  # Scale it to fit the screen

    # Button dimensions
    button_width, button_height = 300, 50
    button_x = (512 - button_width) // 2  # Center horizontally
    button_y_ai = 180  # First button Y-coordinate
    button_y_two_player = button_y_ai + button_height + 20  # Second button Y-coordinate with spacing

    running = True
    mode = None

    while running:
        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Draw buttons
        p.draw.rect(screen, p.Color(240, 217, 181), p.Rect(button_x, button_y_ai, button_width, button_height))
        p.draw.rect(screen, p.Color(181, 136, 99), p.Rect(button_x, button_y_two_player, button_width, button_height))

        # Add text
        text_ai = font.render("Play Against AI", True, p.Color("black"))
        text_two_player = font.render("Two Players", True, p.Color("black"))

        # Center the text on the buttons
        text_ai_rect = text_ai.get_rect(center=(button_x + button_width // 2, button_y_ai + button_height // 2))
        text_two_player_rect = text_two_player.get_rect(center=(button_x + button_width // 2, button_y_two_player + button_height // 2))

        screen.blit(text_ai, text_ai_rect)
        screen.blit(text_two_player, text_two_player_rect)

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_x <= x <= button_x + button_width and button_y_ai <= y <= button_y_ai + button_height:
                    mode = "ai"
                    running = False
                elif button_x <= x <= button_x + button_width and button_y_two_player <= y <= button_y_two_player + button_height:
                    mode = "two_player"
                    running = False

        p.display.flip()

    p.quit()
    return mode


def main():
    while True:
        mode = selectGameMode()
        if mode is None:
            break  # Exit if no mode is selected (i.e., user presses B to go back to the main menu)

        p.init()
        p.display.set_caption("ChessNull")
        screen = p.display.set_mode((WIDTH, HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        gs = chessengine.GameState()
        validMoves = gs.getValidMoves()
        moveMade = False
        animate = False
        loadImage()
        running = True
        sqSelected = ()
        playerClicks = []
        gameOver = False
        ai = ChessAi.ChessAI()

        while running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                    p.quit()  # Explicitly quit Pygame when the window is closed
                    break
                elif event.type == p.MOUSEBUTTONDOWN:
                    if not gameOver and (mode == "two_player" or gs.whiteToMove):
                        location = p.mouse.get_pos()
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE
                        if sqSelected == (row, col):
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        if len(playerClicks) == 2:
                            move = chessengine.Move(playerClicks[0], playerClicks[1], gs.board)
                            if move in validMoves:
                                gs.makeMove(move)
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                            else:
                                playerClicks = [sqSelected]
                elif event.type == p.KEYDOWN:
                    if event.key == p.K_z:
                        gs.undoMove()
                        validMoves = gs.getValidMoves()
                        moveMade = True
                        animate = False
                    if event.key == p.K_r:
                        gs = chessengine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False
                    if event.key == p.K_b:  # 'B' key to return to the main menu
                        running = False  # Exit the current game loop
                    if event.key == p.K_f:  # 'F' key to flip the board
                        flipBoard(gs)
                    if event.key==p.K_p:
                        gs.checkk=False

            if moveMade:
                if animate:
                    animateMove(gs.movelog[-1], screen, gs.board, clock)
                validMoves = gs.getValidMoves()
                moveMade = False
                animate = False

            if mode == "ai" and not gs.whiteToMove and not gameOver:
                aiMove = ai.getBestMove(gs, validMoves)
                gs.makeMove(aiMove)
                moveMade = True
                animate = True

            drawGameState(screen, gs, validMoves, sqSelected)

            if gs.checkMate:
                gameOver = True
                if gs.whiteToMove:
                    drawText(screen, 'Black wins!', "Black")
                else:
                    drawText(screen, 'White wins!', "White")
            elif gs.staleMate:
                gameOver = True
                drawText(screen, 'Stalemate! It\'s a draw.')
            elif gs.checkk:
                drawText(screen, 'CHECK', "RED")

            clock.tick(MAX_FPS)
            p.display.flip()

        # This is where the program will return to the main menu after quitting the game loop.
        continue  # Returns to the main menu to select a new game mode

def hightlightSquares(screen, gs, validMoves,
                      sqSelected):  # by3ml loon green as a highlight lel valid moves elmomken trohha

    if sqSelected != ():  # Check if a square is selected
        r, c = sqSelected  # Get the row and column of the selected square elwa2ef fyha ell3ba dlw
        if gs.board[r][c][0] == (
        'W' if gs.whiteToMove else 'B'):  # Check if the selected piece belongs to the current player
            s = p.Surface((SQ_SIZE, SQ_SIZE))  # Create a transparent surface for highlighting
            s.set_alpha(100)  # Set transparency level
            s.fill(p.Color(
                'gray'))  # Fill the surface with gray color for the selected square(lw hwa wa2ef fy heta bykoun lonha gray at the moment)
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))  # Blit the gray highlight on the selected square
            s.fill(p.Color('green'))  # Change the highlight color to green for valid moves
            for move in validMoves:  # Iterate through all valid moves
                if move.startRow == r and move.startCol == c:  # Check if the move starts from the selected square we have to make sure of this
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))  # Highlight the destination square


def drawGameState(screen, gs, validMoves,
                  sqSelected):  # Draws the current game state, including the board, pieces, and highlighted squares.

    drawBoard(screen)  # Draw the chessboard
    hightlightSquares(screen, gs, validMoves, sqSelected)  # Highlight squares as needed
    #drawKingInCheck(screen,gs)
    drawPieces(screen, gs.board)  # Draw the chess pieces on the board

def drawKingInCheck(screen, gs):
    """
    Highlights the square of the king in red if it is in check.
    """
    if gs.checkk:
        kingLocation = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation
        row, col = kingLocation
        #print(f"Drawing red square at {row}, {col}")  # Debugging line
        s = p.Surface((SQ_SIZE, SQ_SIZE))  # Create a transparent surface
        s.set_alpha(100)  # Set transparency level
        s.fill(p.Color('red'))  # Fill the surface with red color
        screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))  # Blit the red highlight on the king's square


def drawBoard(screen):  # Draws the chessboard with alternating colors for squares, wahda w wahda lel board

    global colors  # Global variable for square colors
    colors = [p.Color(240, 217, 181), p.Color(181, 136, 99)]  # Light and dark square colors
    for i in range(DIMENSION):  # Loop over rows
        for j in range(DIMENSION):  # Loop over columns
            color = colors[(i + j) % 2]  # Alternate colors for squares
            p.draw.rect(screen, color, p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # Draw each square


def drawPieces(screen, board):  # Draws the chess pieces on the board based on the current board state.

    for i in range(DIMENSION):  # Loop over rows
        for j in range(DIMENSION):  # Loop over columns
            piece = board[i][j]  # Get the piece at the current square
            if piece != "--":  # If the square is not empty
                screen.blit(IMAGES[piece], p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # Draw the piece image


def animateMove(move, screen, board,
                clock):  # Animates a move by smoothly transitioning a piece from its starting square to its destination.

    global colors  # Use the global color scheme for the board
    dR = move.endRow - move.startRow  # Calculate row difference
    dC = move.endCol - move.startCol  # Calculate column difference
    framesPerSquare = 10  # Number of frames per square movement
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare  # Total frames for the animation
    for frame in range(frameCount + 1):  # Loop through animation frames
        r, c = (move.startRow + dR * frame / frameCount,
                move.startCol + dC * frame / frameCount)  # Calculate intermediate positions
        drawBoard(screen)  # Redraw the board
        drawPieces(screen, board)  # Redraw all pieces
        color = colors[(move.endRow + move.endCol) % 2]  # Determine the background color of the destination square
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE,
                           SQ_SIZE)  # Destination square rectangle
        p.draw.rect(screen, color, endSquare)  # Draw the destination square
        if move.pieceCaptured != '--':  # If a piece is captured
            screen.blit(IMAGES[move.pieceCaptured], endSquare)  # Display the captured piece

        # Draw the moving piece at its current position
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()  # Update the display
        clock.tick(120)  # Control the animation speed




def drawText(screen, text,colooor):  # Draws text on the screen.

    font = p.font.SysFont("Helvetica", 32, True, False)  # Create a font object
    shadow_text = font.render(text, True, p.Color("Gray"))  # Create a shadow for the text
    shadow_location = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - shadow_text.get_width() / 2, HEIGHT / 2 - shadow_text.get_height() / 2)  # Center the shadow
    screen.blit(shadow_text, shadow_location)  # Draw the shadow text
    text = font.render(text, True, p.Color(colooor))  # Create the main text
    screen.blit(text, shadow_location.move(2, 2))  # Draw the main text with an offset for 3D effect

def flipBoard(gs):
    """Flip the chessboard by reversing the rows."""
    gs.board = gs.board[::-1]  # Reverse the rows of the board
    gs.whiteToMove = not gs.whiteToMove  # Switch turn to the other player


if __name__ == "__main__":
    main()  # Start the game