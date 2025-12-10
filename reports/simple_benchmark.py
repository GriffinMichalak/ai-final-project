"""
Simple Connect4 AI Benchmark - Generates CSV report
"""
import time, random, sys, os, csv
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.minimax_ai import MinimaxAI
from models.minimax_ab_ai import MinimaxABAI
from models.simple_ais import RandomAI
from connect4 import Connect4Game

class CountingMinimax(MinimaxAI):
    def __init__(self, player_id, depth=4):
        super().__init__(player_id, depth)
        self.nodes = 0
    def minimax(self, board, depth, is_maximizing):
        self.nodes += 1
        return super().minimax(board, depth, is_maximizing)

class CountingAlphaBeta(MinimaxABAI):
    def __init__(self, player_id, depth=4):
        super().__init__(player_id, depth)
        self.nodes = 0
    def minimax_ab(self, board, depth, is_maximizing, alpha, beta):
        self.nodes += 1
        return super().minimax_ab(board, depth, is_maximizing, alpha, beta)

def generate_boards(n=30):
    boards = []
    for _ in range(n):
        game = Connect4Game(RandomAI(1), RandomAI(2), headless=True)
        for _ in range(random.randint(8, 15)):
            if not game.game_over and game.is_valid_move(random.randint(0, 6)):
                game.make_move(random.randint(0, 6))
        if not game.game_over:
            boards.append(np.array(game.board))
    return boards

def benchmark():
    boards = generate_boards()
    results = []
    
    for depth in [3, 4, 5]:
        minimax_time, alphabeta_time = 0, 0
        minimax_nodes, alphabeta_nodes = 0, 0
        
        for board in boards:
            # Minimax
            ai1 = CountingMinimax(1, depth)
            start = time.time()
            ai1.get_move(board)
            minimax_time += time.time() - start
            minimax_nodes += ai1.nodes
            
            # Alpha-Beta
            ai2 = CountingAlphaBeta(1, depth) 
            start = time.time()
            ai2.get_move(board)
            alphabeta_time += time.time() - start
            alphabeta_nodes += ai2.nodes
        
        # Averages
        avg_minimax_time = minimax_time / len(boards)
        avg_alphabeta_time = alphabeta_time / len(boards)
        avg_minimax_nodes = minimax_nodes / len(boards)
        avg_alphabeta_nodes = alphabeta_nodes / len(boards)
        
        results.append({
            'Depth': depth,
            'Minimax_Time_Sec': round(avg_minimax_time, 4),
            'AlphaBeta_Time_Sec': round(avg_alphabeta_time, 4),
            'Speedup': round(avg_minimax_time / avg_alphabeta_time, 1),
            'Minimax_Nodes': int(avg_minimax_nodes),
            'AlphaBeta_Nodes': int(avg_alphabeta_nodes),
            'Nodes_Saved_Percent': round((avg_minimax_nodes - avg_alphabeta_nodes) / avg_minimax_nodes * 100, 1)
        })
    
    # Save CSV
    with open('ai_benchmark_results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    # Print summary
    print("🚀 AI Benchmark Complete!")
    print(f"📊 Tested on {len(boards)} boards")
    print("📁 Results saved to: ai_benchmark_results.csv")
    print("\n📈 Quick Summary:")
    for r in results:
        print(f"  Depth {r['Depth']}: {r['Speedup']}x faster, {r['Nodes_Saved_Percent']}% fewer nodes")

if __name__ == "__main__":
    benchmark()