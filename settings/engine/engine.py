import chess
import chess.engine

class UCIEngine:
    def __init__(self, engine_path):
        self.engine_path = engine_path
        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        self.engine.configure({"UCI_ShowWDL": True, "UCI_AnalyseMode": True})
        self.analysis = None

    def play(self, board, limit, info=chess.engine.INFO_NONE):
        return self.engine.play(board, limit, info=info)

    def analyze(self, board, limit):
        last_info = {}
        self.analysis = self.engine.analysis(board, limit)

        # Call this method every time we get a new analyzed move
        def handle_analyze(data):
            move = data["pv"]  # Assuming the 'Move' key is in the form of 'pv'
            score = data["score"]

            # Format the output according to your needs
            move_str = "".join([f"{x}{y}" for x, y in zip(["1", "2", "3", "4", "5", "6"], list(move))])
            score_num = abs(score.relative.score() / 100)
            score_str = f"+{score_num} ply"

            return move_str, score_str

        with self.analysis as analysis:
            while True:
                try:
                    next_info = next(iter(analysis))
                except StopIteration:
                    break

                if "pv" in next_info:
                    move_str, score_str = handle_analyze(next_info)
                    print("Best move:", move_str)

        self.analysis = None
        return last_info

    def set_num_cores(self, num_cores):
        self.engine.configure({"Threads": num_cores})

    def stop_analysis(self):
        if self.analysis is not None:
            self.analysis.stop()
            self.analysis = None

    def close(self):
        self.engine.quit()