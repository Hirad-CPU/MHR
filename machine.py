# Import کتابخانه‌های مورد نیاز
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import dateparser
from datetime import datetime, timedelta

#متغیر ها
n=0
#تبدیل به تابع برای ایمپوت کردن
def machine(message):
    class result:
        def __init__(self,date):
            self.date=date
        def print_absent():
            print(1)



        # تعریف توابع مربوط به هر دستور
        def print_function(self):
            return("🖨 در حال پرینت گرفتن...")
        def absent(self):
            #لیست افراد غایب
            self.not_seven=list(set(self.seven_list)-set(self.pressent_seven))
            self.not_eight=list(set(self.eight_list)-set(self.pressent_eight))
            self.not_nine=list(set(self.nine_list)-set(self.pressent_nine))
            
            print(self.not_seven,self.not_eight,self.not_nine)

        def pressent(self):

            file_name = f"{self.date}.txt"
            # لیست داده‌هایی که می‌خواهید بررسی کنید
            self.seven_list=['هیراد',' Taha']
            self.eight_list=['Hirad','Matin']
            self.nine_list=['Hirad','Rastin']
        
            #لیست افراد حاضر
            self.pressent_seven=[]
            self.pressent_eight=[]
            self.pressent_nine=[]
            # نام فایل متنی

            # خواندن محتوای فایل و ذخیره به صورت یک مجموعه (set)
            with open(file_name, "r", encoding="utf-8") as file:
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
        "لطفا حاضرن پریروز رو بده",
        "حاضرین پریروز رو بنویس",
        "حاضرین امروز رو پرینت کن ",
        "پرینت کن حاضرین امروز رو",
        "پرینت حاضرین امروز ",
        "حاضرین دیروز رو پرینت کن ",
        "پرینت کن حاضرین دیروز رو ",
        "پرینت حاضرین دیروز ",
        "پرینت کن حاضرین پریروز رو ",
        "حاضرین پریروز رو پرینت کن",
        "پرینت حاضرین پریروز "
    ]
    labels = [0, 0, 0, 1, 1, 1, 2, 2, 2, 20, 20, 20, 21, 21, 21, 22, 22, 22] #مقددار دهی دستور ها

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
    #
    #برگذازی شرایط برای پرینتر
    if pred in [20, 21, 22]:
        pred-=20
        n=1
    
    #دیکشنری تبدیل عبارات نسبی تاریخ به تاریخ مطلق
    pred=int(pred)

    m={
        "n":datetime.now() - timedelta(days=pred)
    }


    # مقدار pred را بررسی و مقداردهی کنیم
    if isinstance(pred, (int, float)): 
        pred = int(pred) 
    else: 
        pred = 0  # مقدار پیش‌فرض در صورت نامعتبر بودن pred

    # دیکشنری تبدیل عبارات نسبی تاریخ به تاریخ مطلق
    m = {"n": datetime.now() - timedelta(days=pred)}

    # استفاده از دیکشنری و جداسازی داده مورد نیاز
    j = str(m["n"])
    
    date_only = j.split(' ')[0]
    

    if pred<=2:
        if n==1:
            return p.print_present()
        else:
            p=result(date_only)
            return p.pressent()
    elif pred<=5:
        if n==1:
            return p.print_absent()
        else:
            return p.absent()
        
