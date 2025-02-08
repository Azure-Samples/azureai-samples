# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


class BlocklistEvaluator:
    def __init__(self, blocklist) -> None:  # noqa: ANN001
        self._blocklist = blocklist

    def __call__(self: "BlocklistEvaluator", *, response: str):  # noqa: ANN204
        score = any(word in self._blocklist for word in response.split())
        return {"score": score}
