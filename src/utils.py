class Player:
    def __init__(self, name, stone):
        self.name = name
        self.stone = stone

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
        return [row[:] for row in board]
    
    @staticmethod
    def calculate_scores(board, P1, P2):
        P1_score, P2_score = 0, 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == P1:
                    P1_score += 1
                elif board[x][y] == P2:
                    P2_score += 1
        return P1_score, P2_score
    
    @staticmethod
    def in_bounds(row, col):
        # needed for manual input
        return 0 <= row < 8 and 0 <= col < 8
    
    @staticmethod
    def count_points(board, row, col, horz, vert):
        stone = board[row][col]
        count = 1
        # scalar value allows iteration in (horz, vert) direction
        for scalar in range(1, 8 + 1):
            if Board.in_bounds(row + scalar * horz, col + scalar * vert):
                if board[row + scalar * horz][col + scalar * vert] == 0:
                    return 0
                elif board[row + scalar * horz][col + scalar * vert] == stone:
                    count += 1
                else:
                    return count
            else:
                return 0
        return count
    
    @staticmethod
    def check_move(board, row, col, stone):
        points = 0
        directions = [-1, 0, 1]
        for horz in directions:
            for vert in directions:
                if vert != 0 or horz != 0:
                    if Board.in_bounds(row + horz, col + vert):
                        examined = board[row + horz][col + vert]
                        if examined != 0 and examined != stone:
                            points += Board.count_points(board, row + horz, col + vert, horz, vert)
                        # move is valid if stones can be flipped
                        if points > 0:
                            return points
        return points
    
    @staticmethod
    def get_valid_moves(state, stone):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                # explore free spaces only
                if state[i][j] == 0:
                    gain = Board.check_move(state, i, j, stone)
                    if gain > 0:
                        valid_moves.append(Move((i, j), gain))
        if not valid_moves:
            return None
        else:
            return valid_moves
    
    def simulate_move(board, move, stone):
        if move == None:
            return board
        
        row, col = move
        
        # needed to not modify original board
        board_copy = Board.copy_board(board)
        board_copy[row][col] = stone
        
        directions = [-1, 0, 1]
        # this combination checks surrounding cells
        for vert in directions:
            for horz in directions:
                stones = []
                if vert == horz == 0:
                    continue
                
                lrow = row
                lcol = col
                lrow += vert
                lcol += horz
                
                while Board.in_bounds(lrow, lcol):
                    # if stone is opponents color append to flip later
                    if board_copy[lrow][lcol] != stone and board_copy[lrow][lcol] != 0:
                        stones.append((lrow, lcol))
                    # space breaks direct line, no stones flipped
                    elif board_copy[lrow][lcol] == 0:
                        break
                    # if same color stone found, flip all stones in between
                    elif board_copy[lrow][lcol] == stone:
                        for a, b in stones:
                            board_copy[a][b] = stone
                        break
                    
                    lrow += vert
                    lcol += horz
        
        return board_copy
    
    @staticmethod
    def is_valid(board, move, stone):
        moves = Board.get_valid_moves(board, stone)
        if moves:
            return move in (_.coords for _ in moves)
        return False
    
    @staticmethod
    def no_move_left(board, stone):
        return not bool(Board.get_valid_moves(board, stone))
    
    @staticmethod
    def alpha_beta_search(stone, board, alpha, beta, depth):
        # recursion base case
        if depth == 0:
            return Move(None, Board.calculate_score(board, stone))
        
        valid_moves = Board.get_valid_moves(board, stone)
        
        if not valid_moves:
            # no more valid moves evaluate oponents next play
            if not Board.get_valid_moves(board, Board.opponent_stone(stone)):
                # no more moves for either player, return final state
                return Move(None, Board.final_value(board, stone))
            # opponent has valid moves, return points for that move
            value = -Board.alpha_beta_search(Board.opponent_stone(stone), board, -beta, -alpha, depth - 1).points 
            return Move(None, value)
        
        best_move = valid_moves[0]
        best_move.points = alpha
        
        for move in valid_moves:
            if beta <= alpha:
                # prune nodes that aren't worth visiting
                break
            sim_move_board = Board.simulate_move(board, move.coords, stone)
            value = -Board.alpha_beta_search(Board.opponent_stone(stone), sim_move_board, -beta, -alpha, depth - 1).points 
            if value > alpha:
                # new max
                alpha = value
                best_move = move
                best_move.points = alpha
            #Board.moves_analized.append(move)
        return best_move
    
    def final_value(board, stone):
        # if player wins return max score so adv search uses this branch
        score = Board.calculate_score(board, stone)
        if score < 0:
            return Board.MIN_SCORE
        elif score > 0:
            return Board.MAX_SCORE
        return score
    
    @staticmethod
    def opponent_stone(stone):
        if stone == 1:
            return 2
        elif stone == 2:
            return 1
        else:
            return 0
    
    @staticmethod
    def calculate_score(board, stone):
        score = 0
        for x in range(8):
            for j in range(8):
                if board[x][j] == stone:
                    score += 1
                elif board[x][j] == Board.opponent_stone(stone):
                    score -= 1
        return score
    
    @staticmethod
    def move(board, player, depth=1):
        Board.valid_moves = Board.get_valid_moves(board, player)
        if not Board.valid_moves:
            return None
        move = Board.alpha_beta_search(player, board, Board.MIN_SCORE, Board.MAX_SCORE, depth)
        return move.coords

if __name__ == "__main__":
    pass
