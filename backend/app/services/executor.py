from app.services.data_loader import load_trades, load_holdings
from app.services.intent_parser import (
    ParsedIntent,
    INTENT_COUNT,
    INTENT_AGGREGATION,
    INTENT_PERFORMANCE_COMPARISON,
    AGG_SUM,
    AGG_MEAN,
)

REFUSAL_MESSAGE = "Sorry can not find the answer"


def execute_intent(intent: ParsedIntent) -> str:
    try:
        # -------------------------
        # COUNT
        # -------------------------
        if intent.intent == INTENT_COUNT:
            if intent.dataset == "trades":
                df = load_trades()
                return f"Total number of trades: {len(df)}"

            if intent.dataset == "holdings":
                df = load_holdings()
                return f"Total number of holdings: {len(df)}"

            return REFUSAL_MESSAGE

        # -------------------------
        # AGGREGATION
        # -------------------------
        if intent.intent == INTENT_AGGREGATION:
            question = intent.filters.get("raw_question", "").lower()

            if intent.dataset == "trades":
                df = load_trades()

                if "price" in question:
                    column = "Price"
                elif "quantity" in question:
                    column = "Quantity"
                elif "value" in question or "cash" in question:
                    column = "TotalCash"
                else:
                    return REFUSAL_MESSAGE

            elif intent.dataset == "holdings":
                df = load_holdings()

                if "price" in question:
                    column = "Price"
                elif "quantity" in question:
                    column = "Qty"
                elif "value" in question:
                    column = "MV_Base"
                else:
                    return REFUSAL_MESSAGE

            else:
                return REFUSAL_MESSAGE

            if column not in df.columns:
                return REFUSAL_MESSAGE

            if intent.aggregation == AGG_SUM:
                value = df[column].sum()
                return f"Total {column}: {value}"

            if intent.aggregation == AGG_MEAN:
                value = df[column].mean()
                return f"Average {column}: {value}"

            return REFUSAL_MESSAGE

        # -------------------------
        # PERFORMANCE COMPARISON
        # -------------------------
        if intent.intent == INTENT_PERFORMANCE_COMPARISON:
            df = load_holdings()

            grouped = (
                df.groupby("PortfolioName")["PL_YTD"]
                .sum()
                .sort_values(ascending=False)
            )

            if grouped.empty:
                return REFUSAL_MESSAGE

            top_fund = grouped.index[0]
            top_value = grouped.iloc[0]

            return (
                f"The best performing fund based on yearly P&L is "
                f"{top_fund} with a PL_YTD of {top_value}."
            )

        return REFUSAL_MESSAGE

    except Exception:
        return REFUSAL_MESSAGE
