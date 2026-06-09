import json
import os 
from modules.log import infolog, warnlog, errorlog
# make sure to build the above here, otherwise it will fail :(
# i believe this is built now

LOGFILE = "schemas.log"
SCHEMA_PATH = './schemas'

def load_order_schemas() -> list:
    schemas = []
    for schema in os.listdir(SCHEMA_PATH):
        try:
            schemas.insert(json.load(schema))
        except json.JSONDecodeError as e:
            warnlog(LOGFILE,f"Invalid schema detected... {schema} has error {e}")
    return schemas

def save_order_schema(schema_name, schema_contents):
    with open(f"{SCHEMA_PATH}/{schema_name}.json", encoding="utf-8") as schema_file:
        try:
            schema_contents = json.dump(schema_contents)
            f.write(schema_contents)
            return ("200", "Schema written successfully")
        except IOError as e:
            return ("500", f"Schema failed to write with error {e}")
