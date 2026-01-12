import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def get_order_sum(conn, month):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(
            """
            SELECT c.customer_name, COALESCE(SUM(o.total_amount), 0) as total
            FROM customers c
            LEFT JOIN orders o
                ON c.customer_id = o.customer_id
                AND EXTRACT(MONTH FROM o.order_date) = %s
            GROUP BY c.customer_name
            HAVING COALESCE(SUM(o.total_amount), 0) > 0
            ORDER BY c.customer_name ASC
            """,
            (month,)
        )
        rows = cur.fetchall()
    lines = [
        f'Покупатель {row["customer_name"]} совершил покупок на сумму {int(row["total"])}'
        for row in rows
    ]
    return "\n".join(lines)

# END
