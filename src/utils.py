class Move:
    def __init__(self, coords, points):
        self.coords = coords
        self.points = points
    
    def __repr__(self):
        return f'Move(coords={self.coords}, points={self.points})'

class Board:
    MAX_SCORE = 64
    MIN_SCORE = -64
    
    @staticmethod
    def copy_board(board):
        """Returns a shallow copy of the board"""
        return [row[:] for row in board]
    
    @staticmethod
    def player_scores(board, P1, P2):
        "Returns the scores of the two players"
        P1_score, P2_score = 0, 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == P1:
                    P1_score += 1
                elif board[row][col] == P2:
                    P2_score += 1
        return P1_score, P2_score
    
    @staticmethod
    def heuristic_value(board, player):
        """Returns the heuristic value of a player"""
        score = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == player:
                    score += 1
                elif board[row][col] == Board.opponent(player):
                    score -= 1
        return score
    
    @staticmethod
    def final_value(board, player):
        """Returns final value of a player when the game ends"""
        score = Board.heuristic_value(board, player)
        if score < 0:
            return Board.MIN_SCORE
        elif score > 0:
            return Board.MAX_SCORE
        return score
    
    @staticmethod
    def in_bound(row, col):
        """Checks if a coordinate is within the board or not"""
        return 0 <= row < 8 and 0 <= col < 8
    
    @staticmethod
    def count_points(board, row, col, horz, vert):
        """Returns the points"""
        player = board[row][col]
        points = 1
        for scalar in range(1, 8 + 1):
            if Board.in_bound(row + scalar * horz, col + scalar * vert):
                if board[row + scalar * horz][col + scalar * vert] == 0:
                    return 0
                elif board[row + scalar * horz][col + scalar * vert] == player:
                    points += 1
                else:
                    return points
            else:
                return 0
        return points
    
    @staticmethod
    def check_move(board, row, col, player):
        """Returns the points of a player move"""
        points = 0
        directions = [-1, 0, 1]
        for horz in directions:
            for vert in directions:
                if vert != 0 or horz != 0:
                    if Board.in_bound(row + horz, col + vert):
                        examined = board[row + horz][col + vert]
                        if examined != 0 and examined != player:
                            points += Board.count_points(board, row + horz, col + vert, horz, vert)
                        if points > 0:
                            return points
        return points
    
    @staticmethod
    def get_valid_moves(board, player):
        """Returns all valid moves of a player"""
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if board[row][col] == 0:
                    points = Board.check_move(board, row, col, player)
                    if points > 0:
                        valid_moves.append(Move((row, col), points))
        if not valid_moves:
            return None
        else:
            return valid_moves
    
    @staticmethod
    def transform_board(board, move, player):
        """Returns a new instance of the board when a move is applied"""
        if move == None:
            return board
        
        row, col = move
        new_board = Board.copy_board(board)
        new_board[row][col] = player
        
        directions = [-1, 0, 1]
        # this combination checks surrounding cells
        for vert in directions:
            for horz in directions:
                discs = []
                if vert == horz == 0:
                    continue
                
                lrow = row
                lcol = col
                lrow += vert
                lcol += horz
                
                while Board.in_bound(lrow, lcol):
                    # if opponent's disc, append to flip later
                    if new_board[lrow][lcol] != player and new_board[lrow][lcol] != 0:
                        discs.append((lrow, lcol))
                    # space breaks direct line, no disc flipped
                    elif new_board[lrow][lcol] == 0:
                        break
                    # if same player disc found, flip all discs in between
                    elif new_board[lrow][lcol] == player:
                        for a, b in discs:
                            new_board[a][b] = player
                        break
                    
                    lrow += vert
                    lcol += horz
        
        return new_board
    
    @staticmethod
    def is_valid(board, x, y, player):
        """Checks if a move is valid or not"""
        gain = Board.check_move(board, x, y, player)
        return gain > 0
    
    @staticmethod
    def has_no_move(board, player):
        """Checks if a player has no move or not"""
        return Board.get_valid_moves(board, player) == None
    
    @staticmethod
    def opponent(player):
        """Returns the opponent of a player"""
        if player == 1:
            return 2
        elif player == 2:
            return 1
        else:
            return 0
    
    @staticmethod
    def best_move(board, player, depth=1):
        """Returns the best move using search algorithm"""
        if Board.has_no_move(board, player):
            return None
        
        # best_move = Board.minimax_search(board, player, depth)
        # best_move = Board.negamax_search(board, player, depth)
        best_move = Board.alphabeta_search(board, player, Board.MIN_SCORE, Board.MAX_SCORE, depth)
        
        return best_move
    
    @staticmethod
    def minimax_search(board, player, depth):
        """Returns the best move using minimax search"""
        if depth == 0:
            return Move(None, Board.heuristic_value(board, player))
        
        valid_moves = Board.get_valid_moves(board, player)
        
        if player == 1:
            if not valid_moves:
                # if player 1 has no more valid moves, evaluate the player 2's next play
                if not Board.get_valid_moves(board, 2):
                    # if no more moves for both players, return the final move
                    return Move(None, Board.final_value(board, player))
                # if player 2 has valid moves, return points for that move
                value = Board.minimax_search(board, 2, depth - 1).points 
                return Move(None, value)
            
            best_move = None
            
            for move in valid_moves:
                move_board = Board.transform_board(board, move.coords, player)
                value = Board.minimax_search(move_board, 2, depth - 1).points 
                if (best_move is None) or (value > best_move.points):
                    best_move = move
            
            return best_move
        
        elif player == 2:
            if not valid_moves:
                # if player 2 has no more valid moves, evaluate the player 1's next play
                if not Board.get_valid_moves(board, 1):
                    # if no more moves for both players, return the final move
                    return Move(None, Board.final_value(board, player))
                # if player 1 has valid moves, return points for that move
                value = Board.minimax_search(board, 1, depth - 1).points 
                return Move(None, value)
            
            best_move = None
            
            for move in valid_moves:
                move_board = Board.transform_board(board, move.coords, player)
                value = Board.minimax_search(move_board, 1, depth - 1).points 
                if (best_move is None) or (value > best_move.points):
                    best_move = move
            
            return best_move
    
    @staticmethod
    def negamax_search(board, player, depth):
        """Returns the best move using negamax search"""
        if depth == 0:
            return Move(None, Board.heuristic_value(board, player))
        
        valid_moves = Board.get_valid_moves(board, player)
        
        if not valid_moves:
            # if player has no more valid moves, evaluate the opponent's next play
            if not Board.get_valid_moves(board, Board.opponent(player)):
                # if no more moves for both players, return the final move
                return Move(None, Board.final_value(board, player))
            # if opponent has valid moves, return points for that move
            value = -Board.minimax_search(board, Board.opponent(player), depth - 1).points 
            return Move(None, value)
        
        best_move = None
        
        for move in valid_moves:
            move_board = Board.transform_board(board, move.coords, player)
            value = -Board.minimax_search(move_board, Board.opponent(player), depth - 1).points 
            if (best_move is None) or (value > best_move.points):
                best_move = move
        
        return best_move
    
    @staticmethod
    def alphabeta_search(board, player, alpha, beta, depth):
        """Returns the best move using alpha-beta search"""
        if depth == 0:
            return Move(None, Board.heuristic_value(board, player))
        
        valid_moves = Board.get_valid_moves(board, player)
        
        if not valid_moves:
            # if player has no more valid moves, evaluate the opponent's next play
            if not Board.get_valid_moves(board, Board.opponent(player)):
                # if no more moves for both players, return the final move
                return Move(None, Board.final_value(board, player))
            # if opponent has valid moves, return points for that move
            value = -Board.alphabeta_search(board, Board.opponent(player), -beta, -alpha, depth - 1).points 
            return Move(None, value)
        
        best_move = valid_moves[0]
        best_move.points = alpha
        
        for move in valid_moves:
            if beta <= alpha:
                # prune nodes that are not worth visiting
                break
            move_board = Board.transform_board(board, move.coords, player)
            value = -Board.alphabeta_search(move_board, Board.opponent(player), -beta, -alpha, depth - 1).points 
            if value > alpha:
                # new max
                alpha = value
                best_move = move
                best_move.points = alpha
        
        return best_move

if __name__ == "__main__":
    pass
