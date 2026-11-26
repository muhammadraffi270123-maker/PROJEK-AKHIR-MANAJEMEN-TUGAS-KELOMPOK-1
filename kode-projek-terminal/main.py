from pengguna import Pengguna
from datetime import datetime


# ---------- fungsi bantu untuk input/output ----------
def cetak_tugas(daftar):
    # daftar = list berisi dictionary tugas
    if len(daftar) == 0:
        print("Tidak ada tugas yang ditampilkan.")
        return

    for tugas in daftar:
        print("-" * 40)
        print("ID         :", tugas["id_tugas"])
        print("Judul      :", tugas["judul"])
        print("Deskripsi  :", tugas["deskripsi"])
        print("Tenggat    :", tugas["tenggat"])
        print("Prioritas  :", tugas["prioritas"])
        print("Status     :", tugas["status"])
    print("-" * 40)


def baca_id():
    # kembalikan ID berupa angka, atau None kalau input bukan angka
    teks = input("Masukkan ID tugas: ")
    try:
        return int(teks)
    except ValueError:
        print("ID harus berupa angka.")
        return None


def baca_opsional(pertanyaan):
    # kalau dikosongkan (langsung Enter), kembalikan None artinya "tidak diubah"
    teks = input(pertanyaan)
    if teks.strip() == "":
        return None
    return teks


def pilih_dari_daftar(judul, daftar_pilihan):
    # tampilkan pilihan bernomor, kembalikan pilihan yang dipilih (atau None kalau salah)
    print(judul)
    for i in range(len(daftar_pilihan)):
        print("  " + str(i + 1) + ". " + daftar_pilihan[i])

    teks = input("Pilih nomor: ")
    try:
        nomor = int(teks)
    except ValueError:
        print("Pilihan harus berupa angka.")
        return None

    if nomor < 1 or nomor > len(daftar_pilihan):
        print("Nomor pilihan tidak tersedia.")
        return None
    return daftar_pilihan[nomor - 1]


# ---------- satu fungsi untuk tiap menu ----------
def menu_tambah(pengguna):
    judul = input("Judul     : ")
    deskripsi = input("Deskripsi : ")

    while True:
        tenggat = input("Tenggat (TTTT-BB-HH, contoh 2026-12-31): ")

        try:
            datetime.strptime(tenggat, "%Y-%m-%d")
            break
        except ValueError:
            print("Format tanggal salah. Gunakan format TTTT-BB-HH.")
            print("Contoh: 2026-12-31")

    prioritas = pilih_dari_daftar("Prioritas:", Pengguna.DAFTAR_PRIORITAS)

    if prioritas is None:
        return

    pengguna.tambah_tugas(judul, deskripsi, tenggat, prioritas)
    print(pengguna.pesan_terakhir)


def menu_lihat(pengguna):
    cetak_tugas(pengguna.tampilkan_tugas())


def menu_ubah(pengguna):
    id_tugas = baca_id()
    if id_tugas is None:
        return

    print("Kosongkan (Enter) kalau bagian itu tidak ingin diubah.")
    judul = baca_opsional("Judul baru     : ")
    deskripsi = baca_opsional("Deskripsi baru : ")
    tenggat = baca_opsional("Tenggat baru   : ")
    prioritas = baca_opsional("Prioritas baru (rendah/sedang/tinggi): ")

    pengguna.ubah_tugas(id_tugas, judul, deskripsi, tenggat, prioritas)
    print(pengguna.pesan_terakhir)


def menu_ubah_status(pengguna):
    id_tugas = baca_id()
    if id_tugas is None:
        return

    status = pilih_dari_daftar("Status baru:", Pengguna.DAFTAR_STATUS)
    if status is None:
        return

    pengguna.ubah_status(id_tugas, status)
    print(pengguna.pesan_terakhir)


def menu_tandai_selesai(pengguna):
    id_tugas = baca_id()
    if id_tugas is None:
        return

    pengguna.tandai_selesai(id_tugas)
    print(pengguna.pesan_terakhir)


def menu_hapus(pengguna):
    id_tugas = baca_id()
    if id_tugas is None:
        return

    yakin = input("Yakin ingin menghapus tugas ini? (y/n): ")
    if yakin.strip().lower() != "y":
        print("Penghapusan dibatalkan.")
        return

    pengguna.hapus_tugas(id_tugas)
    print(pengguna.pesan_terakhir)


def menu_cari(pengguna):
    kata_kunci = input("Kata kunci: ")
    hasil = pengguna.cari_tugas(kata_kunci)
    print(pengguna.pesan_terakhir)
    cetak_tugas(hasil)


def menu_filter(pengguna):
    jenis = pilih_dari_daftar("Filter berdasarkan:", ["status", "prioritas"])
    if jenis == "status":
        status = pilih_dari_daftar("Status:", Pengguna.DAFTAR_STATUS)
        if status is None:
            return
        hasil = pengguna.filter_tugas(status=status)
    elif jenis == "prioritas":
        prioritas = pilih_dari_daftar("Prioritas:", Pengguna.DAFTAR_PRIORITAS)
        if prioritas is None:
            return
        hasil = pengguna.filter_tugas(prioritas=prioritas)
    else:
        return

    print(pengguna.pesan_terakhir)
    cetak_tugas(hasil)


def menu_terlambat(pengguna):
    hasil = pengguna.cek_terlambat()
    print(pengguna.pesan_terakhir)
    cetak_tugas(hasil)


def tampilkan_menu(pengguna):
    print()
    print("=== SISTEM MANAJEMEN TUGAS ===")
    print("Pengguna:", pengguna.nama, "(ID " + str(pengguna.id_pengguna) + ")")
    print("1. Tambah tugas")
    print("2. Lihat semua tugas")
    print("3. Ubah tugas")
    print("4. Ubah status tugas")
    print("5. Tandai tugas selesai")
    print("6. Hapus tugas")
    print("7. Cari tugas")
    print("8. Filter tugas")
    print("9. Cek tugas terlambat")
    print("0. Keluar")


# ---------- program utama ----------
def main():
    nama = input("Masukkan nama Anda: ")
    while nama.strip() == "":
        print("Nama tidak boleh kosong.")
        nama = input("Masukkan nama Anda: ")

    pengguna = Pengguna(1, nama)

    while True:
        tampilkan_menu(pengguna)
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            menu_tambah(pengguna)
        elif pilihan == "2":
            menu_lihat(pengguna)
        elif pilihan == "3":
            menu_ubah(pengguna)
        elif pilihan == "4":
            menu_ubah_status(pengguna)
        elif pilihan == "5":
            menu_tandai_selesai(pengguna)
        elif pilihan == "6":
            menu_hapus(pengguna)
        elif pilihan == "7":
            menu_cari(pengguna)
        elif pilihan == "8":
            menu_filter(pengguna)
        elif pilihan == "9":
            menu_terlambat(pengguna)
        elif pilihan == "0":
            print("Terima kasih, sampai jumpa!")
            break
        else:
            print("Menu tidak tersedia, pilih angka 0-9.")


main()
