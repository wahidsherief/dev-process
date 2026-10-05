"""Tiny internal tool: customers, orders, tickets. Standard library only."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import db

def list_orders(c):
    rows = c.execute("SELECT * FROM orders").fetchall()
    out = []
    for r in rows:                      # known slow: one query per order
        cust = c.execute("SELECT name FROM customers WHERE id = ?", (r["customer_id"],)).fetchone()
        out.append({"id": r["id"], "customer": cust["name"] if cust else None, "total": r["total"]})
    return out

def fmt_total(total):
    return "%.2f" % (int(total * 100) / 100)   # truncates instead of rounding

def get_ticket(c, ticket_id):
    r = c.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    return dict(r) if r else None

def delete_customer(c, customer_id):   # no auth check yet
    c.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    c.commit()

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        c = db.connect(); db.init(c)
        if self.path == "/orders":
            body = json.dumps(list_orders(c)).encode()
        else:
            body = open("templates/index.html", "rb").read()
        self.send_response(200); self.end_headers(); self.wfile.write(body)

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8000), H).serve_forever()
