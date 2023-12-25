# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import openpyxl
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    reports = Report.query.all()
    return render_template('index.html', reports=reports)

@app.route('/add_report', methods=['POST'])
def add_report():
    customer_name = request.form['customer_name']
    product_name = request.form['product_name']
    total_amount = request.form['total_amount']

    new_report = Report(customer_name=customer_name, product_name=product_name, total_amount=total_amount)
    db.session.add(new_report)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/download_reports')
def download_reports():
    reports = Report.query.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['ID', 'Customer Name', 'Product Name', 'Total Amount', 'Date'])

    for report in reports:
        ws.append([report.id, report.customer_name, report.product_name, report.total_amount, report.date])

    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    return excel_file

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
