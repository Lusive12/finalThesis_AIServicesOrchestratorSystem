# Ekstraksi Komprehensif Dokumen: `5024231007_Rendy Lexxy K_Draft_DIKUMPULIN.pdf`

> **Sumber Asli:** `C:\Users\User\Documents\AntiGravity\proof-concept-smartkiosk\docs\5024231007_Rendy Lexxy K_Draft_DIKUMPULIN.pdf`  
> **Jumlah Halaman:** 27  
> **Tujuan:** Digest representasi teks lengkap, tabel, dan gambar untuk referensi AI tugas akhir tanpa memangkas detail teknis.

---


## --- Halaman 1 ---


![Gambar Halaman 1 (5024231007_Rendy Lexxy K_Draft_DIKUMPULIN_p1_img1.png)](images/5024231007_Rendy Lexxy K_Draft_DIKUMPULIN_p1_img1.png)

PROPOSAL TUGAS AKHIR - TD123456
SISTEM ORKESTRASI LAYANAN AI BERBASIS
MICROSERVICES PADA SISTEM SMART KIOSK
Rendy Lexxy Kurniawan
NRP 5024231007
Dosen Pembimbing
Arta Kusuma Hernanda, S.T., M.T.
NIP 1996202311024
Dr. Diah Puspito Wulandari, S.T.,M.Sc.
NIP 19801219200501 2 001
Program Studi Strata 1 (S1) Teknik Komputer
Departemen Teknik Komputer
Fakultas Teknologi Elektro dan Informatika Cerdas
Institut Teknologi Sepuluh Nopember
Surabaya
2077


## --- Halaman 2 ---

[Halaman ini sengaja dikosongkan]


## --- Halaman 3 ---

LEMBAR PENGESAHAN
SISTEM ORKESTRASI LAYANAN AI BERBASIS MICROSERVICES PADA SISTEM
SMART KIOSK
PROPOSAL TUGAS AKHIR
Diajukan untuk memenuhi salah satu syarat memperoleh gelar Sarjana Teknik pada Program Studi S-1
Teknik Komputer
Departemen Teknik Komputer
Fakultas Teknik Elektro dan Informatika Cerdas
Institut Teknologi Sepuluh Nopember
Oleh: Rendy Lexxy Kurniawan
NRP. 5024231007
Disetujui Oleh:
Arta Kusuma Hernanda, S.T., M.T.
NIP: 1996202311024
(Pembimbing)
Dr. Diah Puspito Wulandari, S.T.,M.Sc.
NIP: 19801219200501 2 001
(Ko-Pembimbing)
Mengetahui,
Kepala Departemen Teknik Komputer FTEIC-ITS
Dr. Arief Kurniawan, S.T., M.T.
NIP 19740907200212 1 001
SURABAYA
Mei, 2027


## --- Halaman 4 ---

[Halaman ini sengaja dikosongkan]


## --- Halaman 5 ---

ABSTRAK
SISTEM ORKESTRASI LAYANAN AI BERBASIS MICROSERVICES
PADA SISTEM SMART KIOSK
Nama Mahasiswa / NRP: Rendy Lexxy Kurniawan / 5024231007
Departemen
: Teknik Komputer - ITS
Dosen Pembimbing
: 1. Arta Kusuma Hernanda, S.T., M.T.
2. Dr. Diah Puspito Wulandari, S.T.,M.Sc.
Abstrak
Penerapan kecerdasan buatan (Artificial Intelligence/AI) pada smart kiosk memungkinkan
penyediaan layanan interaktif yang beragam. Namun, menjalankan beberapa layanan AI se-
cara bersamaan dapat meningkatkan penggunaan sumber daya komputasi, khususnya mem-
ori GPU (VRAM), sehingga berpotensi memengaruhi kinerja dan stabilitas sistem. Penelitian
ini bertujuan mengembangkan sistem orkestrasi layanan AI berbasis microservices pada smart
kiosk dengan sistem operasi Linux. Sistem dikembangkan dalam bentuk aplikasi desktop yang
mengintegrasikan antarmuka pengguna dengan mekanisme pengelolaan siklus hidup layanan
AI berbasis kontainer. Orkestrator mengatur aktivasi dan penghentian layanan sesuai kebu-
tuhan untuk mengendalikan penggunaan sumber daya GPU lokal. Metode penelitian meliputi
analisis kebutuhan, pemilihan model AI, perancangan arsitektur, implementasi, integrasi, dan
pengujian sistem. Evaluasi dilakukan dengan membandingkan skenario beberapa layanan aktif
secara bersamaan dan aktivasi satu layanan secara bergantian. Parameter pengujian mencakup
penggunaan CPU, RAM, GPU, dan VRAM, waktu aktivasi dan pergantian layanan, serta latensi
inferensi. Penelitian ini diharapkan menghasilkan mekanisme orkestrasi yang mendukung pen-
gelolaan sumber daya komputasi secara efisien dan stabil.
Kata Kunci: orkestrasi layanan AI, microservices, smart kiosk, manajemen sumber daya
GPU, edge computing


## --- Halaman 6 ---

[Halaman ini sengaja dikosongkan]


## --- Halaman 7 ---

ABSTRACT
ORCHESTRATION SYSTEM OF AI SERVICES BASED ON
MICROSERVICES FOR SMART KIOSKS
Student Name / NRP: Rendy Lexxy Kurniawan / 5024231007
Department
: Computer Engineering FTEIC - ITS
Advisor
: 1. Arta Kusuma Hernanda, S.T., M.T.
2. Dr. Diah Puspito Wulandari, S.T.,M.Sc.
Abstract
The integration of Artificial Intelligence (AI) into smart kiosks enables diverse interactive
services. However, running multiple AI services simultaneously can increase computational
resource consumption, particularly GPU memory (VRAM), potentially affecting system per-
formance and stability. This research aims to develop a microservices-based AI service orches-
tration system for a smart kiosk running on Linux. The system is implemented as a desktop
application that integrates a user interface with container-based AI service lifecycle manage-
ment. The orchestrator controls service activation and termination according to operational
requirements to regulate local GPU resource utilization. The research methodology includes
requirements analysis, AI model selection, architecture design, implementation, integration,
and system testing. Evaluation is conducted by comparing scenarios in which multiple services
run simultaneously and individual services are activated sequentially. The evaluation metrics
include CPU, RAM, GPU, and VRAM utilization, service activation and switching time, and
inference latency. This research is expected to produce an orchestration mechanism that sup-
ports efficient and stable computational resource management for AI services in Linux-based
smart kiosks.
Keywords: AI service orchestration, microservices, smart kiosk, GPU resource management,
edge computing


## --- Halaman 8 ---

[Halaman ini sengaja dikosongkan]


## --- Halaman 9 ---

DAFTAR ISI
ABSTRAK
v
DAFTAR ISI
ix
DAFTAR GAMBAR
xi
DAFTAR TABEL
xiii
1
PENDAHULUAN
1
1.1
Latar Belakang . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
1
1.2
Rumusan Masalah . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
2
1.3
Batasan Masalah atau Ruang Lingkup . . . . . . . . . . . . . . . . . . . . . .
2
1.4
Tujuan . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3
1.5
Manfaat
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3
1.5.1
Manfaat Teoritis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3
1.5.2
Manfaat Praktis
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3
2
TINJAUAN PUSTAKA
5
2.1
Hasil penelitian/perancangan terdahulu . . . . . . . . . . . . . . . . . . . . .
5
2.1.1
CEC: A Containerized Edge Computing Framework for Dynamic Resource
Provisioning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5
2.1.2
SensiX++: Bringing MLOps and Multi-Tenant Model Serving to Sensory
Edge Devices
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5
2.1.3
Exploring GPU Sharing Techniques for Edge AI Smart City Applications . .
6
2.2
Teori/Konsep Dasar
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
2.2.1
Smart Kiosk . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
2.2.2
Edge Computing dan Local AI Inference . . . . . . . . . . . . . . . . . . .
6
2.2.3
Microservices . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
2.2.4
Containerization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
ix


## --- Halaman 10 ---

2.2.5
Service orchestration
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
2.2.6
GPU, VRAM, dan Resource Contention . . . . . . . . . . . . . . . . . . .
7
3
METODOLOGI
9
3.1
Metode yang digunakan . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
3.2
Bahan dan peralatan yang digunakan . . . . . . . . . . . . . . . . . . . . . .
9
3.2.1
Hardware
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
3.2.2
Software . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
3.3
Urutan Pelaksanaan Penelitian . . . . . . . . . . . . . . . . . . . . . . . . . .
10
3.3.1
Analisis Kebutuhan Sistem
. . . . . . . . . . . . . . . . . . . . . . . . . .
10
3.3.2
Pemilihan Model AI . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
3.3.3
Perancangan Arsitektur Sistem . . . . . . . . . . . . . . . . . . . . . . . .
10
3.3.4
Implementasi Layanan AI dalam Kontainer . . . . . . . . . . . . . . . . . .
10
3.3.5
Pengembangan Aplikasi Desktop dan Orkestrator
. . . . . . . . . . . . . .
10
3.3.6
Integrasi dan Pengujian Fungsional . . . . . . . . . . . . . . . . . . . . . .
10
3.3.7
Pengujian Kinerja Sistem . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
3.3.8
Analisis Hasil Pengujian . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11
DAFTAR PUSTAKA
13
x


## --- Halaman 11 ---

DAFTAR GAMBAR
xi


## --- Halaman 12 ---

[Halaman ini sengaja dikosongkan]


## --- Halaman 13 ---

DAFTAR TABEL
xiii


## --- Halaman 14 ---

[Halaman ini sengaja dikosongkan]


## --- Halaman 15 ---

BAB 1 PENDAHULUAN
1.1
Latar Belakang
Perkembangan teknologi digital mendorong transformasi kios konvensional menjadi smart
kiosk yang mampu menyediakan layanan interaktif berbasis teknologi komputasi. Integrasi
kecerdasan buatan (Artificial Intelligence atau AI) memungkinkan perangkat tersebut meng-
hadirkan berbagai fungsi, seperti pengenalan visual, pemrosesan bahasa, dan sistem rekomen-
dasi, untuk mendukung interaksi yang lebih adaptif dengan pengguna [1]. Seiring dengan
meningkatnya kebutuhan terhadap layanan tersebut, satu perangkat smart kiosk berpotensi men-
jalankan beberapa aplikasi AI dengan fungsi yang berbeda. Kondisi ini menuntut sistem yang
tidak hanya mampu menyediakan berbagai layanan, tetapi juga mengelola operasionalnya se-
cara terintegrasi dan menjaga kestabilan selama digunakan.
Salah satu aspek penting dalam penerapan AI pada smart kiosk adalah penentuan lingkun-
gan komputasi untuk menjalankan layanan. Pemrosesan melalui cloud computing memungkinkan
aplikasi memanfaatkan sumber daya komputasi eksternal, sedangkan edge computing memu-
ngkinkan pemrosesan dilakukan lebih dekat dengan pengguna, termasuk secara langsung pada
perangkat lokal [2]. Pemrosesan lokal berpotensi mengurangi ketergantungan terhadap ko-
munikasi jaringan untuk proses inferensi, tetapi kebutuhan komputasinya harus dipenuhi oleh
perangkat yang digunakan. Sebaliknya, penggunaan layanan awan dapat melibatkan keter-
gantungan terhadap konektivitas jaringan serta biaya yang bergantung pada penyedia dan pola
penggunaan layanan. Oleh karena itu, penerapan AI lokal pada smart kiosk memerlukan pen-
gelolaan sumber daya yang memadai agar berbagai layanan dapat dijalankan secara efektif.
Kebutuhan pengelolaan sumber daya tersebut menjadi semakin penting ketika beberapa
layanan AI dijalankan pada perangkat yang sama. Model AI dapat menggunakan kapasitas
memori dan komputasi GPU yang cukup besar, sehingga eksekusi beberapa model secara bersamaan
berpotensi menimbulkan persaingan sumber daya (resource contention).
Kondisi ini dapat
memengaruhi waktu respons, kebutuhan memori, dan kestabilan operasional sistem, terutama
ketika kapasitas perangkat terbatas [3], [4]. Dengan demikian, menjalankan seluruh layanan AI
secara bersamaan tidak selalu menjadi pendekatan yang sesuai untuk setiap skenario penggu-
naan. Diperlukan mekanisme yang mampu mengatur layanan mana yang perlu dijalankan atau
dihentikan sesuai kebutuhan, sekaligus mempertimbangkan ketersediaan sumber daya kom-
putasi lokal.
Untuk menjawab kebutuhan tersebut, pendekatan microservices dapat digunakan untuk
memisahkan aplikasi menjadi layanan-layanan yang memiliki fungsi dan tanggung jawab ter-
tentu serta berkomunikasi melalui antarmuka yang terdefinisi [2], [4]. Namun, pemisahan ap-
likasi menjadi beberapa layanan belum cukup untuk memastikan seluruh layanan dapat berop-
erasi secara terkoordinasi. Diperlukan sistem orkestrasi yang mengelola siklus hidup layanan,
memantau status operasional, dan mengoordinasikan penggunaan layanan sesuai kebutuhan ap-
likasi [5]. Dalam konteks smart kiosk, orkestrasi memungkinkan pengelolaan beberapa layanan
AI dilakukan melalui satu sistem terpadu, termasuk pengaturan aktivasi dan penghentian layanan
untuk membantu mengendalikan penggunaan sumber daya. Dengan pendekatan tersebut, kom-
pleksitas pengoperasian beberapa layanan dapat dikelola tanpa mengharuskan seluruh layanan
aktif secara bersamaan.
Berdasarkan permasalahan tersebut, penelitian ini berfokus pada pengembangan Sistem
Orkestrasi Layanan AI Berbasis Microservices pada Sistem Smart Kiosk yang dijalankan pada
1


## --- Halaman 16 ---

sistem operasi Linux. Sistem ini ditujukan untuk mengintegrasikan beberapa layanan AI ke
dalam satu aplikasi desktop serta mengoordinasikan operasional layanan melalui mekanisme
orkestrasi. Pengelolaan sumber daya GPU lokal menjadi salah satu fokus utama, khususnya
dalam pengaturan siklus hidup layanan pada perangkat yang menggunakan NVIDIA GeForce
RTX 5060. Evaluasi dilakukan dengan mengukur penggunaan CPU, RAM, GPU, dan VRAM,
waktu pemuatan dan pergantian layanan, waktu respons, serta kestabilan operasional sistem.
Hasil evaluasi diharapkan dapat menunjukkan kemampuan sistem orkestrasi dalam mendukung
pengoperasian beberapa layanan AI secara terkoordinasi pada smart kiosk dengan sumber daya
komputasi lokal yang terbatas.
1.2
Rumusan Masalah
Berdasarkan identifikasi pada latar belakang, maka rumusan masalah dalam penelitian ini
adalah:
a. Bagaimana mengembangkan sistem orkestrasi layanan AI berbasis microservices untuk
mengintegrasikan beberapa layanan AI pada sistem smart kiosk?
b. Bagaimana mengelola siklus hidup layanan AI dan penggunaan sumber daya GPU lokal
agar layanan dapat dijalankan sesuai kebutuhan operasional smart kiosk?
c. Bagaimana kinerja sistem orkestrasi yang dikembangkan berdasarkan penggunaan sum-
ber daya komputasi, waktu pemuatan dan perpindahan layanan, waktu respons, serta sta-
bilitas sistem?
1.3
Batasan Masalah atau Ruang Lingkup
Untuk menjaga agar penelitian ini tetap fokus dan terarah, ditetapkan beberapa batasan
masalah sebagai berikut:
a. Lingkungan sistem: Penelitian dilakukan pada satu perangkat smart kiosk yang men-
jalankan sistem operasi Linux. Pengelolaan klaster multi-node dan orkestrasi layanan
pada infrastruktur cloud tidak menjadi bagian dari implementasi.
b. Perangkat keras: Pengujian menggunakan perangkat dengan GPU lokal NVIDIA GeForce
RTX 5060. Hasil pengujian merepresentasikan lingkungan perangkat keras dan konfig-
urasi yang digunakan selama penelitian.
c. Layanan AI: Penelitian menggunakan layanan atau model AI yang telah tersedia dan/atau
dikembangkan oleh anggota tim terkait. Pengembangan model AI baru, pelatihan model
dari awal, serta evaluasi akurasi model bukan fokus utama penelitian.
d. Pendekatan layanan: Layanan AI dikelola menggunakan pendekatan microservices. Se-
tiap layanan yang dikategorikan sebagai microservice harus memiliki fungsi dan antar-
muka komunikasi yang jelas. Penggunaan container dapat mendukung isolasi dan penge-
masan layanan, tetapi bukan satu-satunya kriteria penentuan arsitektur microservices.
e. Fungsi orkestrasi: Sistem berfokus pada integrasi layanan, pengelolaan siklus hidup
layanan, pemantauan status layanan, dan koordinasi permintaan pengguna menuju layanan
yang sesuai.
2


## --- Halaman 17 ---

f. Pengelolaan GPU: Pengelolaan sumber daya GPU dibatasi pada tingkat aplikasi dan sik-
lus hidup layanan atau model, seperti menjalankan, menghentikan, memuat, atau melepas
model sesuai kebutuhan. Penelitian tidak mencakup modifikasi driver GPU, virtualisasi
GPU, pengaturan tingkat kernel, maupun pengembangan penjadwal GPU tingkat rendah.
g. Antarmuka pengguna: Antarmuka dirancang sebagai aplikasi desktop layar penuh den-
gan orientasi potret 9:16 untuk penggunaan pada smart kiosk berbasis layar sentuh. In-
teraksi suara dan gestur tidak menjadi bagian inti implementasi.
h. Evaluasi kinerja: Evaluasi mencakup penggunaan CPU, RAM, GPU, dan VRAM; waktu
pemuatan layanan atau model; waktu perpindahan layanan; waktu respons inferensi; serta
indikator kegagalan dan stabilitas sistem. Metrik akhir disesuaikan dengan instrumen pe-
mantauan dan skenario pengujian yang tersedia.
i. Batas evaluasi: Penelitian tidak berfokus pada perbandingan total biaya cloud dengan
komputasi lokal, pengukuran akurasi model AI, atau perbandingan berbagai metode pen-
jadwalan GPU tingkat rendah. Evaluasi usability antarmuka dapat digunakan sebagai
evaluasi pendukung apabila dilaksanakan.
1.4
Tujuan
Penelitian Tugas Akhir ini bertujuan untuk mengatasi permasalahan yang telah dirumuskan.
Tujuan tersebut adalah sebagai berikut:
a. Mengembangkan sistem orkestrasi layanan AI berbasis microservices untuk menginte-
grasikan beberapa layanan AI pada sistem smart kiosk.
b. Menerapkan mekanisme pengelolaan siklus hidup layanan AI dan penggunaan sumber
daya GPU lokal sesuai kebutuhan operasional smart kiosk.
c. Mengevaluasi kinerja sistem berdasarkan penggunaan sumber daya komputasi, waktu pe-
muatan dan perpindahan layanan, waktu respons, serta stabilitas sistem.
1.5
Manfaat
1.5.1
Manfaat Teoritis
Penelitian ini diharapkan dapat menambah kajian mengenai penerapan orkestrasi layanan
AI berbasis microservices pada perangkat edge dengan sumber daya komputasi lokal. Penelitian
juga dapat memberikan gambaran mengenai hubungan antara pengelolaan siklus hidup layanan
AI, penggunaan sumber daya GPU, dan kinerja operasional sistem smart kiosk.
1.5.2
Manfaat Praktis
Penelitian ini diharapkan menghasilkan sistem yang dapat digunakan untuk menginte-
grasikan beberapa layanan AI dalam satu lingkungan smart kiosk, serta menyediakan mekanisme
pengelolaan layanan yang lebih terkoordinasi. Selain itu, hasil evaluasi dapat menjadi bahan
pertimbangan dalam menentukan strategi pengelolaan layanan AI pada perangkat dengan keter-
batasan sumber daya lokal.
3


## --- Halaman 18 ---

[Halaman ini sengaja dikosongkan]


## --- Halaman 19 ---

BAB 2 TINJAUAN PUSTAKA
2.1
Hasil penelitian/perancangan terdahulu
Pada bagian ini, akan dibahas hasil penelitian terdahulu yang relevan dengan penelitian
yang akan dilakukan. Penelitian terdahulu tersebut akan dibahas berdasarkan metode yang
digunakan, hasil yang diperoleh, dan kesimpulan yang diambil.
2.1.1
CEC: A Containerized Edge Computing Framework for Dynamic Resource Pro-
visioning
Hu et al. [5] mengembangkan CEC (*Containerized Edge Computing*), sebuah kerangka
kerja berbasis kontainer untuk menyediakan sumber daya secara dinamis pada server edge.
Penelitian ini dilatarbelakangi oleh perubahan beban permintaan layanan dan keterlambatan
aktivasi kontainer yang dapat memengaruhi latensi layanan serta efisiensi pemanfaatan sumber
daya.
Metode yang digunakan adalah menggabungkan algoritma prediksi permintaan layanan se-
cara periodik dengan mekanisme *resource pre-provisioning* berbasis pengendali adaptif. Ke-
butuhan sumber daya kontainer dipersiapkan berdasarkan distribusi permintaan yang diprediksi.
Evaluasi melalui simulasi dan eksperimen pada lingkungan pengujian menunjukkan bahwa
mekanisme yang diusulkan dapat meningkatkan akurasi prediksi serta menghasilkan latensi
layanan lebih rendah dan utilisasi sumber daya lebih tinggi dibandingkan pendekatan pem-
banding [5].
Hasil dari penelitian ini memiliki relevansi tinggi karena membahas pengelolaan kontainer,
waktu aktivasi layanan, dan efisiensi sumber daya pada komputasi edge. Perbedaannya ter-
letak pada mekanisme dan lingkup penerapan. CEC berfokus pada penyediaan sumber daya
berdasarkan prediksi permintaan, sedangkan tugas akhir ini berfokus pada orkestrasi layanan AI
dalam satu smart kiosk berbasis Linux, termasuk pengelolaan siklus hidup layanan dan penggu-
naan GPU lokal. Oleh karena itu, CEC menjadi acuan untuk memahami hubungan pengelolaan
kontainer dengan kinerja sistem tanpa mengharuskan penerapan algoritma prediksi permintaan
yang sama.
2.1.2
SensiX++: Bringing MLOps and Multi-Tenant Model Serving to Sensory Edge
Devices
Min et al. [4] mengembangkan SensiX++, sistem *multi-tenant model serving* dengan
kemampuan MLOps terintegrasi untuk perangkat edge, seperti kamera, mikrofon, dan sensor
IoT. Sistem ini mengintegrasikan pengelolaan siklus hidup sensor, transformasi data, eksekusi
model, serta penyediaan hasil inferensi melalui microservices dan REST API [4].
Metode yang digunakan adalah koordinator data, *resource-aware model server*, dan pen-
jadwal adaptif untuk mengelola beberapa model pada akselerator heterogen. Evaluasi terhadap
sepuluh model visi komputer dan akustik menggunakan perangkat seperti NVIDIA Jetson AGX
dan Coral TPU menunjukkan kemampuan sistem dalam mengelola eksekusi multi-tenant serta
mengurangi kompleksitas operasional model pada perangkat edge [4].
Hasil dari penelitian ini memiliki relevansi tinggi karena membahas pengelolaan beberapa
model AI pada perangkat dengan sumber daya terbatas. Namun, penelitian tersebut berfokus
pada perangkat sensor, otomatisasi pipeline data, dan penjadwalan eksekusi model. Sebaliknya,
tugas akhir ini berfokus pada orkestrasi layanan AI dalam satu smart kiosk, termasuk integrasi
layanan, perpindahan layanan, dan pengelolaan siklus hidup model berdasarkan kebutuhan op-
erasional. Dengan demikian, SensiX++ menjadi acuan untuk memahami pengelolaan model
5


## --- Halaman 20 ---

AI lokal tanpa mengharuskan seluruh mekanisme internalnya diterapkan.
2.1.3
Exploring GPU Sharing Techniques for Edge AI Smart City Applications
Woo et al. [3] meneliti teknik penggunaan bersama GPU untuk aplikasi AI pada perangkat
edge. Penelitian ini menggunakan NVIDIA Jetson AGX Orin untuk mengkaji pengaruh pelak-
sanaan beberapa beban kerja AI terhadap waktu penyelesaian pekerjaan, penggunaan memori,
dan utilisasi GPU [3].
Metode yang digunakan adalah membandingkan pendekatan threading dan multiprocess-
ing menggunakan beban kerja deteksi objek berbasis YOLOv8. Hasilnya menunjukkan bahwa
threading dapat mengurangi penggunaan memori melalui berbagi konteks CUDA, sedangkan
multiprocessing dapat meningkatkan utilisasi GPU dan memperpendek waktu inferensi pada
skenario tertentu. Namun, kedua pendekatan memiliki keterbatasan akibat persaingan sumber
daya dan overhead sinkronisasi. Pada kondisi tertentu, peningkatan jumlah beban kerja secara
bersamaan justru menurunkan kinerja [3].
Hasil dari penelitian ini memiliki relevansi tinggi karena menjelaskan risiko persaingan
sumber daya ketika beberapa layanan AI menggunakan GPU lokal. Perbedaannya, penelitian
tersebut berfokus pada teknik berbagi GPU, sedangkan tugas akhir ini berfokus pada orkestrasi
layanan AI dalam smart kiosk. Pemahaman mengenai persaingan sumber daya digunakan se-
bagai dasar untuk mengatur aktivasi dan penghentian layanan. Evaluasi diarahkan pada peng-
gunaan GPU dan VRAM, waktu perpindahan layanan, waktu respons, serta kestabilan sistem,
bukan pengembangan mekanisme berbagi GPU tingkat rendah.
2.2
Teori/Konsep Dasar
2.2.1
Smart Kiosk
Smart kiosk merupakan kios layanan mandiri yang mengintegrasikan perangkat komputasi,
antarmuka interaktif, dan perangkat lunak untuk menyediakan layanan kepada pengguna. Inte-
grasi AI memungkinkan kios menjalankan fungsi seperti rekomendasi, pengenalan objek, dan
pemrosesan masukan pengguna.
Chen et al. [1] mengembangkan MiniDeep, platform AI edge yang menerapkan model
deep learning pada sistem kios restoran cepat saji. Penelitian tersebut menunjukkan penerapan
integrasi layanan AI dengan antarmuka kios melalui arsitektur cloud-edge [1].
Dalam tugas akhir ini, smart kiosk menjadi platform yang mengintegrasikan beberapa
layanan AI melalui satu antarmuka. Sistem membutuhkan orkestrator untuk mengoordinasikan
akses pengguna, aktivasi layanan, dan penggunaan sumber daya lokal.
2.2.2
Edge Computing dan Local AI Inference
Edge computing merupakan paradigma komputasi yang menempatkan pemrosesan data
dekat dengan sumber data atau pengguna untuk mengurangi ketergantungan terhadap infras-
truktur cloud dan komunikasi jarak jauh. *Local AI inference* adalah proses menjalankan
model AI pada perangkat lokal untuk menghasilkan prediksi berdasarkan data masukan.
Chiang et al. [6] menjelaskan bahwa komputasi edge dapat mengurangi latensi komu-
nikasi, tetapi menimbulkan tantangan dalam pengelolaan layanan dan sumber daya. MiniDeep
[1] juga menunjukkan penerapan inferensi AI pada perangkat edge dalam sistem kios.
Pada penelitian ini, inferensi lokal digunakan agar layanan AI dapat berjalan pada perangkat
smart kiosk berbasis Linux. Keterbatasan CPU, GPU, dan memori menjadi pertimbangan dalam
mengatur layanan yang aktif.
2.2.3
Microservices
Microservices merupakan arsitektur yang membagi aplikasi menjadi layanan-layanan kecil
dengan tanggung jawab fungsional tertentu. Setiap layanan dapat dikembangkan, dijalankan,
6


## --- Halaman 21 ---

dan dikelola secara relatif independen serta berkomunikasi melalui antarmuka yang ditentukan,
seperti REST API.
Velepucha dan Flores [7] membahas prinsip modularitas, pola desain, serta kelebihan dan
tantangan arsitektur microservices. Pemisahan layanan mendukung pemeliharaan dan pengem-
bangan modular, tetapi juga menambah kebutuhan komunikasi dan pengelolaan komponen.
Dalam tugas akhir ini, microservices digunakan untuk memisahkan layanan AI berdasarkan
fungsinya. Orkestrator mengoordinasikan akses ke layanan tersebut pada satu perangkat Linux,
sehingga setiap layanan dapat dikelola tanpa harus menggabungkan seluruh fungsi ke dalam
satu aplikasi monolitik.
2.2.4
Containerization
Containerization merupakan teknik pengemasan aplikasi beserta dependensinya ke dalam
lingkungan eksekusi terisolasi yang berbagi kernel sistem operasi host. Pada Linux, mekanisme
seperti namespaces dan control groups (cgroups) mendukung isolasi proses serta pengaturan
sumber daya [8], [9].
Hu et al. [5] mengkaji penggunaan kontainer untuk penyediaan sumber daya edge, sedan-
gkan Min et al. [4] menggunakan kontainer untuk mendukung eksekusi model AI. Kontainer
membantu menjaga konsistensi lingkungan layanan, tetapi aktivasi kontainer dan pemuatan
model tetap dapat menimbulkan overhead.
Penelitian ini menggunakan containerization untuk mengemas layanan AI agar lebih mu-
dah diterapkan dan dikelola secara terpisah. Dukungan GPU perlu dikonfigurasi melalui run-
time yang sesuai, misalnya NVIDIA Container Toolkit, agar layanan di dalam kontainer dapat
mengakses GPU host [10].
2.2.5
Service orchestration
Service orchestration merupakan koordinasi layanan untuk memastikan setiap kompo-
nen dijalankan sesuai kebutuhan operasional sistem. Proses ini dapat mencakup aktivasi dan
penghentian layanan, pengelolaan dependensi, pemantauan status, serta pengaturan urutan ek-
sekusi.
Chiang et al. [6] membahas orkestrasi dan pengelolaan sumber daya pada komputasi edge,
sedangkan Hu et al. [5] meneliti penyediaan sumber daya kontainer secara dinamis. Keduanya
menjadi landasan untuk memahami hubungan antara koordinasi layanan dan efisiensi sumber
daya.
Dalam penelitian ini, orkestrator berjalan pada Linux dan mengoordinasikan layanan AI
pada satu smart kiosk. Ketika pengguna memilih fungsi tertentu, orkestrator dapat mengak-
tifkan layanan yang dibutuhkan dan menghentikan layanan yang tidak lagi diperlukan. Pen-
dekatan ini ditujukan untuk mengelola penggunaan sumber daya lokal, bukan mengorkestrasi
banyak server terdistribusi.
2.2.6
GPU, VRAM, dan Resource Contention
GPU merupakan perangkat pemrosesan paralel yang banyak digunakan untuk inferensi
AI. VRAM adalah memori GPU yang digunakan untuk menyimpan parameter model, data,
dan kebutuhan komputasi lainnya. *Resource contention* terjadi ketika beberapa beban kerja
bersaing menggunakan sumber daya komputasi yang sama.
Woo et al. [3] menunjukkan bahwa teknik berbagi GPU memiliki kompromi antara peng-
gunaan memori, utilisasi GPU, dan waktu inferensi. Min et al. [4] juga membahas tantangan
pengelolaan beberapa model AI pada perangkat edge dengan sumber daya terbatas.
Dalam tugas akhir ini, GPU dan VRAM menjadi sumber daya yang diperhatikan oleh
orkestrator. Aktivasi dan penghentian layanan secara terkoordinasi dapat mengurangi kebu-
7


## --- Halaman 22 ---

tuhan menjalankan banyak model secara bersamaan. Namun, strategi tersebut juga dapat menam-
bah waktu pemuatan model ketika layanan diaktifkan kembali.
8


## --- Halaman 23 ---

BAB 3 METODOLOGI
3.1
Metode yang digunakan
Penelitian ini menggunakan metode pengembangan sistem dan pengujian eksperimental.
Penelitian dilakukan untuk mengembangkan sistem orkestrasi layanan AI berbasis microser-
vices pada smart kiosk berbasis Linux. Secara spesifik, penelitian berfokus pada pengelolaan
siklus hidup layanan AI yang dijalankan secara lokal menggunakan GPU NVIDIA RTX 5060.
Kinerja sistem dievaluasi dengan membandingkan penggunaan sumber daya komputasi, waktu
pemuatan dan perpindahan layanan, serta latensi inferensi pada skenario beberapa layanan aktif
bersamaan dan satu layanan aktif pada satu waktu.
3.2
Bahan dan peralatan yang digunakan
Untuk merealisasikan sistem yang diusulkan, dibutuhkan komponen perangkat keras (hard-
ware) dan perangkat lunak (software) sebagai berikut:
3.2.1
Hardware
a. Komputer Smart Kiosk: Komputer berbasis Linux dengan GPU NVIDIA RTX 5060
yang digunakan untuk menjalankan aplikasi desktop, orkestrator, dan layanan AI secara
lokal.
b. Perangkat Layar Sentuh: Layar dengan orientasi potret dan rasio aspek 9:16 yang di-
gunakan sebagai media interaksi pengguna dengan aplikasi smart kiosk.
c. Penyimpanan Internal: Digunakan untuk menyimpan kode sumber, konfigurasi kon-
tainer, dependensi perangkat lunak, model AI, log, dan data hasil pengujian.
3.2.2
Software
a. Sistem Operasi: Linux sebagai lingkungan pengembangan dan pengoperasian sistem
smart kiosk.
b. Bahasa Pemrograman: Python untuk backend orkestrator dan pengelolaan layanan,
serta Dart untuk pengembangan aplikasi desktop menggunakan Flutter.
c. Pustaka dan Kerangka Kerja (Framework):
i. Flutter Desktop: Untuk membangun antarmuka aplikasi smart kiosk dalam tampi-
lan layar penuh.
ii. FastAPI: Untuk menyediakan API komunikasi antara aplikasi desktop, backend
orkestrator, dan layanan AI.
iii. Docker Engine dan Docker SDK for Python: Untuk menjalankan serta mengelola
siklus hidup kontainer layanan AI melalui backend orkestrator.
iv. NVIDIA Driver dan NVIDIA Container Toolkit: Untuk mendukung akses GPU
NVIDIA dari lingkungan kontainer.
v. Model AI dan Framework Inferensi: Model AI diambil dari implementasi yang
tersedia di internet dan dipilih berdasarkan fungsi, kompatibilitas GPU, serta kebu-
tuhan sumber daya komputasi.
vi. Perangkat Pemantauan: nvidia-smi dan Docker Stats untuk memantau penggu-
naan GPU, VRAM, CPU, dan RAM selama pengujian.
9


## --- Halaman 24 ---

3.3
Urutan Pelaksanaan Penelitian
3.3.1
Analisis Kebutuhan Sistem
Tahap awal dilakukan dengan menentukan kebutuhan fungsional sistem smart kiosk. Ke-
butuhan tersebut meliputi pemilihan layanan AI melalui antarmuka desktop, aktivasi dan penghen-
tian layanan, pengiriman permintaan inferensi, serta penampilan hasil pemrosesan. Pada tahap
ini juga ditentukan metrik pengujian berupa penggunaan CPU, RAM, GPU, VRAM, waktu
pemuatan layanan, waktu perpindahan layanan, dan latensi inferensi.
3.3.2
Pemilihan Model AI
Model AI dipilih dari implementasi yang tersedia di internet berdasarkan fungsi layanan
yang dibutuhkan, kompatibilitas dengan Linux dan GPU NVIDIA RTX 5060, kebutuhan VRAM,
serta ketersediaan dokumentasi dan antarmuka pemanggilan. Setiap kandidat diuji secara mandiri
untuk memastikan model dapat dijalankan secara lokal dan menghasilkan keluaran yang sesuai.
Model yang memenuhi kriteria kemudian ditetapkan sebagai layanan AI penelitian.
3.3.3
Perancangan Arsitektur Sistem
Tahap ini dilakukan dengan merancang hubungan antara aplikasi desktop, backend orkestra-
tor, dan layanan AI. Flutter digunakan untuk antarmuka pengguna, FastAPI untuk menan-
gani komunikasi dan logika orkestrasi, sedangkan Docker digunakan untuk menjalankan setiap
layanan AI dalam kontainer terpisah. Pada tahap ini juga ditentukan kontrak API, konfigurasi
layanan, dan mekanisme pemeriksaan kesiapan layanan berdasarkan kebutuhan implementasi
microservices [11], [12].
3.3.4
Implementasi Layanan AI dalam Kontainer
Setiap model AI terpilih disiapkan sebagai layanan yang dapat menerima permintaan melalui
API dan mengembalikan hasil inferensi. Dependensi dan konfigurasi model dikemas ke dalam
kontainer Docker, kemudian akses GPU dikonfigurasi menggunakan NVIDIA Container Toolkit.
Setiap kontainer diuji secara mandiri untuk memastikan model dapat dimuat, menerima per-
mintaan, menghasilkan keluaran, dan menggunakan GPU sesuai kebutuhan.
3.3.5
Pengembangan Aplikasi Desktop dan Orkestrator
Aplikasi desktop dikembangkan menggunakan Flutter dengan tampilan layar penuh beror-
ientasi potret. Antarmuka menyediakan menu pemilihan layanan, masukan pengguna, indikator
status, dan tampilan hasil inferensi. Backend orkestrator dikembangkan menggunakan FastAPI
dan Docker SDK for Python untuk menjalankan, memeriksa kesiapan, menghentikan, serta
mengalihkan permintaan ke layanan AI yang sesuai. Mekanisme perpindahan layanan diran-
cang untuk menghentikan layanan sebelumnya sebelum mengaktifkan layanan tujuan.
3.3.6
Integrasi dan Pengujian Fungsional
Aplikasi desktop, backend orkestrator, dan seluruh layanan AI diintegrasikan menjadi satu
sistem. Pengujian dilakukan dengan memilih layanan melalui antarmuka, memeriksa aktivasi
kontainer, mengirimkan permintaan inferensi, dan memastikan hasil ditampilkan dengan be-
nar. Pengujian juga mencakup perpindahan layanan serta penanganan kegagalan aktivasi dan
permintaan. Kesalahan yang ditemukan diperbaiki sebelum pengujian kinerja dilakukan.
3.3.7
Pengujian Kinerja Sistem
Pengujian dilakukan dengan membandingkan dua skenario, yaitu beberapa layanan AI ak-
tif secara bersamaan dan satu layanan AI aktif pada satu waktu. Kedua skenario dijalankan
menggunakan model, konfigurasi, dan masukan uji yang sama sejauh memungkinkan. Peng-
gunaan CPU, RAM, GPU, dan VRAM dipantau menggunakan perangkat pemantauan sistem,
sedangkan waktu pemuatan, waktu perpindahan, latensi inferensi, dan keberhasilan permintaan
dicatat melalui log orkestrator. Setiap kondisi pengujian diulang secara konsisten agar hasilnya
10


## --- Halaman 25 ---

dapat dibandingkan.
3.3.8
Analisis Hasil Pengujian
Data hasil pengujian dikelompokkan berdasarkan skenario dan layanan AI, kemudian di-
analisis menggunakan statistik deskriptif, seperti rata-rata, nilai minimum, maksimum, dan
simpangan baku. Hasil kedua skenario dibandingkan untuk mengetahui pengaruh kebijakan
orkestrasi terhadap penggunaan sumber daya komputasi, waktu respons, dan kestabilan sistem.
Hasil analisis digunakan untuk mengevaluasi efektivitas mekanisme orkestrasi serta menyusun
kesimpulan berdasarkan data pengujian.
11


## --- Halaman 26 ---

[Halaman ini sengaja dikosongkan]


## --- Halaman 27 ---

DAFTAR PUSTAKA
[1]
Y.-S. Chen, K.-H. Cheng, C.-S. Hsu, and H.-L. Zhang, “MiniDeep: A standalone AI-edge
platform with a deep learning-based MINI-PC and AI-QSR system,” Sensors, vol. 22,
no. 16, p. 5975, 2022. doi: 10.3390/s22165975
[2]
M. D. Hossain et al., “The role of microservice approach in edge computing: Opportu-
nities, challenges, and research directions,” ICT Express, vol. 9, no. 6, pp. 1162–1182,
2023. doi: 10.1016/j.icte.2023.06.006
[3]
Y. Chiang et al., “Management and orchestration of edge computing for IoT: A com-
prehensive survey,” IEEE Internet of Things Journal, vol. 10, no. 16, pp. 14 307–14 331,
2023. doi: 10.1109/JIOT.2023.3245611
[4]
S. Woo, J. Yeo, J. Kim, and K. Lee, “Exploring GPU sharing techniques for edge AI
smart city applications,” ETRI Journal, vol. 47, no. 5, pp. 855–864, 2025. doi: 10.4218/
etrij.2025-0065
[5]
C. Min, A. Mathur, U. G. Acer, A. Montanari, and F. Kawsar, “SensiX++: Bringing
MLOps and multi-tenant model serving to sensory edge devices,” ACM Transactions on
Embedded Computing Systems, vol. 22, no. 6, pp. 1–27, 2023. doi: 10.1145/3617507
[6]
S. Hu, W. Shi, and G. Li, “CEC: A containerized edge computing framework for dy-
namic resource provisioning,” IEEE Transactions on Mobile Computing, vol. 22, no. 7,
pp. 3840–3854, 2023. doi: 10.1109/TMC.2022.3147800
[7]
V. Velepucha and P. Flores, “A survey on microservices architecture: Principles, patterns
and migration challenges,” IEEE Access, vol. 11, pp. 88 339–88 358, 2023. doi: 10 .
1109/ACCESS.2023.3305687
[8]
Linux Kernel Documentation. “Control group v2,” Accessed: Oct. 12, 2026. [Online].
Available: https://docs.kernel.org/admin-guide/cgroup-v2.html
[9]
Docker Inc. “Resource constraints,” Docker Documentation, Accessed: Oct. 12, 2026.
[Online]. Available: https://docs.docker.com/engine/containers/resource_
constraints/
[10]
NVIDIA. “NVIDIA Container Toolkit,” NVIDIA Container Toolkit Documentation, Ac-
cessed: Oct. 12, 2026. [Online]. Available: https://docs.nvidia.com/datacenter/
cloud-native/container-toolkit/latest/
[11]
Flutter. “Desktop support for flutter. ”[Online]. Available: https://docs.flutter.
dev/platform-integration/desktop
[12]
FastAPI. “FastAPI documentation. ”[Online]. Available: https://fastapi.tiangolo.
com/
[13]
Docker. “Docker SDK for Python. ”[Online]. Available: https://docker-py.readthedocs.
io/en/stable/
[14]
Docker. “Docker container stats. ”[Online]. Available: https://docs.docker.com/
reference/cli/docker/container/stats/
13
