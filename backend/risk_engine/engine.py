from dataclasses import dataclass


@dataclass
class RiskResult:
    ml_score: float
    velocity_score: float
    amount_score: float
    behaviour_score: float
    final_score: float
    decision: str
    reasons: list[str]


class RiskEngine:
    def calculate_risk(
        self,
        ml_probability: float,
        transactions_last_1h: int,
        transactions_last_24h: int,
        amount_vs_customer_avg: float,
        customer_transaction_count: int,
    ) -> RiskResult:

        reasons = []

        # --------------------------------------------------
        # ML score
        # --------------------------------------------------

        ml_score = ml_probability * 100

        # --------------------------------------------------
        # Velocity risk
        # --------------------------------------------------

        velocity_score = 0.0

        if transactions_last_1h >= 10:
            velocity_score = 100
            reasons.append(
                "Very high transaction velocity in the last hour"
            )

        elif transactions_last_1h >= 5:
            velocity_score = 70
            reasons.append(
                "High transaction velocity in the last hour"
            )

        elif transactions_last_1h >= 3:
            velocity_score = 40
            reasons.append(
                "Elevated transaction velocity"
            )

        elif transactions_last_1h >= 1:
            velocity_score = 15

        # Additional 24-hour signal
        if transactions_last_24h >= 20:
            velocity_score = max(
                velocity_score,
                70,
            )
            reasons.append(
                "High transaction activity in the last 24 hours"
            )

        # --------------------------------------------------
        # Amount risk
        # --------------------------------------------------

        amount_score = 0.0

        if amount_vs_customer_avg >= 20:
            amount_score = 100
            reasons.append(
                "Transaction amount is extremely high "
                "compared with customer history"
            )

        elif amount_vs_customer_avg >= 10:
            amount_score = 80
            reasons.append(
                "Transaction amount is significantly above "
                "customer history"
            )

        elif amount_vs_customer_avg >= 5:
            amount_score = 60
            reasons.append(
                "Transaction amount is unusually high"
            )

        elif amount_vs_customer_avg >= 3:
            amount_score = 40
            reasons.append(
                "Transaction amount is above normal"
            )

        # --------------------------------------------------
        # Behaviour risk
        # --------------------------------------------------

        behaviour_score = 0.0

        if customer_transaction_count == 0:
            behaviour_score += 20
            reasons.append(
                "First observed transaction for this customer"
            )

        elif customer_transaction_count < 3:
            behaviour_score += 10

        # --------------------------------------------------
        # Combine risk signals
        # --------------------------------------------------

        final_score = (
            0.60 * ml_score
            + 0.20 * velocity_score
            + 0.15 * amount_score
            + 0.05 * behaviour_score
        )

        final_score = min(
            max(final_score, 0),
            100,
        )

        # --------------------------------------------------
        # Decision
        # --------------------------------------------------

        if final_score >= 75:
            decision = "BLOCK"

        elif final_score >= 40:
            decision = "REVIEW"

        else:
            decision = "ALLOW"

        return RiskResult(
            ml_score=round(ml_score, 2),
            velocity_score=round(
                velocity_score,
                2,
            ),
            amount_score=round(
                amount_score,
                2,
            ),
            behaviour_score=round(
                behaviour_score,
                2,
            ),
            final_score=round(
                final_score,
                2,
            ),
            decision=decision,
            reasons=reasons,
        )