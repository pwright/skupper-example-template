#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import os
from flask import Flask, Response
from threading import Lock
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "skupper"
app.config["MYSQL_DATABASE_PASSWORD"] = "reppuks"
app.config["MYSQL_DATABASE_DB"] = "skupper"
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
mysql.init_app(app)

host = os.environ.get("BACKEND_SERVICE_HOST", "0.0.0.0")
port = int(os.environ.get("BACKEND_SERVICE_PORT", 8081))

pod = os.environ.get("HOSTNAME", "hello-world-backend")

lock = Lock()
count = 0

@app.errorhandler(Exception)
def error(e):
    app.logger.error(e)
    return Response(f"Trouble! {e}\n", status=500, mimetype="text/plain")

@app.route("/api/hello")
def hello():
    global count

    with lock:
        count += 1
    


    return Response(f" ({count})", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host=host, port=port)
