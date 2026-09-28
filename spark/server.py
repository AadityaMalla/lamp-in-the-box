import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .appName("lamp-spark-sql")
         .master("local[1]")
         .config("spark.driver.memory", "512m")
         .config("spark.ui.port", "4040")
         .getOrCreate())
spark.sparkContext.setLogLevel("WARN")

spark.createDataFrame(
    [(1, "Alice", "Computer Science"), (2, "Bob", "Mathematics"), (3, "Carol", "Physics")],
    ["id", "name", "major"],
).createOrReplaceTempView("students")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/students":
            rows = spark.sql("SELECT id, name, major FROM students ORDER BY id").collect()
            body, code = json.dumps([r.asDict() for r in rows]).encode(), 200
        elif self.path == "/health":
            body, code = b'{"status":"ok"}', 200
        else:
            body, code = b'{"error":"not found"}', 404
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

print("Spark SQL service listening on :9000", flush=True)
HTTPServer(("0.0.0.0", 9000), Handler).serve_forever()
