from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database

app = Flask(__name__)
app.secret_key = '7985'  # Replace with a real secret key

db = Database()

@app.route('/')
def dashboard():
    try:
        expiry_alerts = db.get_expiry_alerts()
        return render_template('dashboard.html', expiry_alerts=expiry_alerts)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('dashboard.html', expiry_alerts=[])

@app.route('/set_reorder_threshold', methods=['GET', 'POST'])
def set_reorder_threshold():
    if request.method == 'POST':
        try:
            medication_id = request.form['medication_id']
            threshold = request.form['threshold']
            if db.set_reorder_threshold(medication_id, threshold):
                flash('Reorder threshold updated successfully!', 'success')
            else:
                flash('Failed to update reorder threshold.', 'error')
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('set_reorder_threshold'))
    
    medications = db.get_all_medications()
    return render_template('set_reorder_threshold.html', medications=medications)

@app.route('/historical_usage')
def historical_usage():
    try:
        medication_id = request.args.get('medication_id')
        period = request.args.get('period', 'month')
        usage_data = db.get_historical_usage(medication_id, period)
        medications = db.get_all_medications()
        return render_template('historical_usage.html', usage_data=usage_data, medications=medications)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('historical_usage.html', usage_data=[], medications=[])

@app.route('/expiry_alerts')
def expiry_alerts():
    try:
        alerts = db.get_expiry_alerts()
        return render_template('expiry_alerts.html', alerts=alerts)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('expiry_alerts.html', alerts=[])

@app.route('/acknowledge_alert/<int:alert_id>')
def acknowledge_alert(alert_id):
    try:
        if db.acknowledge_alert(alert_id):
            flash('Alert acknowledged successfully!', 'success')
        else:
            flash('Failed to acknowledge alert.', 'error')
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
    return redirect(url_for('expiry_alerts'))

@app.route('/inventory_report')
def inventory_report():
    try:
        report_data = db.generate_inventory_report()
        return render_template('inventory_report.html', report_data=report_data)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('inventory_report.html', report_data=[])

@app.route('/update_inventory', methods=['GET', 'POST'])
def update_inventory():
    if request.method == 'POST':
        try:
            medication_id = request.form['medication_id']
            quantity = request.form['quantity']
            if db.update_inventory(medication_id, quantity):
                flash('Inventory updated successfully!', 'success')
            else:
                flash('Failed to update inventory.', 'error')
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('update_inventory'))
    
    medications = db.get_all_medications()
    return render_template('update_inventory.html', medications=medications)

if __name__ == '__main__':
    app.run(debug=True)