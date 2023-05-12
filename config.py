import os
import glob

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
engine_dir = os.path.join(parent_dir, 'ChessProgram', 'Engine')  # Add the missing folder 'ChessProgram'

stockfish_files = glob.glob(os.path.join(engine_dir, '*stockfish*.exe'))
nnue_files = glob.glob(os.path.join(engine_dir, '*.nnue'))

engine_path = stockfish_files[0] if stockfish_files else None
nnue_path = nnue_files[0] if nnue_files else None

print(f"Engine directory: {engine_dir}")
print(f"Stockfish files: {stockfish_files}")
print(f"NNUE files: {nnue_files}")
print(f"Engine path: {engine_path}")
print(f"NNUE path: {nnue_path}")

CONFIG = {
    'engine_path': engine_path,
    'nnue_path': nnue_path,
    'settings_file': 'settings.json'
}


