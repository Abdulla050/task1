from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# MySQL ilə əlaqə yaradın
db = pymysql.connect(
    host="localhost",  # MySQL server ünvanı
    user="root",  # MySQL istifadəçi adı
    password="12345",  # MySQL istifadəçi şifrəsi
    db="root"  # İstifadə edilən cədvəl
)

# Ana səhifədə məlumatları çıxarmaq
@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    per_page = 5  # Səhifədə görünəcək məlumatların sayı

    # Məlumatları çıxarmaq üçün SQL əmri
    start = (page - 1) * per_page
    cur = db.cursor()
    cur.execute("SELECT * FROM blogs LIMIT %s OFFSET %s", (per_page, start))
    blogs = cur.fetchall()
    cur.close()

    # Pagination üçün digər hesablamar
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM blogs")
    total_blogs = cur.fetchone()[0]
    cur.close()
    total_pages = (total_blogs + per_page - 1) // per_page

    return render_template('index.html', blogs=blogs, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
