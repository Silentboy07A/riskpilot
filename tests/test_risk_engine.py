from backend.risk_engine.engine import RiskEngine


engine = RiskEngine()


# Normal transaction
normal = engine.calculate_risk(
    ml_probability=0.05,
    transactions_last_1h=1,
    transactions_last_24h=3,
    amount_vs_customer_avg=1.2,
    customer_transaction_count=20,
)

print("\nNORMAL TRANSACTION")
print(normal)


# Suspicious transaction
suspicious = engine.calculate_risk(
    ml_probability=0.85,
    transactions_last_1h=8,
    transactions_last_24h=25,
    amount_vs_customer_avg=12,
    customer_transaction_count=2,
)

print("\nSUSPICIOUS TRANSACTION")
print(suspicious)