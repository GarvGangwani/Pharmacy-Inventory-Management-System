import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
    
                database='pharmacy_inventory',
                user='root@localhost',  # Replace with your MySQL username if different
                password='7985'  # Replace with your actual MySQL password
            )
            if self.connection.is_connected():
                print('Connected to MySQL database')
            else:
                print('Failed to connect to MySQL database')
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None

    def _get_cursor(self):
        if self.connection is None or not self.connection.is_connected():
            print("Database connection is not established. Attempting to reconnect...")
            self.connect()
        
        if self.connection is None or not self.connection.is_connected():
            print("Failed to establish database connection.")
            return None
        
        try:
            return self.connection.cursor(dictionary=True)
        except Error as e:
            print(f"Error creating cursor: {e}")
            return None

    def set_reorder_threshold(self, medication_id, threshold):
        cursor = self._get_cursor()
        if cursor is None:
            return False
        try:
            query = "UPDATE medications SET reorder_threshold = %s WHERE id = %s"
            cursor.execute(query, (threshold, medication_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()

    def get_historical_usage(self, medication_id, period):
        cursor = self._get_cursor()
        if cursor is None:
            return []
        try:
            if period == 'month':
                query = """
                SELECT YEAR(usage_date) as year, MONTH(usage_date) as month, SUM(quantity) as total_used
                FROM medication_usage
                WHERE medication_id = %s
                GROUP BY YEAR(usage_date), MONTH(usage_date)
                ORDER BY YEAR(usage_date) DESC, MONTH(usage_date) DESC
                LIMIT 12
                """
            elif period == 'year':
                query = """
                SELECT YEAR(usage_date) as year, SUM(quantity) as total_used
                FROM medication_usage
                WHERE medication_id = %s
                GROUP BY YEAR(usage_date)
                ORDER BY YEAR(usage_date) DESC
                LIMIT 5
                """
            cursor.execute(query, (medication_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def get_expiry_alerts(self):
        cursor = self._get_cursor()
        if cursor is None:
            return []
        try:
            thirty_days_from_now = datetime.now() + timedelta(days=30)
            query = """
            SELECT m.id, m.name, m.expiry_date, m.quantity
            FROM medications m
            WHERE m.expiry_date <= %s AND m.quantity > 0
            ORDER BY m.expiry_date
            """
            cursor.execute(query, (thirty_days_from_now,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def acknowledge_alert(self, alert_id):
        cursor = self._get_cursor()
        if cursor is None:
            return False
        try:
            query = "UPDATE expiry_alerts SET acknowledged = TRUE WHERE id = %s"
            cursor.execute(query, (alert_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()

    def generate_inventory_report(self):
        cursor = self._get_cursor()
        if cursor is None:
            return []
        try:
            query = """
            SELECT id, name, quantity, reorder_threshold, expiry_date
            FROM medications
            ORDER BY name
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def update_inventory(self, medication_id, quantity):
        cursor = self._get_cursor()
        if cursor is None:
            return False
        try:
            query = "UPDATE medications SET quantity = %s WHERE id = %s"
            cursor.execute(query, (quantity, medication_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()

    def get_all_medications(self):
        cursor = self._get_cursor()
        if cursor is None:
            return []
        try:
            query = "SELECT id, name FROM medications ORDER BY name"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def __del__(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print('MySQL connection is closed')