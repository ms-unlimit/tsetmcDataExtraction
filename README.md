# استخراج و ذخیره خودکار داده‌های سهام بورس ایران


این پروژه به کمک کتابخانه finpy_tse اطلاعات قیمتی و معالات حقیق و حقوقی سهام را به طور روزانه جمع آوری کرده و در پایگاه داده mongo ذخیره می کند.
<!-- Table of Contents -->
# فهرست مطالب
- [ راهنمای نصب](#نصب-و-راه‌اندازی)
- [ اجرای پروژه](#اجرای پروژه)

<!-- /Table of Contents -->

# راهنمای نصب
این راهنما شامل مراحل نصب و راه‌اندازی پروژه با استفاده از Docker و Python 3.10 است.

### نصب Docker
ابتدا داکر را از [سایت رسمی داکر](https://www.docker.com/) دانلود و نصب کنید. 

### اجرای Docker برای MongoDB

استفاده از Docker Compose برای اجرای MongoDB:

1. ایجاد یک فایل به نام `docker-compose.yml` و محتوای زیر را در آن قرار دهید:

    ```yaml
    version: '3'
    services:
      mongo:
        image: mongo
        ports:
          - "27017:27017"
    ```
   
2. در ترمینال، به مسیر حاوی فایل `docker-compose.yml` بروید و دستور زیر را اجرا کنید:
   اجرای داکر مونگو از mongodb/MongoDockerFile

    ```bash
    docker-compose up -d
    ```

3. MongoDB حالا اجرا شده و بر روی پورت 27017 در دسترس است.

### نصب Python 3.10

پروژه از Python 3.10 استفاده می‌کند. شما می‌توانید این نسخه را از [وب‌سایت Python](https://www.python.org/downloads/) دانلود و نصب کنید.

### نصب پکیج‌ها از #requirements.txt

1. در ترمینال، به مسیر پروژه بروید که فایل `requirements.txt` در آن قرار دارد.

2. دستور زیر را اجرا کنید تا پکیج‌های مورد نیاز از فایل `requirements.txt` نصب شوند:

    ```bash
    pip install -r requirements.txt
    ```

## اجرای پروژ

حالا که Docker اجرا شده، Python 3.10 نصب شده و پکیج‌های مورد نیاز نصب شده‌اند، می‌توانید پروژه را اجرا کنید.

```bash
python main.py
