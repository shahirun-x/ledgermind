from typing import Optional, Dict


# -----------------------------
# Intent constants
# -----------------------------
INTENT_COUNT = "COUNT"
INTENT_AGGREGATION = "AGGREGATION"
INTENT_PERFORMANCE_COMPARISON = "PERFORMANCE_COMPARISON"
INTENT_UNKNOWN = "UNKNOWN"

AGG_SUM = "SUM"
AGG_MEAN = "MEAN"


# -----------------------------
# Parsed intent contract
# -----------------------------
class ParsedIntent:
    def __init__(
        self,
        intent: str,
        dataset: Optional[str] = None,
        metric: Optional[str] = None,
        group_by: Optional[str] = None,
        aggregation: Optional[str] = None,
        filters: Optional[Dict] = None,
    ):
        self.intent = intent
        self.dataset = dataset
        self.metric = metric
        self.group_by = group_by
        self.aggregation = aggregation
        self.filters = filters or {}


# -----------------------------
# Intent parser
# -----------------------------
def parse_intent(question: str) -> ParsedIntent:
    q = question.lower()

    # -------------------------------------------------
    # 0. BLOCK COMPOUND QUESTIONS (CRITICAL)
    # -------------------------------------------------
    # BLOCK compound questions (except financial terms like profit and loss)
    if (
        (" and " in q or " & " in q)
        and "profit and loss" not in q
        and "p&l" not in q
    ):
        return ParsedIntent(
            intent=INTENT_UNKNOWN,
            filters={"raw_question": question},
        )


    # -------------------------------------------------
    # 1. BLOCK EXPLANATION / WHY QUESTIONS
    # -------------------------------------------------
    if "why" in q or "explain" in q or "reason" in q:
        return ParsedIntent(
            intent=INTENT_UNKNOWN,
            filters={"raw_question": question},
        )

    # -------------------------------------------------
    # 2. PERFORMANCE COMPARISON
    # -------------------------------------------------
    if (
        "performed better" in q
        or "performed the best" in q
        or "best performing" in q
        or "top performing" in q
        or "highest profit" in q
        or "highest p&l" in q
        or "profit and loss" in q
    ):
        # refuse vague performance questions
        if "total performance" in q:
            return ParsedIntent(
                intent=INTENT_UNKNOWN,
                filters={"raw_question": question},
            )

        return ParsedIntent(
            intent=INTENT_PERFORMANCE_COMPARISON,
            dataset="holdings",
            metric="PL_YTD",
            group_by="PortfolioName",
            aggregation=AGG_SUM,
            filters={"raw_question": question},
        )

    # -------------------------------------------------
    # 3. COUNT (MUST COME BEFORE AGGREGATION)
    # -------------------------------------------------
    if "how many" in q or "number of" in q or "count" in q:
        if "trade" in q:
            return ParsedIntent(
                intent=INTENT_COUNT,
                dataset="trades",
                filters={"raw_question": question},
            )
        if "holding" in q:
            return ParsedIntent(
                intent=INTENT_COUNT,
                dataset="holdings",
                filters={"raw_question": question},
            )

        return ParsedIntent(
            intent=INTENT_COUNT,
            filters={"raw_question": question},
        )

    # -------------------------------------------------
    # 4. AGGREGATION (SUM)
    # -------------------------------------------------
    if "total" in q or "sum" in q:
        dataset = None
        if "trade" in q:
            dataset = "trades"
        elif "holding" in q:
            dataset = "holdings"

        return ParsedIntent(
            intent=INTENT_AGGREGATION,
            dataset=dataset,
            aggregation=AGG_SUM,
            filters={"raw_question": question},
        )

    # -------------------------------------------------
    # 5. AGGREGATION (MEAN)
    # -------------------------------------------------
    if "average" in q or "mean" in q:
        dataset = None
        if "trade" in q:
            dataset = "trades"
        elif "holding" in q:
            dataset = "holdings"

        return ParsedIntent(
            intent=INTENT_AGGREGATION,
            dataset=dataset,
            aggregation=AGG_MEAN,
            filters={"raw_question": question},
        )

    # -------------------------------------------------
    # 6. UNKNOWN
    # -------------------------------------------------
    return ParsedIntent(
        intent=INTENT_UNKNOWN,
        filters={"raw_question": question},
    )
