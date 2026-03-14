from flask import render_template
from . import main
from .. import db
from ..models import Harvest
from ..models import FinanceTransaction, FinanceCategory
from ..models import InventoryItem, InventoryCategory
from ..models import (
    Production,
    WeightRecord,
    HealthRecord,
    BreedingEvent,
    FeedRecord
)

################################################
# REPORTS DASHBOARD
################################################

@main.route("/reports")
def reports():

    # Crop production
    total_harvest = sum(h.quantity for h in Harvest.query.all())

    # Livestock production
    total_livestock_production = sum(p.quantity for p in Production.query.all())

    # Inventory
    inventory_count = InventoryItem.query.count()

    # Finance
    transactions = FinanceTransaction.query.all()

    income = sum(float(t.amount) for t in transactions if t.type == "income")
    expenses = sum(float(t.amount) for t in transactions if t.type == "expense")

    profit = income - expenses

    return render_template(
        "reports/reports.html",
        total_harvest=total_harvest,
        total_livestock_production=total_livestock_production,
        inventory_count=inventory_count,
        income=income,
        expenses=expenses,
        profit=profit
    )

################################################
# CROP REPORTS
################################################

@main.route("/reports/crops")
def crop_reports():

    harvests = Harvest.query.all()

    field_yields = {}

    for harvest in harvests:

        field_name = harvest.planting.field.name

        if field_name not in field_yields:
            field_yields[field_name] = 0

        field_yields[field_name] += harvest.quantity


    return render_template(
        "reports/crop_reports.html",
        harvests=harvests,
        field_yields=field_yields
    )


################################################
# LIVESTOCK REPORTS
################################################

@main.route("/reports/livestock")
def livestock_reports():

    productions = Production.query.all()
    weights = WeightRecord.query.all()
    health_records = HealthRecord.query.all()
    breeding_events = BreedingEvent.query.all()
    feed_records = FeedRecord.query.all()

    # Production total
    total_production = sum(p.quantity for p in productions)

    # Average weight
    avg_weight = 0
    if weights:
        avg_weight = sum(w.weight for w in weights) / len(weights)

    # Feed usage
    total_feed = sum(float(f.quantity) for f in feed_records)

    return render_template(
        "reports/livestock_reports.html",
        productions=productions,
        weights=weights,
        health_records=health_records,
        breeding_events=breeding_events,
        feed_records=feed_records,
        total_production=total_production,
        avg_weight=round(avg_weight, 2),
        total_feed=total_feed
    )


################################################
# INVENTORY REPORTS
################################################

@main.route("/reports/inventory")
def inventory_reports():

    items = InventoryItem.query.all()
    categories = InventoryCategory.query.all()

    total_items = len(items)

    # Low stock detection
    low_stock_items = [
        item for item in items if float(item.quantity) <= 5
    ]

    # Inventory totals by category
    category_totals = {}

    for item in items:

        if item.category:
            category = item.category.name
        else:
            category = "Uncategorized"

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += float(item.quantity)

    return render_template(
        "reports/inventory_reports.html",
        items=items,
        categories=categories,
        total_items=total_items,
        low_stock_items=low_stock_items,
        category_totals=category_totals
    )


################################################
# FINANCE REPORTS
################################################

@main.route("/reports/finance")
def finance_reports():

    transactions = FinanceTransaction.query.order_by(
        FinanceTransaction.date.desc()
    ).all()

    income = sum(
        float(t.amount) for t in transactions if t.type == "income"
    )

    expenses = sum(
        float(t.amount) for t in transactions if t.type == "expense"
    )

    profit = income - expenses

    return render_template(
        "reports/finance_reports.html",
        transactions=transactions,
        income=income,
        expenses=expenses,
        profit=profit
    )