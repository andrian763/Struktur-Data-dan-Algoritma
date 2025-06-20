import heapq
import time
from threading import Timer
from datetime import datetime, timedelta

class Patient:
    queue_green = []
    queue_yellow = []
    queue_red = []

    @classmethod
    def enqueue(cls, patient):
        if patient.severity == 1:
            heapq.heappush(cls.queue_green, patient)
        elif patient.severity == 2:
            heapq.heappush(cls.queue_yellow, patient)
        elif patient.severity == 3:
            heapq.heappush(cls.queue_red, patient)
        print("Pasien", patient.name, "telah ditambahkan ke dalam antrian.")

    @classmethod
    def dequeue(cls):
        if cls.queue_red:
            return heapq.heappop(cls.queue_red)
        elif cls.queue_yellow:
            return heapq.heappop(cls.queue_yellow)
        elif cls.queue_green:
            return heapq.heappop(cls.queue_green)
        else:
            return None

    @classmethod
    def get_queue_list(cls):
        sorted_queue = sorted(cls.queue_red, reverse=True) + sorted(cls.queue_yellow, reverse=True) + sorted(cls.queue_green, reverse=True)
        return sorted_queue

    @classmethod
    def search_patient(cls, name):
        all_queues = cls.queue_red + cls.queue_yellow + cls.queue_green
        for patient in all_queues:
            if patient.name.lower() == name.lower():
                print(f"Pasien ditemukan: {patient.name}, Usia: {patient.age}, Gejala: {patient.symptoms}, Keparahan: {patient.severity}, Alamat: {patient.address}")
                return
        print("Pasien tidak ditemukan.")

    @classmethod
    def add_patient(cls, service):
        if service.available_ambulances > 0:
            print("\n+-------------------------------+")
            print("|       Input Data Pasien       |")
            print("+-------------------------------+")
            name = input("Masukkan nama pasien: ")
            age = input("Masukkan usia pasien: ")
            symptoms = input("Masukkan gejala pasien: ")
            address = input("Masukkan alamat pasien: ")
            print("+------------------------------------------------------------------+")
            print("|                          Tingkat Keparahan                       |")
            print("+----+--------------+----------------------+-----------------------+")
            print("| No | Warna        | Kategori             | Kondisi Penyakit/Luka |")
            print("+----+--------------+----------------------+-----------------------+")
            print("| 1  | Hijau        | Ringan               | Luka ringan           |")
            print("| 2  | Kuning       | Sedang               | Luka sedang           |")
            print("| 3  | Merah        | Kritis               | Luka berat            |")
            print("+----+--------------+----------------------+-----------------------+")
            severity = int(input("Masukkan tingkat keparahan (1-3): "))
            patient = Patient(name, age, symptoms, severity, address)
            cls.enqueue(patient)
            wait_min, wait_max = service.wait_time[severity]
            print(f"Estimasi waktu tunggu untuk pasien {name} adalah antara {wait_min}-{wait_max} menit.")
        else:
            print("Maaf, tidak ada ambulan yang tersedia saat ini.")

    def __init__(self, name, age, symptoms, severity, address):
        self.name = name
        self.age = age
        self.symptoms = symptoms
        self.severity = severity
        self.address = address

    def __lt__(self, other):
        return self.severity > other.severity

    def notify(self):
        print(f"Ambulan menuju ke alamat: {self.address}")
        print(f"Pasien {self.name} dengan tingkat keparahan {self.severity} telah diambil untuk diangkut ke rumah sakit.")
        print("Data pasien:")
        print("Nama:", self.name)
        print("Usia:", self.age)
        print("Gejala:", self.symptoms)

    def estimate_arrival_time(self, wait_time):
        wait_min, wait_max = wait_time[self.severity]
        traffic_factor = 1
        estimated_time = datetime.now() + timedelta(minutes=(wait_min + wait_max) / 2 * traffic_factor)
        return estimated_time

class AmbulanceService:
    def __init__(self):
        self.available_ambulances = 3  # Jumlah ambulans yang tersedia
        self.max_ambulances = 3  # Batas maksimum ambulans yang dapat tersedia
        self.wait_time = {1: (10, 15), 2: (7, 10), 3: (5, 5)}

    def add_ambulance(self):
        if self.available_ambulances < self.max_ambulances:
            self.available_ambulances += 1
            print(f"Ambulans ditambahkan. Jumlah ambulans yang tersedia: {self.available_ambulances}.")
        else:
            print("Tidak bisa menambahkan ambulan karena sudah mencapai batas maksimum.")

    def remove_ambulance(self):
        if self.available_ambulances > 1:
            self.available_ambulances -= 1
            print(f"Ambulans dikurangi. Jumlah ambulans yang tersedia: {self.available_ambulances}.")
        else:
            print("Tidak bisa mengurangi ambulans lebih lanjut.")

    def use_ambulance(self):
        if self.available_ambulances > 0:
            self.available_ambulances -= 1
            Timer(180, self.release_ambulance).start()  # 180 detik atau 3 menit
        else:
            print("Tidak ada ambulans yang tersedia untuk digunakan.")

    def release_ambulance(self):
        if self.available_ambulances < self.max_ambulances:
            self.available_ambulances += 1
            print("Satu ambulans telah kembali dan sekarang tersedia.")

    def check_ambulance_status(self):
        if self.available_ambulances == 0:
            print("Semua ambulans sedang digunakan. Harap tunggu hingga ambulans tersedia.")
        elif self.available_ambulances == self.max_ambulances:
            print("Semua ambulans tersedia. Tidak ada ambulans yang sedang digunakan.")
        else:
            print(f"Terdapat {self.available_ambulances} ambulans yang tersedia.")

def print_horizontal_line():
    print("+--------------------------------+")

def main():
    service = AmbulanceService()
    while True:
        print("\n+------------------------+")
        print("|        Pilihan         |")
        print("+------------------------+")
        print("| 1. Daftar pasien       |")
        print("| 2. Ambil pasien        |")
        print("| 3. Daftar antrian      |")
        print("| 4. Tambahkan ambulan   |")
        print("| 5. Kurangi ambulan     |")
        print("| 6. Status Ambulan      |")
        print("| 7. Cari pasien         |")
        print("| 8. Keluar              |")
        print("+------------------------+")
        choice = input("Pilih opsi: ")
        if choice == "1":
            Patient.add_patient(service)
        elif choice == "2":
            if service.available_ambulances > 0:
                next_patient = Patient.dequeue()
                if next_patient:
                    service.use_ambulance()
                    next_patient.notify()
                    arrival_time = next_patient.estimate_arrival_time(service.wait_time)
                    print(f"Estimasi waktu kedatangan ambulans: {arrival_time}")
                else:
                    print("Tidak ada pasien dalam antrian.")
            else:
                print("Semua ambulans sedang digunakan. Harap tunggu hingga ambulans tersedia.")
        elif choice == "3":
            print("\nDaftar Antrian:")
            queue_list = Patient.get_queue_list()
            print("+----+----------------------+----------------------+")
            print("| No | Nama                 | Keparahan            |")
            print("+----+----------------------+----------------------+")
            for index, patient in enumerate(queue_list, start=1):
                name_str = str(patient.name)
                severity_str = str(patient.severity)
                print(f"| {str(index).ljust(2)} | {name_str.ljust(20)} | {severity_str.ljust(20)} |")
            print("+----+----------------------+----------------------+")
        elif choice == "4":
            service.add_ambulance()
        elif choice == "5":
            service.remove_ambulance()
        elif choice == "6":
            service.check_ambulance_status()
        elif choice == "7":
            name = input("Masukkan nama pasien yang ingin dicari: ")
            Patient.search_patient(name)
        elif choice == "8":
            break

if __name__ == "__main__":
    main()
