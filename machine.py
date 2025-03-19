# Import کتابخانه‌های مورد نیاز
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import dateparser
from datetime import datetime, timedelta
import httpp
import time
import threading
#متغیر ها
n=0
#تبدیل به تابع برای ایمپوت کردن
def machine(message):
    print(0)
    # خواندن محتوای فایل و ذخیره به صورت یک مجموعه برای بررسی درخواست ذخیره عکس
    with open("CHECK.txt", "r", encoding="utf-8") as file:
        file_data1 = set(file.read().splitlines())

    if "1" in file_data1:
        with open("CHECK.txt", "w", encoding="utf-8") as file:
            file.write(message + "\n")
            file.write("2\n")
        with open("CHECK.txt", "r", encoding="utf-8") as file:
            file_data1 = set(file.read().splitlines())
        print(file_data1)  # برای دیباگ، محتوای فایل را نمایش بده

        with open("CHECK.txt", "r", encoding="utf-8") as file:
            file_data1 = set(file.read().splitlines())
        return "لطفا کلاس دانش آموز را وارد کنید"

    elif "2" in file_data1:
        # اضافه کردن پیام به فایل
        with open("CHECK.txt", "a+", encoding="utf-8") as file:
            file.write(message + "\n")
        with open("CHECK.txt", "r", encoding="utf-8") as file:
            #انتفال دیتا دانش آموز جدید به لیست داده
            file_data2 = file.read().splitlines()
        #دادن مقدار به فایل دیتا مربوط به کلاس کاربر با توجه به درخواست
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

         
        # پاک کردن فایل بعد از 15 ثانیه
        time.sleep(15)
        with open("CHECK.txt", "w", encoding="utf-8") as file:
            file.write("")
        print(9)  # برای دیباگ


        return "عکس رو گرفتم فقط برای احتیاط, دانش آموز دو یا سه ثانیه جلو دوربین بایستد, ممنون"

    # خواندن محتوای فایل و ذخیره به صورت یک مجموعه برای بررسی درخواست پاک کردن داده ها
    with open("CHECK.txt", "r", encoding="utf-8") as file:
        file_data1 = set(file.read().splitlines())

    if "3" in file_data1:
        print(2)
        # پاک کردن محتوای فایل‌های مربوط به کلاس‌ها
        for filename in  ["seven.txt", "eight.txt", "nine.txt"]:
            with open(filename, "w", encoding="utf-8") as file:
                file.write("")
        # پاک کردن فایل بعد از 15 ثانیه
        time.sleep(10)
        with open("CHECK.txt", "w", encoding="utf-8") as file:
            file.write("")
        print(10)  # برای دیباگ
        return "اطلاعات کلاس های دخیره شدع پاک شد"


    else:
        class result:
            def __init__(self,date):
                self.date=date

                # نام فایل متنی
                self.file_name = f"{self.date}.txt"
                # لیست داده‌هایی که می‌خواهید بررسی کنید
                with open("seven.txt", "r",encoding='utf-8') as file:
                    self.seven_list= file.read().splitlines()
                with open("eight.txt","r",encoding="utf-8") as file:
                    self.eight_list=file.read().splitlines()
                with open("nine.txt","r",encoding="utf-8") as file:
                    self.nine_list=file.read().splitlines()
            
                #لیست افراد حاضر
                self.pressent_seven=[]
                self.pressent_eight=[]
                self.pressent_nine=[]
                
            def print_absent():
                print(1)



            # تعریف توابع مربوط به هر دستور
            def print_function(self):
                return("🖨 در حال پرینت گرفتن...")
            def absent(self):
                self.pressent(1)
                #لیست افراد غایب
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
                
            def pressent(self,number):
                print(self.file_name)
                # خواندن محتوای فایل و ذخیره به صورت یک مجموعه (set)
                with open(self.file_name, "r", encoding="utf-8") as file:
                    file_data = set(file.read().splitlines())  # خواندن خطوط و حذف تکراری‌ها
                for i, p in zip([self.seven_list, self.eight_list, self.nine_list], 
                            [self.pressent_seven, self.pressent_eight, self.pressent_nine]):
                    for name in i:
                        for line in file_data:
                            if name in line:  # ✅ به جای بررسی دقیق، بررسی کنیم که نام در متن وجود دارد
                                p.append(name)
                                break  # چون همین که یک بار نام پیدا شود کافی است، از حلقه خارج شوی
                
                        
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




        # ایجاد دیتاست نمونه برای آموزش مدل
        # در اینجا 0 نمایانگر دستور پرینت و 1 نمایانگر دستور غایب است
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
            "ذخیره عکس",
            "اضافه کردن عکس",
            "ثبت عکس",
            "پاک کن",
            "داده ها پاک",
            "پاک"
        ]
        labels = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 20, 20, 20, 21, 21, 21, 22, 22, 22, 31, 31, 31, 32, 32, 32] #مقددار دهی دستور ها

        # مرحله ۱: استخراج ویژگی‌های متنی با TF-IDF
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(commands)

        # مرحله ۲: آموزش مدل ماشین لرنینگ (Logistic Regression)
        clf = LogisticRegression()
        clf.fit(X, labels)


        # تبدیل ورودی کاربر به بردار ویژگی‌ها
        X_input = vectorizer.transform([message])
        
        n=0

        # پیش‌بینی دسته دستور
        pred = int(clf.predict(X_input)[0])
        print(f"ورودی: {message}, پیشبینی: {pred}")
        print(3)
    
        #برگذازی شرایط برای پرینتر
        if pred in [20, 21, 22, 23, 24, 25]:
            pred-=20
            n=1
        #پیدا کردن تاریخ مربوط به دستور غایبین
        f=pred    
        if 2<pred<20:
            f-=3
        #دیکشنری تبدیل عبارات نسبی تاریخ به تاریخ مطلق
        pred=int(pred)

        m={
            "n":datetime.now() - timedelta(days=f)
        }


        # مقدار pred را بررسی و مقداردهی کنیم
        if isinstance(pred, (int, float)): 
            pred = int(pred) 
        else: 
            pred = 0  # مقدار پیش‌فرض در صورت نامعتبر بودن pred

        # استفاده از دیکشنری و جداسازی داده مورد نیاز
        j = str(m["n"])
        
        date_only = j.split(' ')[0]
        
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
        
            
