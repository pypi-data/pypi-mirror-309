from abc import ABC, abstractmethod

import chess
import numpy as np

from .chess_features import (
    get_unified_valued_bitboard,
    to_bit_attack_map,
    to_bit_defend_map,
    to_bitboard,
    to_chess_neighborhoods,
    to_fen,
    to_san,
    to_unified_neg_bitboard,
    to_valued_attack_map,
    to_valued_bitboard,
    to_valued_defend_map,
    to_white_moving,
)


class ExtractorBase(ABC):
    @abstractmethod
    def __call__(self, board: chess.Board, **_: dict) -> np.ndarray | str | chess.Board:
        pass


class BitAttackExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> np.ndarray:
        return to_bit_attack_map(board)


class BitDefendExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> np.ndarray:
        return to_bit_defend_map(board)


class BitboardExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> np.ndarray:
        return to_bitboard(board)


class NeighborhoodExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> np.ndarray:
        return to_chess_neighborhoods(board, **_)


class FenExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> str:
        return to_fen(board)


class SanExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> str:
        return to_san(board)


class UnifiedNegBitboardExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> np.ndarray:
        return to_unified_neg_bitboard(board)


class ValuedAttackExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> np.ndarray:
        return to_valued_attack_map(board, **_)


class ValuedBitboardExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> np.ndarray:
        return to_valued_bitboard(board, **_)


class ValuedDefendExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> np.ndarray:
        return to_valued_defend_map(board, **_)


class WhiteMovingExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> chess.Board:
        return to_white_moving(board)


class UnifiedValuedBitboardExtractor(ExtractorBase):
    def __call__(self, board: chess.Board, **_: dict) -> np.ndarray:
        return get_unified_valued_bitboard(board, **_)
