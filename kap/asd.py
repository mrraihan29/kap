with open('db.json', 'rb') as file: content = file.read() 
with open('db.json', 'wb') as file: file.write(content.decode('utf-16').encode('utf-8'))