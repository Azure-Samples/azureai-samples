# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


class BlocklistEvaluator:
    def __init__(self, blocklist) -> None:  # noqa: ANN101, ANN001
        self._blocklist = blocklist

    def __call__(self: "BlocklistEvaluator", *, response: str):  # noqa: ANN204
        score = any(word in response for word in self._blocklist)
        return {"score": score}
