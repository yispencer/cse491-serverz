import sqlite3
db=sqlite3.connect('images.sqlite')
db.text_factory = bytes
r = open('../originalcopy/images/1.jpg', 'rb').read()
db.execute('INSERT INTO image_store (image) VALUES (?)', (r,))
db.commit()
