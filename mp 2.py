import csv
import os

nama_file = "dataset_stunting.csv"

kolom = ["PROVINSI", "KABKOTA", "PCT_STUNTING_2018", "PCT_MISKIN_2018", "IPM_2018"]

bobot_stunting = 1 / 3
bobot_miskin = 1 / 3
bobot_ipm = 1 / 3

ambang_tinggi = 0.70
ambang_sedang = 0.50

tanda_anomali = ["1", "1.0", "true", "ya", "yes"]


def baca_data(nama):
    if not os.path.exists(nama):
        print("File", nama, "tidak ditemukan.")
        return []

    with open(nama, "r", newline="", encoding="utf-8-sig") as f:
        data = list(csv.DictReader(f))

    if len(data) == 0:
        print("File kosong atau hanya berisi header.")
        return []

    for k in kolom:
        if k not in data[0]:
            print("Kolom", k, "tidak ditemukan di file.")
            return []

    return data


def cek_angka(teks):
    teks = teks.strip().replace(",", ".")
    if teks.startswith("-"):
        teks = teks[1:]
    if teks == "" or teks == ".":
        return False

    jumlah_titik = 0
    for c in teks:
        if c == ".":
            jumlah_titik += 1
        elif c not in "0123456789":
            return False
    return jumlah_titik <= 1


def ubah_angka(teks):
    return float(teks.strip().replace(",", "."))


def klasifikasi(v):
    if v >= ambang_tinggi:
        return "Tinggi"
    elif v >= ambang_sedang:
        return "Sedang"
    else:
        return "Rendah"


def proses(data, masalah):
    valid = []
    sudah_ada = []
    no_baris = 1

    for row in data:
        no_baris += 1

        anomali = ""
        if "FLAG_ANOMALI" in row and row["FLAG_ANOMALI"] != None:
            anomali = row["FLAG_ANOMALI"].strip().lower()
        if anomali in tanda_anomali:
            masalah.append(f"[anomali] baris {no_baris}: {row['KABKOTA']} ditandai anomali, tidak dihitung")
            continue

        kosong = False
        for k in kolom:
            if row[k] == None or row[k].strip() == "":
                kosong = True
        if kosong:
            masalah.append(f"[tidak valid] baris {no_baris}: ada kolom yang kosong")
            continue

        if not (cek_angka(row["PCT_STUNTING_2018"]) and cek_angka(row["PCT_MISKIN_2018"]) and cek_angka(row["IPM_2018"])):
            masalah.append(f"[tidak valid] baris {no_baris}: ada nilai yang bukan angka")
            continue

        stunting = ubah_angka(row["PCT_STUNTING_2018"])
        miskin = ubah_angka(row["PCT_MISKIN_2018"])
        ipm = ubah_angka(row["IPM_2018"])

        if stunting < 0 or stunting > 100 or miskin < 0 or miskin > 100 or ipm < 0 or ipm > 100:
            masalah.append(f"[tidak valid] baris {no_baris}: nilai di luar rentang 0-100")
            continue

        if ipm == 0:
            masalah.append(f"[tidak valid] baris {no_baris}: IPM tidak boleh 0")
            continue

        provinsi = row["PROVINSI"].strip()
        kabkota = row["KABKOTA"].strip()
        kunci = provinsi.lower() + "|" + kabkota.lower()
        if kunci in sudah_ada:
            masalah.append(f"[duplikat] baris {no_baris}: {kabkota} ({provinsi}) sudah ada, baris pertama dipakai")
            continue
        sudah_ada.append(kunci)

        valid.append({
            "no_baris": no_baris,
            "provinsi": provinsi,
            "kabkota": kabkota,
            "stunting": stunting,
            "miskin": miskin,
            "ipm": ipm,
        })

    if len(valid) == 0:
        return []

    max_stunting = max([d["stunting"] for d in valid])
    max_miskin = max([d["miskin"] for d in valid])
    min_ipm = min([d["ipm"] for d in valid])

    for d in valid:
        if max_stunting > 0:
            d["r_stunting"] = d["stunting"] / max_stunting
        else:
            d["r_stunting"] = 0

        if max_miskin > 0:
            d["r_miskin"] = d["miskin"] / max_miskin
        else:
            d["r_miskin"] = 0

        d["r_ipm"] = min_ipm / d["ipm"]

        v = bobot_stunting * d["r_stunting"] + bobot_miskin * d["r_miskin"] + bobot_ipm * d["r_ipm"]
        d["v"] = round(v, 4)
        d["status"] = klasifikasi(d["v"])

    hasil = valid.copy()
    for i in range(len(hasil)):
        for j in range(i + 1, len(hasil)):
            if hasil[i]["v"] < hasil[j]["v"]:
                hasil[i], hasil[j] = hasil[j], hasil[i]

    for i in range(len(hasil)):
        if i > 0 and hasil[i]["v"] == hasil[i - 1]["v"]:
            hasil[i]["peringkat"] = hasil[i - 1]["peringkat"]
        else:
            hasil[i]["peringkat"] = i + 1

    return hasil


def tabel(hasil):
    garis = "-" * 100
    print(garis)
    print(f"{'No':<4} | {'Kabupaten/Kota':<24} | {'Provinsi':<20} | {'Stunting':<8} | {'Miskin':<7} | {'IPM':<6} | {'V':<6} | {'Status':<7}")
    print(garis)
    for h in hasil:
        print(f"{h['peringkat']:<4} | {h['kabkota'][:24]:<24} | {h['provinsi'][:20]:<20} | {h['stunting']:<8} | {h['miskin']:<7} | {h['ipm']:<6} | {h['v']:<6} | {h['status']:<7}")
    print(garis)


def rekap_status(hasil):
    rekap = {"Rendah": 0, "Sedang": 0, "Tinggi": 0}
    for h in hasil:
        rekap[h["status"]] += 1
    return rekap


def tampil_rekap_status(hasil):
    rekap = rekap_status(hasil)
    print("Total wilayah:", len(hasil))
    print("Tinggi :", rekap["Tinggi"])
    print("Sedang :", rekap["Sedang"])
    print("Rendah :", rekap["Rendah"])


def ambil_tinggi(hasil):
    return [h for h in hasil if h["status"] == "Tinggi"]


def tampil_tinggi(hasil):
    tinggi = ambil_tinggi(hasil)
    if tinggi:
        tabel(tinggi)
        print("Jumlah wilayah berstatus Tinggi:", len(tinggi))
    else:
        print("Tidak ada wilayah berstatus Tinggi.")


def cari_provinsi(hasil, kata):
    kata = kata.strip().lower()
    return [h for h in hasil if kata in h["provinsi"].lower()]


def tampil_cari_provinsi(hasil):
    kata = input("Masukkan nama provinsi: ").strip()
    if kata == "":
        print("Nama provinsi tidak boleh kosong.")
        return

    ketemu = cari_provinsi(hasil, kata)
    if ketemu:
        tabel(ketemu)
        print("Jumlah kabupaten/kota:", len(ketemu))
    else:
        print("Provinsi", kata, "tidak ditemukan.")


def tampil_masalah(masalah):
    if len(masalah) == 0:
        print("Tidak ada data bermasalah.")
        return
    for m in masalah:
        print(m)
    print("Jumlah data bermasalah:", len(masalah))


def tampil_parameter(hasil):
    print("Stunting terbesar   :", max([h["stunting"] for h in hasil]))
    print("Kemiskinan terbesar :", max([h["miskin"] for h in hasil]))
    print("IPM terkecil        :", min([h["ipm"] for h in hasil]))
    print("Bobot tiap kriteria :", round(bobot_stunting, 4))
    print("Status Tinggi jika V >=", ambang_tinggi)
    print("Status Sedang jika V >=", ambang_sedang, ", selain itu Rendah")


if __name__ == "__main__":
    data = baca_data(nama_file)
    masalah = []
    hasil = proses(data, masalah)

    if len(hasil) == 0:
        print("Tidak ada data yang bisa diproses.")
    else:
        print("Jumlah wilayah yang diklasifikasikan:", len(hasil))
        print("Jumlah data bermasalah:", len(masalah))

        while True:
            print("\n===== PRIORITAS PENANGANAN STUNTING (METODE SAW) =====")
            print("1. Tampilkan peringkat dan status")
            print("2. Rekap jumlah wilayah per status")
            print("3. Daftar wilayah berstatus Tinggi")
            print("4. Cari berdasarkan provinsi")
            print("5. Laporan data bermasalah")
            print("6. Parameter SAW")
            print("0. Keluar")

            menu = input("Pilih menu: ").strip()

            if menu == "1":
                tabel(hasil)
            elif menu == "2":
                tampil_rekap_status(hasil)
            elif menu == "3":
                tampil_tinggi(hasil)
            elif menu == "4":
                tampil_cari_provinsi(hasil)
            elif menu == "5":
                tampil_masalah(masalah)
            elif menu == "6":
                tampil_parameter(hasil)
            elif menu == "0":
                print("Terima kasih telah menggunakan program!")
                break
            else:
                print("Menu tidak tersedia.")