from flask import Flask, render_template, request, redirect, url_for, g, session, jsonify
import mysql.connector
import os
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
from werkzeug.utils import secure_filename
from flask_session import Session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Güçlü bir gizli anahtar belirleyin
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model_path = 'son_v3.h5'
model = None

# MySQL veritabanı ayarları
DATABASE_CONFIG = {
    'user': 'your_username',  # MySQL kullanıcı adınızı buraya girin
    'password': 'your_password',  # MySQL şifrenizi buraya girin
    'host': 'localhost',
    'database': 'bitirmeproje',
    'port': 3306,
    'raise_on_warnings': True
}

# Modeli yüklemeye çalış
try:
    model = load_model(model_path)
    print("Model başarıyla yüklendi.")
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {e}")

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**DATABASE_CONFIG)
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        with open('db.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
            sql_commands = sql_script.split(';')
            for command in sql_commands:
                if command.strip():  # Boş komutları atla
                    cursor.execute(command)
                    db.commit()
        cursor.close()

# Veritabanını oluştur
if not os.path.exists('database_initialized'):
    init_db()
    with open('database_initialized', 'w') as f:
        f.write('Database initialized.')

@app.route('/hasta_ara', methods=['POST'])
def hasta_ara():
    tcno = request.form.get('tcno')
    cursor = get_db().cursor(dictionary=True)
    cursor.execute("SELECT * FROM hasta WHERE tc = %s", (tcno,))
    hasta = cursor.fetchone()
    if hasta:
        cursor.execute("SELECT hastalik_derecesi FROM kayit WHERE hasta_tc = %s ORDER BY tarih DESC LIMIT 1", (tcno,))
        kayit = cursor.fetchone()
        if kayit:
            hasta['hastalik_derecesi'] = kayit['hastalik_derecesi']
        else:
            hasta['hastalik_derecesi'] = 'Daha önce bir analiz yapılmamış.'
    cursor.close()
    if hasta:
        return jsonify(hasta), 200
    else:
        return jsonify({'error': 'Hasta bulunamadı'}), 404

@app.route('/hasta_ve_doktor_islemleri', methods=['GET', 'POST'])
def hasta_ve_doktor_islemleri():
    if request.method == 'POST':
        button_type = request.form['button_type']
        if button_type == 'hasta':
            return redirect(url_for('hasta_islemleri'))
        elif button_type == 'doktor':
            return redirect(url_for('doktor_islemleri'))
    return render_template('islemler.html')

@app.route('/hasta_ekle', methods=['GET', 'POST'])
def hasta_ekle():
    if request.method == 'POST':
        tc = request.form.get('tc')
        ad = request.form.get('ad')
        soyad = request.form.get('soyad')
        dogum_tarihi = request.form.get('dogum_tarihi')
        cinsiyet = request.form.get('cinsiyet')
        iletisim_bilgisi = request.form.get('iletisim_bilgisi')

        if not tc or not ad or not soyad:
            return jsonify({'error': "TC Kimlik Numarası, Ad ve Soyad alanları zorunludur"}), 400

        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM hasta WHERE tc = %s", (tc,))
        existing_hasta = cursor.fetchone()

        if existing_hasta:
            return jsonify({'error': "Bu TC kimlik numarasıyla kayıtlı bir hasta zaten mevcut"}), 400

        cursor.execute(
            "INSERT INTO hasta (tc, ad, soyad, dogum_tarihi, cinsiyet, iletisim_bilgisi) VALUES (%s, %s, %s, %s, %s, %s)", 
            (tc, ad, soyad, dogum_tarihi, cinsiyet, iletisim_bilgisi)
        )
        get_db().commit()
        cursor.close()
        return jsonify({'success': "Hasta başarıyla eklendi"}), 200

    return render_template('hasta_ekle.html')

@app.route('/hasta_islemleri', methods=['GET', 'POST'])
def hasta_islemleri():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return 'Dosya seçilmedi', 400

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            image = preprocess_image(filepath, (224, 224))
            if model:
                predictions = model.predict(image)
                predicted_class_index = np.argmax(predictions[0])
                classes = ['Class_Mild', 'Class_Moderate', 'Class_No_DR', 'Class_Proliferate_DR', 'Class_Severe']
                result = classes[predicted_class_index]
                
                # Doktor ve hasta bilgilerini kaydet
                doktor_tc = session.get('doctor_tc')
                hasta_tc = request.form.get('tcno')
                tarih = datetime.now().strftime('%Y-%m-%d')
                hastalik_derecesi = result

                cursor = get_db().cursor()
                cursor.execute(
                    "INSERT INTO kayit (doktor_tc, hasta_tc, tarih, hastalik_derecesi, retina_gorsel) VALUES (%s, %s, %s, %s, %s)", 
                    (doktor_tc, hasta_tc, tarih, hastalik_derecesi, filepath)
                )
                get_db().commit()
                cursor.close()

                return render_template('result.html', result=result)
            else:
                return 'Model yüklenemedi', 500
    return render_template('hasta_islemleri.html')

@app.route('/doktor_islemleri', methods=['GET', 'POST'])
def doktor_islemleri():
    if 'doctor_tc' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'ekle' in request.form:
            return redirect(url_for('doktor_ekle'))
        else:
            tc = request.form.get('tc')
            ad = request.form.get('ad')
            soyad = request.form.get('soyad')
            sifre = request.form.get('sifre')
            uzmanlik_alan = request.form.get('uzmanlik_alan')
            iletisim_bilgisi = request.form.get('iletisim_bilgisi')

            cursor = get_db().cursor()
            cursor.execute("UPDATE doktor SET ad = %s, soyad = %s, sifre = %s, uzmanlik_alan = %s, iletisim_bilgisi = %s WHERE tc = %s", 
                           (ad, soyad, sifre, uzmanlik_alan, iletisim_bilgisi, tc))
            get_db().commit()
            cursor.close()
            return "success"

    # Giriş yapan doktorun bilgilerini al
    cursor = get_db().cursor(dictionary=True)
    cursor.execute("SELECT * FROM doktor WHERE tc = %s", (session['doctor_tc'],))
    doktor = cursor.fetchone()
    cursor.close()

    return render_template('doktor_islemleri.html', doktor=doktor)


@app.route('/doktor_ekle', methods=['GET', 'POST'])
def doktor_ekle():
    if request.method == 'POST':
        tc = request.form.get('tc')
        ad = request.form.get('ad')
        soyad = request.form.get('soyad')
        sifre = request.form.get('sifre')
        uzmanlik_alan = request.form.get('uzmanlik_alan')
        iletisim_bilgisi = request.form.get('iletisim_bilgisi')

        # Form alanlarının dolu olup olmadığını kontrol et
        if not tc or not ad or not soyad:
            return jsonify({'error': "TC Kimlik Numarası, Ad ve Soyad alanları zorunludur"}), 400

        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM doktor WHERE tc = %s", (tc,))
        existing_doktor = cursor.fetchone()

        if existing_doktor:
            return jsonify({'error': "Bu TC kimlik numarasıyla kayıtlı bir doktor zaten mevcut"}), 400

        cursor.execute(
            "INSERT INTO doktor (tc, ad, soyad, sifre, uzmanlik_alan, iletisim_bilgisi) VALUES (%s, %s, %s, %s, %s, %s)", 
            (tc, ad, soyad, sifre, uzmanlik_alan, iletisim_bilgisi)
        )
        get_db().commit()
        cursor.close()
        return jsonify({'success': "Doktor başarıyla eklendi"}), 200
    
    # GET isteğinde formu göster
    return render_template('doktor_ekle.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tc = request.form.get('tc')
        password = request.form.get('password')
        cursor = get_db().cursor(dictionary=True)
        cursor.execute("SELECT * FROM doktor WHERE tc = %s AND sifre = %s", (tc, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['doctor_tc'] = user['tc']  # Oturumda doktorun TC'sini sakla
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Geçersiz kullanıcı adı veya şifre'}), 401
    return render_template('login.html')

def preprocess_image(image_path, target_size):
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image_array = np.asarray(image)
    image_array = image_array.astype(np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
