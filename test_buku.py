from buku import Buku
b1 = Buku("Python OOP", "Lambert", 2017)
b2 = Buku("Clean Code", "Martin", 2008)

print(b1)            # [Tersedia] Python OOP
print(b2)
            
print(b1.pinjam())   # Python OOP dipinjam.
print(b2.pinjam())    

print(b1.pinjam())   # Buku tidak tersedia!
print(b2.pinjam()) 

print(b1.tersedia)   # False
print(b2.tersedia)

b1.tersedia = True   # kembalikan
print(b1)            # [Tersedia] Python OOP

b2.tersedia = True   # kembalikan
print(b2)            # [Tersedia] Clean code