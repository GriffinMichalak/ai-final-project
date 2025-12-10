"""
Script to run training model for Reinforcement Learning AI
"""
import argparse
import os
from models.rl_cnn_ai import CNNRLAI

def format_games(num):
    """
    Format number of games into a compact string
    """
    if num >= 1_000_000:
        if num % 1_000_000 == 0:
            return f"{num // 1_000_000}M"
        return f"{num / 1_000_000:.1f}M"
    
    if num >= 1000:
        if num % 1000 == 0:
            return f"{num // 1000}k"
        return f"{num / 1000:.1f}k"
    return str(num)

def read_games_from_filename(filename: str) -> int:
    """
    Parse game count from model name of form cnnrl_<mode>_<games>_<eps>.pt
    Returns int number of games (500k -> 500000).
    """
    base = os.path.basename(filename).replace(".pt", "")
    parts = base.split("_")
    if len(parts) < 4:
        return 0

    games_part = parts[2]

    if games_part.endswith("k"):
        return int(games_part[:-1]) * 1000
    
    if games_part.endswith("M"):
        return int(float(games_part[:-1]) * 1_000_000)

    try:
        return int(games_part)
    except:
        return 0
    
def train_resumable(model_path: str,
                    target_total_games: int,
                    mode: str,
                    epsilon_decay: float,
                    device: str):
    """
    Resume training an existing model to reach target total games.
    """
    # Load previous training progress
    print(f"Loading model from: {model_path}")
    already_trained = read_games_from_filename(model_path)
    print(f"Detected {already_trained:,} previously trained games.")

    rl = CNNRLAI(player_id=1, epsilon_decay=epsilon_decay, device=device)
    rl.load_model(model_path)
    eps_from_schedule = (rl.epsilon_decay ** already_trained)
    rl.epsilon = max(rl.epsilon_min, eps_from_schedule)

    remaining = max(0, target_total_games - already_trained)
    print(f"Training remaining {remaining:,} games to reach {target_total_games:,}...")

    if remaining == 0:
        print("Model already trained to desired count.")
        return

    # Train the extra games
    rl.train(num_games=remaining, mode=mode)

    # Save a new model with updated filename
    new_games_total = already_trained + remaining
    save_path = f"CNN_models/cnnrl_{mode}_{format_games(new_games_total)}_{epsilon_decay}.pt"

    rl.save_model(save_path)
    print(f"Saved resumed model as: {save_path}")

def main():
    parser = argparse.ArgumentParser(description="Train CNN RL Agent for Connect4")
    parser.add_argument("--mode", type=str, default="random",
                        choices=["random", "self", "heuristic"],
                        help="Training opponent type")
    parser.add_argument("--games", type=int, default=None,
                        help="Number of games to train (default = model default)")
    parser.add_argument("--eps", type=float, default=None,
                        help="Epsilon decay factor (default = model default)")
    parser.add_argument("--device", type=str, default=None,
                        help="Device to use: cpu / cuda / cuda:0 (default = auto)")
    parser.add_argument("--resume", type=str, default=None,
                        help="Path to an existing .pt file to resume training.")
    parser.add_argument("--target-games", type=int, default=None,
                        help="Train model until it reaches this many total games.")
    args = parser.parse_args()

    # Resumable Training
    if args.resume is not None:
        if args.target_games is None:
            raise ValueError("--resume requires --target-games")
        
        train_resumable(
            model_path=args.resume,
            target_total_games=args.target_games,
            mode=args.mode,
            epsilon_decay=args.eps if args.eps is not None else 0.999995,
            device=args.device
        )
        return

    # Normal Training
    rl = CNNRLAI(player_id=1, device=args.device)
    num_games = args.games if args.games is not None else 10000
    if args.eps is not None:
        rl.epsilon_decay = args.eps
    
    # For printing & saving
    mode = args.mode
    eps_decay_str = f"{rl.epsilon_decay}"

    rl.train(num_games=num_games, mode=mode)

    games_label = format_games(num_games)
    model_path = f"CNN_models/cnnrl_{mode}_{games_label}_{eps_decay_str}.pt"
    rl.save_model(model_path)

    print(f"\nModel saved to: {model_path}\n")

if __name__ == "__main__":
    main()