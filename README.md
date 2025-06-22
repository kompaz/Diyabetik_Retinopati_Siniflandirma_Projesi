# 🧠 Diyabetik Retinopati Sınıflandırma Projesi

Bu proje, diyabet hastalığının ciddi bir komplikasyonu olan **diyabetik retinopati** hastalığını, retina görüntüleri üzerinden **derin öğrenme teknikleriyle sınıflandırmayı** amaçlamaktadır.

## 📌 Proje Hakkında

Diyabetik retinopati, retinadaki kan damarlarının hasar görmesiyle ortaya çıkan ve körlüğe kadar ilerleyebilen ciddi bir göz hastalığıdır. Bu projede, retina görüntülerinden hastalık seviyesini tespit eden bir yapay zeka modeli geliştirilmiş, bunun yanı sıra doktorların teşhis süreçlerini desteklemek için bir **web uygulaması** tasarlanmıştır.

Modelin doğruluk oranı yüksek (**%98**), web arayüzü kullanıcı dostu, veritabanı ise esnek ve ilişkisel yapıdadır. Proje sürecinde hem yazılım mühendisliği pratikleri hem de makine öğrenmesi teknikleri birlikte yürütülmüştür.

---

## 🧪 Kullanılan Teknolojiler

- **Backend**: Python, Flask, SQLAlchemy  
- **Frontend**: HTML, CSS, Bootstrap  
- **Görüntü işleme**: OpenCV, NumPy  
- **Makine öğrenimi / Derin öğrenme**: TensorFlow, Keras  
- **Veritabanı**: MySQL  
- **Model**: EfficientNetV2S (Transfer Learning)

---

## 🧬 Model Özellikleri

- Model: **EfficientNetV2S**
- Aktivasyon: `softmax` (çok sınıflı sınıflandırma için)
- Kayıp Fonksiyonu: `categorical_crossentropy`
- Optimizasyon: `Adam`
- Epoch: 50
- Batch Size: 32
- Eğitim Sonrası Başarı: **%98 doğruluk**

Model `.h5` formatında (`son_v3.h5`) eğitilmiş olup, doğrudan Flask uygulamasına entegre edilmiştir.

---

## 🗃️ Veri Seti

Projede kullanılan veri seti Kaggle'daki APTOS 2019 yarışmasından alınmıştır. Retina fundus görüntülerini içermektedir.

| Sınıf | Tanım               | Görüntü Sayısı |
|-------|---------------------|----------------|
| 0     | No DR               | 1805           |
| 1     | Mild                | 370            |
| 2     | Moderate            | 999            |
| 3     | Severe              | 193            |
| 4     | Proliferative DR    | 295            |
|       | **Toplam**          | **3662**       |

### 🔄 Veri Arttırma (Augmentation)

Veri dengesizliğini azaltmak ve overfitting’i engellemek için eğitim verileri üzerinde çeşitli görsel dönüşümler uygulanmıştır:

- Rastgele döndürme (rotate)
- Dikey/Yatay çevirme (flip)
- Yakınlaştırma/Uzaklaştırma (zoom)
- Konum kaydırma (shift)
- Renk/parlaklık değiştirme

> Bu sayede veri seti yaklaşık **15.000 görüntüye** çıkarılmıştır.

---

## 🛠️ Veri İşleme Adımları

- Görseller yeniden boyutlandırılmış ve merkezden kırpılmıştır.
- Histogram dengeleme (contrast enhancement) uygulanmıştır.
- RGB formatında normalize edilmiş tensörlere dönüştürülmüştür.
- Etiketler `categorical` forma çevrilmiştir (`to_categorical`).

---

## 🧾 Veritabanı Yapısı

SQLAlchemy ile modellenmiş ve MySQL üzerinde çalışan ilişkisel bir veritabanı kullanılmıştır. Veritabanında aşağıdaki ana tablolar yer alır:

- **Doktorlar**: Doktor bilgileri (ID, İsim, Uzmanlık)
- **Hastalar**: Hasta bilgileri (ID, İsim, Yaş, Cinsiyet)
- **Kayıtlar**: Teşhis tarihleri, yüklenen görüntüler, tahmin edilen sınıf, hasta ve doktor ID'leri ile ilişkilendirilmiştir.

---

## 🌐 Web Uygulaması Özellikleri

- **Kayıt ve Giriş**: Doktorlar sisteme kayıt olabilir ve oturum açabilir.
- **Hasta Takibi**: Doktorlar yeni hasta ekleyebilir, geçmiş verileri görüntüleyebilir.
- **Tahmin Sistemi**: Retina görüntüsü yüklendikten sonra model sınıf tahmini yapar.
- **Raporlama**: Kullanıcı geçmiş verilerini gözlemleyebilir.

---

## 📈 Model Performansı

Eğitim sürecinde `accuracy` ve `val_accuracy` eğrileri neredeyse paralel ilerlemiş, overfitting gözlenmemiştir. Confusion matrix analizleri ile sınıflar arası doğruluk da test edilmiştir.

> Eğitim ve test sonuçları için detaylı grafikler raporda yer almaktadır.

---

## 🧪 Model Eğitimi (Notebook)

Modelin eğitim sürecine dair tüm detaylara aşağıdaki Jupyter Notebook dosyasından ulaşabilirsiniz:

📔 [Model Eğitimi - V2S_SON_v2.ipynb](./notebooks/V2S_SON_v2.ipynb)

Bu dosyada:

- EfficientNetV2S mimarisi  
- Veri ön işleme ve augmentation  
- Eğitim ve validasyon süreci  
- Kayıp ve doğruluk grafiklerinin oluşturulması  
- `.h5` dosyasının (`son_v3.h5`) export edilmesi  
  adım adım belgelenmiştir.

---

## 📄 Teknik Rapor

Detaylı teknik açıklamalar, süreç analizi, model mimarisi ve sonuçların tamamı aşağıdaki PDF dosyasında sunulmuştur:

📄 [Bitirme Projesi Raporu (PDF)](./Bitirme_Projesi_Final_Rapor.pdf)

---

# 🧠 Diyabetik Retinopati Sınıflandırma Projesi

Bu proje, diyabet hastalığının ciddi bir komplikasyonu olan **diyabetik retinopati** hastalığını, retina görüntüleri üzerinden **derin öğrenme teknikleriyle sınıflandırmayı** amaçlamaktadır.

## 📌 Proje Hakkında

Diyabetik retinopati, retinadaki kan damarlarının hasar görmesiyle ortaya çıkan ve körlüğe kadar ilerleyebilen ciddi bir göz hastalığıdır. Bu projede, retina görüntülerinden hastalık seviyesini tespit eden bir yapay zeka modeli geliştirilmiş, bunun yanı sıra doktorların teşhis süreçlerini desteklemek için bir **web uygulaması** tasarlanmıştır.

Modelin doğruluk oranı yüksek (**%98**), web arayüzü kullanıcı dostu, veritabanı ise esnek ve ilişkisel yapıdadır. Proje sürecinde hem yazılım mühendisliği pratikleri hem de makine öğrenmesi teknikleri birlikte yürütülmüştür.

---

## 🧪 Kullanılan Teknolojiler

- **Backend**: Python, Flask, SQLAlchemy  
- **Frontend**: HTML, CSS, Bootstrap  
- **Görüntü işleme**: OpenCV, NumPy  
- **Makine öğrenimi / Derin öğrenme**: TensorFlow, Keras  
- **Veritabanı**: MySQL  
- **Model**: EfficientNetV2S (Transfer Learning)

---

## 🧬 Model Özellikleri

- Model: **EfficientNetV2S**
- Aktivasyon: `softmax` (çok sınıflı sınıflandırma için)
- Kayıp Fonksiyonu: `categorical_crossentropy`
- Optimizasyon: `Adam`
- Epoch: 50
- Batch Size: 32
- Eğitim Sonrası Başarı: **%98 doğruluk**

Model `.h5` formatında (`son_v3.h5`) eğitilmiş olup, doğrudan Flask uygulamasına entegre edilmiştir.

---

## 🗃️ Veri Seti

Projede kullanılan veri seti Kaggle'daki APTOS 2019 yarışmasından alınmıştır. Retina fundus görüntülerini içermektedir.

| Sınıf | Tanım               | Görüntü Sayısı |
|-------|---------------------|----------------|
| 0     | No DR               | 1805           |
| 1     | Mild                | 370            |
| 2     | Moderate            | 999            |
| 3     | Severe              | 193            |
| 4     | Proliferative DR    | 295            |
|       | **Toplam**          | **3662**       |

### 🔄 Veri Arttırma (Augmentation)

Veri dengesizliğini azaltmak ve overfitting’i engellemek için eğitim verileri üzerinde çeşitli görsel dönüşümler uygulanmıştır:

- Rastgele döndürme (rotate)
- Dikey/Yatay çevirme (flip)
- Yakınlaştırma/Uzaklaştırma (zoom)
- Konum kaydırma (shift)
- Renk/parlaklık değiştirme

> Bu sayede veri seti yaklaşık **15.000 görüntüye** çıkarılmıştır.

---

## 🛠️ Veri İşleme Adımları

- Görseller yeniden boyutlandırılmış ve merkezden kırpılmıştır.
- Histogram dengeleme (contrast enhancement) uygulanmıştır.
- RGB formatında normalize edilmiş tensörlere dönüştürülmüştür.
- Etiketler `categorical` forma çevrilmiştir (`to_categorical`).

---

## 🧾 Veritabanı Yapısı

SQLAlchemy ile modellenmiş ve MySQL üzerinde çalışan ilişkisel bir veritabanı kullanılmıştır. Veritabanında aşağıdaki ana tablolar yer alır:

- **Doktorlar**: Doktor bilgileri (ID, İsim, Uzmanlık)
- **Hastalar**: Hasta bilgileri (ID, İsim, Yaş, Cinsiyet)
- **Kayıtlar**: Teşhis tarihleri, yüklenen görüntüler, tahmin edilen sınıf, hasta ve doktor ID'leri ile ilişkilendirilmiştir.

---

## 🌐 Web Uygulaması Özellikleri

- **Kayıt ve Giriş**: Doktorlar sisteme kayıt olabilir ve oturum açabilir.
- **Hasta Takibi**: Doktorlar yeni hasta ekleyebilir, geçmiş verileri görüntüleyebilir.
- **Tahmin Sistemi**: Retina görüntüsü yüklendikten sonra model sınıf tahmini yapar.
- **Raporlama**: Kullanıcı geçmiş verilerini gözlemleyebilir.

---

## 📈 Model Performansı

Eğitim sürecinde `accuracy` ve `val_accuracy` eğrileri neredeyse paralel ilerlemiş, overfitting gözlenmemiştir. Confusion matrix analizleri ile sınıflar arası doğruluk da test edilmiştir.

> Eğitim ve test sonuçları için detaylı grafikler raporda yer almaktadır.

---

## 🧪 Model Eğitimi (Notebook)

Modelin eğitim sürecine dair tüm detaylara aşağıdaki Jupyter Notebook dosyasından ulaşabilirsiniz:

📔 [Model Eğitimi - V2S_SON_v2.ipynb](./notebooks/V2S_SON_v2.ipynb)

Bu dosyada:

- EfficientNetV2S mimarisi  
- Veri ön işleme ve augmentation  
- Eğitim ve validasyon süreci  
- Kayıp ve doğruluk grafiklerinin oluşturulması  
- `.h5` dosyasının (`son_v3.h5`) export edilmesi  
  adım adım belgelenmiştir.

---

## 📄 Teknik Rapor

Detaylı teknik açıklamalar, süreç analizi, model mimarisi ve sonuçların tamamı aşağıdaki PDF dosyasında sunulmuştur:

📄 [Bitirme Projesi Raporu (PDF)](./Bitirme_Projesi_Final_Rapor.pdf)

---

## 🚀 Kurulum ve Çalıştırma

Projenin yerel ortamda çalıştırılabilmesi için aşağıdaki adımları takip edebilirsiniz:

### 1. Repoyu Klonlayın
```bash
git clone https://github.com/kompaz/Diyabetik_Retinopati_Siniflandirma_Projesi.git
cd Diyabetik_Retinopati_Siniflandirma_Projesi
```

### 2. Sanal Ortam Oluşturun ve Aktif Edin
```bash
python -m venv myenv
myenv\Scripts\activate  # Linux/macOS için: source myenv/bin/activate
```

### 3. Gerekli Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Veritabanı Ayarlarını Yapın
`config.py` dosyasını açarak kendi veritabanı kullanıcı adı, şifre ve bağlantı bilgilerinizi girin.

### 5. Veritabanı Tablolarını Oluşturun
```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 6. Uygulamayı Başlatın
```bash
python app.py
```

### 7. Web Arayüzüne Erişin
Tarayıcınızda aşağıdaki bağlantıya gidin:
```
http://localhost:5000
```

> Not: Model ağırlık dosyası olan `son_v3.h5` dosyasının `models/` klasörü içinde bulunması gerekmektedir. Ayrıca Flask uygulaması bu dosyaya erişebilir olmalıdır.

