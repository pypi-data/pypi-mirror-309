import chess
import numpy as np

from .extractor_factory import ExtractorFactory


class ChessTransformer:
    def __init__(self, transformation_type: str) -> None:
        self.transformation_type = transformation_type
        self._extractor_factory = ExtractorFactory()
        self.extractor = self._extractor_factory.create(transformation_type)

    def __call__(self, board: chess.Board, values: dict | None = None) -> np.ndarray:
        if isinstance(board, str):
            board = chess.Board(board)
        return self.extractor(board, values=values)

    def get_available_transformations(self) -> list:
        return list(self._extractor_factory.keys())
