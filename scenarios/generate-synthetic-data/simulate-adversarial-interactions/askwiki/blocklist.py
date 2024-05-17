# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import List, Dict


class BlocklistEvaluator:
    def __init__(self: "BlocklistEvaluator", blocklist: List[str]) -> None:
        self._blocklist = blocklist

    def __call__(self: "BlocklistEvaluator", *, answer: str) -> Dict[str, bool]:
        score = any(word in answer for word in self._blocklist)
        return {"score": score}
