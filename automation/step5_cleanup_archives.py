import os
import time

EXPORT_DIR = "exports"
AGE_LIMIT_DAYS = 7

now = time.time()
for file in os.listdir(EXPORT_DIR):
    path = os.path.join(EXPORT_DIR, file)
    if os.path.isfile(path) and (now - os.path.getmtime(path)) > AGE_LIMIT_DAYS * 86400:
        os.remove(path)
