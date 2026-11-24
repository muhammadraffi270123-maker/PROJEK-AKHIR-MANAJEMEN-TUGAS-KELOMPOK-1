from datetime import datetime


class Pengguna:
    # pilihan yang boleh dipakai (milik class, bukan milik satu object)
    DAFTAR_STATUS = ["belum dikerjakan", "sedang dikerjakan", "selesai"]
    DAFTAR_PRIORITAS = ["rendah", "sedang", "tinggi"]

    def __init__(self, id_pengguna, nama):
        # atribut private (diawali __), tidak bisa diakses langsung dari luar class
        self.__id_pengguna = id_pengguna
        self.__nama = "Tanpa Nama"
        self.__daftar_tugas = []
        self.__id_tugas_berikutnya = 1
        self.__pesan_terakhir = ""

        # isi nama lewat setter supaya ikut divalidasi
        self.nama = nama

    # ---------- id_pengguna (hanya bisa dibaca) ----------
    @property
    def id_pengguna(self):
        return self.__id_pengguna

    # ---------- nama (bisa dibaca dan diubah, dengan validasi) ----------
    @property
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, nama_baru):
        nama_baru = nama_baru.strip()
        if nama_baru == "":
            self.__pesan_terakhir = "Nama tidak boleh kosong."
            return
        self.__nama = nama_baru
        self.__pesan_terakhir = ""

    # ---------- pesan_terakhir (hanya bisa dibaca) ----------
    @property
    def pesan_terakhir(self):
        return self.__pesan_terakhir

    # ---------- method bantu (private): cek format tenggat ----------
    def __cek_tenggat(self, tenggat):
        # kembalikan tenggat yang sudah rapi (TTTT-BB-HH), atau None kalau tidak valid
        try:
            tanggal = datetime.strptime(tenggat.strip(), "%Y-%m-%d")
        except ValueError:
            return None
        return tanggal.strftime("%Y-%m-%d")

    # ---------- tambah tugas ----------
    def tambah_tugas(self, judul, deskripsi, tenggat, prioritas):
        judul = judul.strip()
        deskripsi = deskripsi.strip()
        prioritas = prioritas.strip().lower()

        if judul == "":
            self.__pesan_terakhir = "Judul tugas tidak boleh kosong."
            return False

        if prioritas not in Pengguna.DAFTAR_PRIORITAS:
            self.__pesan_terakhir = "Prioritas harus rendah, sedang, atau tinggi."
            return False

        tenggat_rapi = self.__cek_tenggat(tenggat)
        if tenggat_rapi is None:
            self.__pesan_terakhir = "Tenggat tidak valid. Gunakan format TTTT-BB-HH, contoh 2026-12-31."
            return False

        tugas = {
            "id_tugas": self.__id_tugas_berikutnya,
            "judul": judul,
            "deskripsi": deskripsi,
            "tenggat": tenggat_rapi,
            "prioritas": prioritas,
            "status": "belum dikerjakan",
        }
        self.__daftar_tugas.append(tugas)
        self.__id_tugas_berikutnya += 1
        self.__pesan_terakhir = "Tugas berhasil ditambahkan."
        return True

    # ---------- ambil seluruh tugas ----------
    def tampilkan_tugas(self):
        # kembalikan salinan daftar tugas supaya daftar asli tidak bisa diubah dari luar
        hasil = []
        for tugas in self.__daftar_tugas:
            hasil.append(tugas.copy())
        return hasil

    # ---------- method bantu (private): cari tugas berdasarkan id ----------
    def __cari_tugas_by_id(self, id_tugas):
        for tugas in self.__daftar_tugas:
            if tugas["id_tugas"] == id_tugas:
                return tugas
        return None

    # ---------- ubah isi tugas ----------
    def ubah_tugas(self, id_tugas, judul=None, deskripsi=None, tenggat=None, prioritas=None):
        tugas = self.__cari_tugas_by_id(id_tugas)
        if tugas is None:
            self.__pesan_terakhir = "Tugas dengan ID tersebut tidak ditemukan."
            return False

        if judul is None and deskripsi is None and tenggat is None and prioritas is None:
            self.__pesan_terakhir = "Tidak ada bagian yang diubah."
            return False

        # siapkan nilai baru dulu, simpan ke tugas hanya kalau semuanya valid
        judul_baru = tugas["judul"]
        deskripsi_baru = tugas["deskripsi"]
        tenggat_baru = tugas["tenggat"]
        prioritas_baru = tugas["prioritas"]

        if judul is not None:
            judul_baru = judul.strip()
            if judul_baru == "":
                self.__pesan_terakhir = "Judul tugas tidak boleh kosong."
                return False

        if deskripsi is not None:
            deskripsi_baru = deskripsi.strip()

        if tenggat is not None:
            tenggat_baru = self.__cek_tenggat(tenggat)
            if tenggat_baru is None:
                self.__pesan_terakhir = "Tenggat tidak valid. Gunakan format TTTT-BB-HH, contoh 2026-12-31."
                return False

        if prioritas is not None:
            prioritas_baru = prioritas.strip().lower()
            if prioritas_baru not in Pengguna.DAFTAR_PRIORITAS:
                self.__pesan_terakhir = "Prioritas harus rendah, sedang, atau tinggi."
                return False

        tugas["judul"] = judul_baru
        tugas["deskripsi"] = deskripsi_baru
        tugas["tenggat"] = tenggat_baru
        tugas["prioritas"] = prioritas_baru
        self.__pesan_terakhir = "Tugas berhasil diubah."
        return True

    # ---------- ubah status tugas ----------
    def ubah_status(self, id_tugas, status_baru):
        tugas = self.__cari_tugas_by_id(id_tugas)
        if tugas is None:
            self.__pesan_terakhir = "Tugas dengan ID tersebut tidak ditemukan."
            return False

        status_baru = status_baru.strip().lower()
        if status_baru not in Pengguna.DAFTAR_STATUS:
            self.__pesan_terakhir = "Status harus belum dikerjakan, sedang dikerjakan, atau selesai."
            return False

        tugas["status"] = status_baru
        self.__pesan_terakhir = "Status tugas berhasil diubah."
        return True

    # ---------- tandai selesai ----------
    def tandai_selesai(self, id_tugas):
        return self.ubah_status(id_tugas, "selesai")

    # ---------- hapus tugas ----------
    def hapus_tugas(self, id_tugas):
        tugas = self.__cari_tugas_by_id(id_tugas)
        if tugas is None:
            self.__pesan_terakhir = "Tugas dengan ID tersebut tidak ditemukan."
            return False

        self.__daftar_tugas.remove(tugas)
        self.__pesan_terakhir = "Tugas berhasil dihapus."
        return True

    # ---------- cari tugas berdasarkan kata kunci ----------
    def cari_tugas(self, kata_kunci):
        kata_kunci = kata_kunci.strip().lower()
        if kata_kunci == "":
            self.__pesan_terakhir = "Kata kunci tidak boleh kosong."
            return []

        hasil = []
        for tugas in self.__daftar_tugas:
            if kata_kunci in tugas["judul"].lower() or kata_kunci in tugas["deskripsi"].lower():
                hasil.append(tugas.copy())

        if len(hasil) == 0:
            self.__pesan_terakhir = "Tidak ada tugas yang cocok dengan kata kunci."
        else:
            self.__pesan_terakhir = "Ditemukan " + str(len(hasil)) + " tugas."
        return hasil