from __future__ import print_function


from googleapiclient.discovery import build
from datetime import date, datetime, timedelta
import mysql.connector


class GoogleSearch(object):
    def __init__(self):
        service = build("customsearch",
                        version="v1",
                        developerKey="AIzaSyBqCJbcpp1RzPzVi5aR5DyARY84X7o24Uo")
        self.querier = service.cse()

    def query(self, query_string):
        query_op = self.querier.list(q=query_string,
                                     cx='017576662512468239146:omuauf_lfve').excute()
        response = query_op.excute()
        return response

    def process_response(self, response):
        pass

    def save_to_mysql(self):
        cnx = mysql.connector.connect(user='scott', database='employees')
        cursor = cnx.cursor()

        tomorrow = datetime.now().date() + timedelta(days=1)

        add_employee = ("INSERT INTO employees "
                        "(first_name, last_name, hire_date, gender, birth_date) "
                        "VALUES (%s, %s, %s, %s, %s)")
        add_salary = ("INSERT INTO salaries "
                      "(emp_no, salary, from_date, to_date) "
                      "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

        data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

        # Insert new employee
        cursor.execute(add_employee, data_employee)
        emp_no = cursor.lastrowid

        # Insert salary information
        data_salary = {
            'emp_no': emp_no,
            'salary': 50000,
            'from_date': tomorrow,
            'to_date': date(9999, 1, 1),
        }
        cursor.execute(add_salary, data_salary)

        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()
        cnx.close()