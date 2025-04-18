 # ایمپورت کتابخانه‌های مورد نیاز برای پردازش متن، مدل یادگیری ماشین، زمان و اجرای سرور
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import dateparser
from datetime import datetime, timedelta
import httpp
import time
import threading

# تعریف متغیر عمومی
n=0

# تبدیل کل عملیات به تابع برای دریافت پیام به‌عنوان ورودی
def machine(message):
    print(0)

    # خواندن محتوای فایل و بررسی اینکه آیا در وضعیت "ذخیره عکس" هست یا نه
    with open("CHECK.txt", "r", encoding="utf-8") as file:
        file_data1 = set(file.read().splitlines())

    # اگر وضعیت ذخیره عکس فعال باشد
    if "1" in file_data1:
        with open("CHECK.txt", "w", encoding="utf-8") as file:
            file.write(message + "\n")
            file.write("2\n")
        with open("CHECK.txt", "r", encoding="utf-8") as file:
            file_data1 = set(file.read().splitlines())
        print(file_data1)  # چاپ وضعیت فعلی برای دیباگ

        with open("CHECK.txt", "r", encoding="utf-8") as file:
            file_data1 = set(file.read().splitlines())
        return "لطفا کلاس دانش آموز را وارد کنید"

    # مرحله دوم ذخیره‌سازی (پس از دریافت نام و کلاس دانش‌آموز)
    elif "2" in file_data1:
        # اضافه کردن پیام جدید به فایل
        with open("CHECK.txt", "a+", encoding="utf-8") as file:
            file.write(message + "\n")
        with open("CHECK.txt", "r", encoding="utf-8") as file:
            # انتقال داده به لیست
            file_data2 = file.read().splitlines()
        # بر اساس کلاس، ذخیره در فایل مرتبط
        print(file_data2)
        if "هفتم" in file_data2:
            print(990)
            with open("seven.txt","a",encoding="utf-8") as file:
                file.write(file_data2[0]+"\n")
        elif "هشتم" in file_data2:
            with open("eight.txt","a",encoding="utf-8") as file:
                file.write(file_data2[0]+"\n")
        elif "نهم" in file_data2:
            with open("nine.txt","a",encoding="utf-8") as file:
                file.write(file_data2[0]+"\n")

        # اجرای سرور در یک ترد جداگانه
        threading.Thread(target=httpp.httpp, daemon=True).start()

        # پاکسازی فایل وضعیت بعد از ۱۵ ثانیه
        time.sleep(15)
        with open("CHECK.txt", "w", encoding="utf-8") as file:
            file.write("")
        print(9)  # چاپ پیام دیباگ

        return "عکس رو گرفتم فقط برای احتیاط, دانش آموز دو یا سه ثانیه جلو دوربین بایستد, ممنون"

    # بررسی درخواست پاک‌سازی تمام اطلاعات
    with open("CHECK.txt", "r", encoding="utf-8") as file:
        file_data1 = set(file.read().splitlines())

    if "3" in file_data1:
        print(2)
        # پاک کردن اطلاعات تمام کلاس‌ها
        for filename in  ["seven.txt", "eight.txt", "nine.txt"]:
            with open(filename, "w", encoding="utf-8") as file:
                file.write("")
        # پاک کردن وضعیت پس از ۱۰ ثانیه
        time.sleep(10)
        with open("CHECK.txt", "w", encoding="utf-8") as file:
            file.write("")
        print(10)  # دیباگ
        return "اطلاعات کلاس های دخیره شدع پاک شد"

    # بررسی درخواست پاک‌سازی یک نفر خاص
    with open("CHECK.txt", "r", encoding="utf-8") as file:
        file_data1 = set(file.read().splitlines())
        
    if "4" in file_data1:
        with open("CHECK.txt", "w", encoding="utf-8") as file:
            file.write(message + "\n")
            print(message)        
            file.write("5\n")
        with open("CHECK.txt", "r", encoding="utf-8") as file:
            file_data1 = set(file.read().splitlines())
        print(file_data1)  # دیباگ

        with open("CHECK.txt", "r", encoding="utf-8") as file:
            file_data1 = set(file.read().splitlines())
        return "لطفا کلاس دانش آموز را وارد کنید"

    # مرحله دوم حذف فرد خاص پس از دریافت کلاس
    elif "5" in file_data1:
        # اضافه کردن پیام جدید به فایل
        with open("CHECK.txt", "a+", encoding="utf-8") as file:
            file.write(message + "\n")
        with open("CHECK.txt", "r", encoding="utf-8") as file:
            file_data2 = file.read().splitlines()
        print(file_data2)

        # حذف فرد از فایل کلاس مربوطه
        if "هفتم" in file_data2:
            print(990)
            with open("seven.txt","r",encoding="utf-8") as file:
                lines = file.readlines()
            with open("seven.txt","w",encoding="utf-8") as file:
                for line in lines:
                    if line.strip() != file_data2[0]:
                        file.write(line)
        elif "هشتم" in file_data2:
            with open("eight.txt","r",encoding="utf-8") as file:
                lines = file.readlines()
            with open("eight.txt","w",encoding="utf-8") as file:
                for line in lines:
                    if line.strip() != file_data2[0]:
                        file.write(line)
        elif "نهم" in file_data2:
            with open("nine.txt","r",encoding="utf-8") as file:
                lines = file.readlines()
            with open("nine.txt","w",encoding="utf-8") as file:
                for line in lines:
                    if line.strip() != file_data2[0]:
                        file.write(line)

        # اجرای سرور در یک ترد جدا
        threading.Thread(target=httpp.httpp, daemon=True).start()
        
        # پاکسازی فایل وضعیت بعد از ۱۵ ثانیه
        time.sleep(15)
        with open("CHECK.txt", "w", encoding="utf-8") as file:
            file.write("")
        return "فرد مورد نظر پاک شد"

    else:
        # تعریف کلاس مدیریت وضعیت حضور و غیاب
        class result:
            def __init__(self,date):
                self.date=date

                # نام فایل مربوط به تاریخ خاص
                self.file_name = f"{self.date}.txt"

                # خواندن لیست اسامی دانش‌آموزان هر کلاس
                with open("seven.txt", "r",encoding='utf-8') as file:
                    self.seven_list= file.read().splitlines()
                with open("eight.txt","r",encoding="utf-8") as file:
                    self.eight_list=file.read().splitlines()
                with open("nine.txt","r",encoding="utf-8") as file:
                    self.nine_list=file.read().splitlines()
            
                # تعریف لیست افراد حاضر در هر کلاس
                self.pressent_seven=[]
                self.pressent_eight=[]
                self.pressent_nine=[]
                
            def print_absent():
                print(1)

            # تابع چاپ برای دستور پرینت
            def print_function(self):
                return("🖨 در حال پرینت گرفتن...")

            # تابع نمایش لیست غایبین
            def absent(self):
                self.pressent(1)
                self.not_seven=list(set(self.seven_list)-set(self.pressent_seven))
                self.not_eight=list(set(self.eight_list)-set(self.pressent_eight))
                self.not_nine=list(set(self.nine_list)-set(self.pressent_nine))

                self.result_not = (
                    "کلاس هفتم:"
                    f"{', '.join(self.not_seven)}\n"
                    "کلاس هشتم:"
                    f"{', '.join(self.not_eight)}\n"
                    "کلاس نهم:"
                    f"{', '.join(self.not_nine)}"
                )
                
                print(self.not_seven,self.not_eight,self.not_nine)
                return self.result_not
                
            # تابع بررسی و ثبت حضور دانش‌آموزان
            def pressent(self,number):
                print(self.file_name)
                with open(self.file_name, "r", encoding="utf-8") as file:
                    file_data = set(file.read().splitlines())

                for i, p in zip([self.seven_list, self.eight_list, self.nine_list], 
                                [self.pressent_seven, self.pressent_eight, self.pressent_nine]):
                    for name in i:
                        for line in file_data:
                            if name in line:
                                p.append(name)
                                break

                self.result_present = (
                    "کلاس هفتم:"
                    f"{', '.join(self.pressent_seven)}\n"
                    "کلاس هشتم:"
                    f"{', '.join(self.pressent_eight)}\n"
                    "کلاس نهم:"
                    f"{', '.join(self.pressent_nine)}"
                )
                
                if number==0:
                    print(self.result_present)
                    return self.result_present

        # تعریف دستورات و برچسب‌گذاری آنها برای آموزش مدل
        commands = [
            "حاضرین امروز",
            "لطفا حاضرین امروز روبده",
            "حاضرین امروز رو بنویس",
            "حاضرین دیروز",
            "لطفا حاضرین دیروز رو بده",
            "حاضرین دیروز رو بنویس",
            "حاضرین پریروز",
            "لطفا حاضرین پریروز رو بده",
            "حاضرین پریروز رو بنویس",
            "غایبین امروز",
            "لطفا غایبین امروز رو بده",
            "غایبین امروز رو بنویس",
            "غایبین دیروز",
            "لطفا غایبین دیروز رو بده",
            "غایبین دیروز رو بنویس",
            "غایبین پریروز",
            "لطفا غایبین پریروز رو بده",
            "غایبین پریروز رو بنویس",
            "حاضرین امروز رو پرینت کن ",
            "پرینت کن حاضرین امروز رو",
            "پرینت حاضرین امروز ",
            "حاضرین دیروز رو پرینت کن ",
            "پرینت کن حاضرین دیروز رو ",
            "پرینت حاضرین دیروز ",
            "پرینت کن حاضرین پریروز رو ",
            "حاضرین پریروز رو پرینت کن",
            "پرینت حاضرین پریروز ",
            "پرینت کن غایبین امروز رو",
            "غایبین امروز رو پرینت کن",
            "پرینت غایبین امروز",
            "پرینت کن غایبین دیروز رو",
            "غایبین دیروز رو پرینت کن",
            "پرینت غایبین دیروز",
            "پرینت کن غایبین پریروز رو",
            "غایبین پریروز رو پرینت کن",
            "پرینت غایبین پریروز",
            "ذخیره عکس",
            "اضافه کردن عکس",
            "ثبت عکس",
            "همه رو پاک کن",
            "داده ها رو پاک",
            "پاک",
            "یدونه رو پاک کن",
            "یک نفر رو پاک کن",
            "پاک یه نفر"
        ]
        labels = [0,0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,20,20,20,21,21,21,22,22,22,23,23,23,24,24,24,25,25,25,31,31,31,32,32,32,33,33,33]

        # تبدیل متون به ویژگی‌های عددی با TF-IDF
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(commands)

        # آموزش مدل طبقه‌بندی لجستیک رگرسیون
        clf = LogisticRegression()
        clf.fit(X, labels)

        # پیش‌پردازش ورودی کاربر
        X_input = vectorizer.transform([message])
        n=0

        # پیش‌بینی دستور داده‌شده
        pred = int(clf.predict(X_input)[0])
        print(f"ورودی: {message}, پیشبینی: {pred}")
        print(3)

        # بررسی آیا پرینت نیاز است یا نه
        if pred in [20, 21, 22, 23, 24, 25]:
            pred-=20
            n=1

        # محاسبه روز برای عبارت "دیروز" و "پریروز"
        f=pred    
        if 2<pred<20:
            f-=3

        # تبدیل روز نسبی به تاریخ دقیق
        pred=int(pred)
        m={
            "n":datetime.now() - timedelta(days=f)
        }

        # اطمینان از اینکه مقدار pred معتبر است
        if isinstance(pred, (int, float)): 
            pred = int(pred) 
        else: 
            pred = 0

        # استخراج فقط تاریخ از شیء datetime
        j = str(m["n"])
        date_only = j.split(' ')[0]

        # ساخت آبجکت result برای دریافت حضور یا غیاب
        p=result(date_only)

        if pred<=2:
            if n==1:
                return p.print_present()
            else:
                return p.pressent(0)
        elif pred<=5:
            if n==1:
                return p.print_absent()
            else:
                return p.absent()
        elif pred==31:
            with open("CHECK.txt",'a') as file:
                file.write("1")
            return "لطفا نام کاربر رو وارد کن"
        elif pred==32:
            with open("CHECK.txt",'a') as file:
                file.write("3")
                print(4)
        elif pred==33:
            with open("CHECK.txt","a") as file:
                file.write("4")
            with open("CHECK.txt", "r", encoding="utf-8") as file:
                file_data1 = set(file.read().splitlines())
                return "لطفا نام کاربر حذفی رو وارد کن"
