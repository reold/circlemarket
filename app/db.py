from deta import Deta

deta = Deta()
user_db = deta.Base("users")
inventory_db = deta.Base("inventory")
media_drive = deta.Drive("media")