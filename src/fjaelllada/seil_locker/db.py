
from fjaelllada.db.card_db import CardDatabase
from fjaelllada.db.log import RotatingLog
from fjaelllada.db.totp_db import TotpDatabase


card_db = CardDatabase('card_db.txt')
admin_db = TotpDatabase('admin_db.txt')
log = RotatingLog('log.log', 5, 5*1024*1024)

for entry in card_db.get_all():
    print(f"Registered user {entry!r}")
for entry in admin_db.get_all():
    print(f"Registered admin {entry!r}")
