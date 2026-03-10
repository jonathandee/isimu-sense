from flask import render_template, request, redirect, url_for
from . import main
from .. import db
from ..models import FinanceTransaction, FinanceCategory


################################################
# FINANCE DASHBOARD
################################################

@main.route("/finance")
def finance():

    return render_template("finance.html")


################################################
# FINANCE TRANSACTIONS
################################################

@main.route("/finance/transactions", methods=["GET", "POST"])
def finance_transactions():

    categories = FinanceCategory.query.all()

    if request.method == "POST":

        type = request.form.get("type")
        category_id = request.form.get("category")
        description = request.form.get("description")
        amount = request.form.get("amount")
        date = request.form.get("date")
        notes = request.form.get("notes")

        # Basic validation
        if not type or not category_id or not amount or not date:
            return redirect(url_for("main.finance_transactions"))

        transaction = FinanceTransaction(
            type=type,
            category_id=category_id,
            description=description,
            amount=amount,
            date=date,
            notes=notes
        )

        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for("main.finance_transactions"))

    transactions = FinanceTransaction.query.order_by(
        FinanceTransaction.date.desc()
    ).all()

    return render_template(
        "finance_transactions.html",
        transactions=transactions,
        categories=categories
    )


################################################
# FINANCE CATEGORIES (CONFIGURATION)
################################################

@main.route("/finance/categories", methods=["GET", "POST"])
def finance_categories():

    if request.method == "POST":

        name = request.form.get("name")
        type = request.form.get("type")
        description = request.form.get("description")

        category = FinanceCategory(
            name=name,
            type=type,
            description=description
        )

        db.session.add(category)
        db.session.commit()

        return redirect(url_for("main.finance_categories"))

    categories = FinanceCategory.query.order_by(
        FinanceCategory.type
    ).all()

    return render_template(
        "finance_categories.html",
        categories=categories
    )


@main.route("/finance/categories/edit/<int:id>", methods=["POST"])
def edit_finance_category(id):

    category = FinanceCategory.query.get_or_404(id)

    category.name = request.form.get("name")
    category.type = request.form.get("type")
    category.description = request.form.get("description")

    db.session.commit()

    return redirect(url_for("main.finance_categories"))


@main.route("/finance/categories/delete/<int:id>")
def delete_finance_category(id):

    category = FinanceCategory.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()

    return redirect(url_for("main.finance_categories"))