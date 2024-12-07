
from fjaelllada.db.card_db import CardDatabase
from fjaelllada.db.totp_db import TotpDatabase


card_db = CardDatabase('card_db.txt')
admin_db = TotpDatabase('admin_db.txt')
