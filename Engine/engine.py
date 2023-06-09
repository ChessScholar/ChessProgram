import chess.engine
import chess.pgn

class ChessEngine:
    def __init__(self, engine_path, nnue_path=None, output_callback=None):
        self.engine_path = engine_path
        self.nnue_path = nnue_path
        self.output_callback = output_callback
        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)

        if self.nnue_path:
            self.engine.configure({"Use NNUE": True, "EvalFile": self.nnue_path})
        else:
            self.engine.configure({"Use NNUE": False})

    def set_engine_options(self, options):
        self.engine.configure(options)

    def analyze(self, board, depth=None, lines=None, cores=None, memory=None):
        limit = chess.engine.Limit(depth=depth)
        options = {
            "Threads": cores,
            "Hash": memory
        }
        self.engine.configure(options)
        info = self.engine.analyse(board, limit, multipv=lines, info=chess.engine.INFO_ALL)
        return info

    def close(self):
        self.engine.quit()