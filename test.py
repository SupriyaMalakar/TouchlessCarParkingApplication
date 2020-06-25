import qrcode

img = qrcode.make('test text')

print(type(img))
print(img.size)