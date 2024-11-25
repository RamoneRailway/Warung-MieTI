from flask import Flask, render_template, request, redirect, url_for

class Item:
    def __init__(self, name, price):
        self.nama = name
        self.harga = price

class Kasir:
    def __init__(self):
        self.menu_makanan = [
            Item("Mie Ayam Biasa", 10000),
            Item("Mie Ayam Pangsit", 13000),
            Item("Mie Ayam Jamur", 13000),
            Item("Mie Ayam Bakso Biasa", 15000),
            Item("Mie Ayam Pangsit + Jamur", 16000),
            Item("Mie Ayam Pangsit + Bakso", 18000),
            Item("Mie Ayam Jamur + Bakso", 18000),
            Item("Mie Ayam Komplit", 20000),
            Item("Pangsit Rebus", 7000)
        ]
        self.menu_minuman = [
            Item("Air Mineral", 3000),
            Item("Teh Tawar Panas", 3000),
            Item("Es Teh Tawar", 3000),
            Item("Teh Manis Panas", 4000),
            Item("Es Teh Manis", 4000),
            Item("Teh Botol", 4000),
            Item("Jeruk Peras Panas", 5000),
            Item("Es Jeruk Peras", 5000),
            Item("Fanta Susu", 7000)
        ]
        self.keranjang = []

    def tambah_ke_keranjang(self, nomor_item):
        total_items = len(self.menu_makanan) + len(self.menu_minuman)
        if 1 <= nomor_item <= len(self.menu_makanan):
            self.keranjang.append(self.menu_makanan[nomor_item - 1])
        elif len(self.menu_makanan) < nomor_item <= total_items:
            self.keranjang.append(self.menu_minuman[nomor_item - len(self.menu_makanan) - 1])

    def hapus_dari_keranjang(self, nomor_item):
        if 1 <= nomor_item <= len(self.keranjang):
            self.keranjang.pop(nomor_item - 1)

    def hitung_total(self):
        return sum(item.harga for item in self.keranjang)

app = Flask(__name__)
kasir = Kasir()

@app.route("/")
def home():
    return render_template("home.html", makanan=kasir.menu_makanan, minuman=kasir.menu_minuman, keranjang=kasir.keranjang)

@app.route("/tambah/<int:nomor_item>")
def tambah_ke_keranjang(nomor_item):
    kasir.tambah_ke_keranjang(nomor_item)
    return redirect(url_for("home"))

@app.route("/hapus/<int:nomor_item>")
def hapus_dari_keranjang(nomor_item):
    kasir.hapus_dari_keranjang(nomor_item)
    return redirect(url_for("home"))

@app.route("/bayar", methods=["POST"])
def bayar():
    total = kasir.hitung_total()
    jumlah = int(request.form.get("jumlah"))
    if jumlah >= total:
        kembalian = jumlah - total
        kasir.keranjang.clear()
        return render_template("bayar.html", sukses=True, kembalian=kembalian, jumlah=jumlah, total=total)
    else:
        kekurangan = total - jumlah
        return render_template("bayar.html", sukses=False, kekurangan=kekurangan, jumlah=jumlah, total=total)

if __name__ == "__main__":
    app.run(debug=True)
