"""One-shot key remap for verdicts.py: reviewer-shortened IDs -> true bundle IDs."""

from pathlib import Path

P = "financial-analysis--"
PAIRS = [
("if-converted-debt-to-common-diluted-eps", "if-converted-debt-earnings-per-share"),
("if-converted-preferred-to-common-diluted-eps", "if-converted-preferred-earnings-per-share"),
("treasury-stock-method-incremental-shares", "treasury-stock-method-earnings-per-share"),
("pretax-margin-from-continuing-operations", "pretax-profit-margin"),
("current-ratio", "current-liquidity-ratio"),
("quick-ratio", "quick-liquidity-ratio"),
("cash-ratio", "cash-liquidity-ratio"),
("free-cash-flow-to-firm-from-net-income", "free-cash-flow-firm-from-net-income"),
("free-cash-flow-to-firm-from-cfo", "free-cash-flow-firm-from-operating-cash-flow"),
("free-cash-flow-to-equity-from-cfo", "free-cash-flow-equity-from-operating-cash-flow"),
("direct-method-cash-collected-from-customers", "cash-collected-from-customers"),
("direct-method-cash-paid-for-salaries", "cash-paid-for-accrued-expense"),
("direct-method-cash-paid-to-suppliers", "cash-paid-to-inventory-suppliers"),
("cash-return-on-assets", "cash-return-on-average-assets"),
("cash-return-on-equity", "cash-return-on-average-equity"),
("cash-to-operating-income-ratio", "cash-flow-to-operating-income"),
("operating-cash-flow-per-share", "operating-cash-flow-per-common-share"),
("long-term-debt-payment-coverage", "cash-flow-long-term-debt-payment-coverage"),
("investing-financing-cash-coverage", "cash-flow-investing-financing-coverage"),
("cash-flow-reinvestment-ratio", "operating-cash-flow-reinvestment-coverage"),
("cash-flow-dividend-coverage-ratio", "operating-cash-flow-dividend-coverage"),
("debt-to-assets-ratio", "interest-bearing-debt-to-assets"),
("equity-multiplier-leverage", "balance-sheet-financial-leverage"),
("debt-to-capital-ratio", "interest-bearing-debt-to-capital"),
("debt-to-ebitda-ratio", "interest-bearing-debt-to-ebitda"),
("indirect-method-operating-cash-flow", "indirect-operating-cash-flow-reconciliation"),
("retained-earnings-rollforward", "retained-earnings-roll-forward"),
("payables-turnover-ratio", "trade-payables-turnover-ratio"),
("days-sales-outstanding", "days-of-sales-outstanding"),
("days-inventory-on-hand", "days-of-inventory-on-hand"),
("days-payables-outstanding", "days-of-trade-payables"),
("cash-conversion-cycle-days", "cash-conversion-cycle"),
("defensive-interval-ratio", "defensive-interval-from-period-expenditures"),
("operating-return-on-assets", "operating-return-on-average-assets"),
("return-on-total-assets", "net-income-return-on-average-assets"),
("return-on-common-equity", "return-on-average-equity"),
("return-on-capital-employed", "return-on-average-common-equity"),
("tax-burden-factor", "dupont-tax-burden"),
("interest-burden-factor", "dupont-interest-burden"),
("ebit-margin-factor", "dupont-ebit-margin"),
("dupont-three-factor-roe", "dupont-three-factor-return-on-equity"),
("dupont-five-factor-roe", "dupont-five-factor-return-on-equity"),
("lifo-to-fifo-cogs-adjustment", "fifo-cost-of-sales-from-lifo-reserve"),
("lifo-to-fifo-inventory-adjustment", "fifo-net-income-from-lifo-reserve-change"),
("lifo-to-fifo-net-income-adjustment", "fifo-net-income-from-lifo-reserve-change"),
("dividend-payout-ratio", "common-dividend-payout-ratio"),
("earnings-retention-rate", "earnings-retention-fraction"),
("sustainable-growth-rate", "retention-based-sustainable-growth"),
("inventory-net-realizable-value", "inventory-net-realisable-value"),
("lifo-liquidation-profit-after-tax", "lifo-liquidation-gross-profit-effect"),
("ebitda-per-share", "ebitda-per-common-share"),
("dividends-per-share", "dividends-declared-per-common-share"),
("operating-cash-flow-per-weighted-share", "valuation-operating-cash-flow-per-share"),
("sales-per-share", "sales-per-weighted-average-share"),
("units-of-production-depreciation-expense", "units-of-production-depreciation"),
("carrying-amount-net-of-accumulated-depreciation", "asset-carrying-amount-cost-model"),
("average-age-of-depreciable-assets", "estimated-depreciable-asset-age"),
("average-remaining-life-of-depreciable-assets", "estimated-depreciable-asset-remaining-life"),
("asset-sale-gain-or-loss-on-disposal", "long-lived-asset-sale-gain-loss"),
("fair-value-less-costs-of-disposal", "fair-value-less-disposal-costs"),
("asset-taxable-temporary-difference-dtl", "asset-taxable-temporary-difference-deferred-liability"),
("asset-deductible-temporary-difference-dta", "asset-deductible-temporary-difference-deferred-asset"),
("effective-income-tax-rate", "reported-effective-income-tax-rate"),
("liability-deductible-temporary-difference-dta", "liability-deductible-temporary-difference-deferred-asset"),
("liability-taxable-temporary-difference-dtl", "liability-taxable-temporary-difference-deferred-liability"),
("income-tax-expense-current-plus-deferred", "income-tax-expense-current-and-deferred"),
("deferred-tax-rate-change-effect", "deferred-tax-liability-rate-change-effect"),
("bond-carrying-value-rollforward", "bond-amortised-cost-carrying-rollforward"),
("debt-extinguishment-gain-or-loss", "debt-extinguishment-gain"),
("degree-of-financial-leverage", "degree-of-financial-leverage-ebit-ebt"),
("enterprise-value-full-ownership", "enterprise-value-equity-debt-cash"),
("tangible-book-value-of-equity", "tangible-book-value-equity"),
("inventory-cost-of-goods-flow", "inventory-cost-flow-cost-of-sales"),
("property-casualty-combined-ratio", "insurance-combined-ratio-earned-premiums"),
("after-tax-return-on-invested-capital", "after-tax-return-on-average-invested-capital"),
("forgone-cash-discount-effective-annual-rate", "forgone-discount-trade-credit-effective-annual-cost"),
("treasury-stock-outstanding-shares", "outstanding-shares-from-issued-and-treasury"),
("goodwill-at-acquisition-full-ownership", "acquisition-goodwill-full-ownership"),
("cash-and-equivalents-rollforward", "cash-and-equivalents-statement-rollforward"),
("direct-method-operating-cash-flow-total", "direct-operating-cash-flow-from-gross-receipts-payments"),
("total-comprehensive-income-composition", "total-comprehensive-income-from-profit-and-oci"),
("lifo-to-fifo-retained-earnings-adjustment", "fifo-retained-earnings-from-lifo-reserve"),
("inventory-writedown-adjusted-cogs", "fifo-adjusted-cost-of-sales-without-inventory-writedown"),
("net-income-excluding-inventory-writedown", "net-income-excluding-inventory-writedown-charge"),
("specific-borrowing-eligible-capitalized-costs", "specific-borrowing-cost-capitalization-ifrs"),
("shareholders-equity-rollforward", "shareholders-equity-rollforward-comprehensive-income"),
("lessee-finance-lease-rou-amortization", "operating-lease-rou-amortization-from-lease-cost"),
("asset-tax-base-cost-less-tax-depreciation", "depreciable-asset-tax-base-from-cost-and-deductions"),
("liability-tax-base-carrying-less-future-deduction", "liability-tax-base-from-future-deduction"),
("deferred-tax-balance-from-temporary-difference", "deferred-revenue-liability-tax-base"),
("enterprise-value-to-ebitda-multiple", "enterprise-value-to-ebitda"),
("ebitda-from-ebt-build", "ebitda-from-ebit-and-depreciation-amortization"),
("horizontal-trend-index-number", "horizontal-common-size-trend-index"),
("straight-line-bond-premium-discount-amortization", "straight-line-bond-discount-premium-amortization"),
("effective-interest-bond-interest-expense", "bond-interest-expense-from-coupon-and-amortization"),
("current-income-tax-payable", "current-income-tax-from-taxable-profit"),
]


def run():
    """Apply all key renames to verdicts.py."""
    path = Path("ingest-notes/slice-e-work/verdicts.py")
    text = path.read_text(encoding="utf-8")
    for old, new in PAIRS:
        key_old = f'"{P}{old}":'
        key_new = f'"{P}{new}":'
        assert key_old in text, old
        assert text.count(key_old) >= 1
        text = text.replace(key_old, key_new)
    path.write_text(text, encoding="utf-8")
    print(f"remapped {len(PAIRS)} keys")


if __name__ == "__main__":
    run()
