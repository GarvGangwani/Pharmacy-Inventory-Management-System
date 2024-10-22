from pharmacy_inventory import Database

# Instantiate the database
db = Database()

# View all medications
medications = db.get_all_medications()
print("Medications:", medications)

# Set reorder threshold for a medication
result = db.set_reorder_threshold(1, 15)
print("Threshold update successful:", result)

# View historical usage
usage = db.get_historical_usage(1, 'month')
print("Historical usage:", usage)

# View expiry alerts
alerts = db.get_expiry_alerts()
print("Expiry alerts:", alerts)

# Generate an inventory report
report = db.generate_inventory_report()
print("Inventory report:", report)

# Update inventory
update_result = db.update_inventory(1, 120)
print("Inventory update successful:", update_result)
