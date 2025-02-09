# Import کتابخانه‌های مورد نیاز
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import dateparser
from datetime import datetime, timedelta
#تبدیل به تابع برای ایمپوت کردن
def machine(message):
    class result:
        def __init__(self,date):
            self.date=date



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
            self.seven_list=['hirad','taha']
            self.eight_list=['ali','matin']
            self.nine_list=['reza','rastin']
        
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
                for n in i:
                    if n in file_data:
                        print(2)
                        p.append(n)
                        
            
                    
            self.result_present = (
                "کلاس هفتم:"
                f"{', '.join(self.pressent_seven)}"
                "کلاس هشتم:"
                f"{', '.join(self.pressent_eight)}"
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
    ]
    labels = [0, 0, 0, 1, 1, 1, 2, 2, 2] #مقددار دهی دستور ها

    # مرحله ۱: استخراج ویژگی‌های متنی با TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(commands)

    # مرحله ۲: آموزش مدل ماشین لرنینگ (Logistic Regression)
    clf = LogisticRegression()
    clf.fit(X, labels)


    # تبدیل ورودی کاربر به بردار ویژگی‌ها
    X_input = vectorizer.transform([message])

    # پیش‌بینی دسته دستور
    pred = clf.predict(X_input)[0]

    print(pred)
    #تبدیل عبارات نسبی تاریخ به تاریخ مطلق
    pred=int(pred)
    m={
        "n":datetime.now() - timedelta(days=pred)
    }
    



    j=str(m["n"])
    print(j)
    date_only=j.split(' ')[0]
    print(date_only)

    if pred<=2:
        p=result(date_only)
        return p.pressent
