import os
import shutil
from docx import Document
import PyPDF2

# Region mapping
regions = {
    "north": [
        "Acre", "עכו", "Afula", "עפולה", "Arraba", "ערבה", "Bet She'an", "בית שאן", 
        "Karmiel", "כרמיאל", "Kiryat Shmona", "קריית שמונה", "Ma'alot-Tarshiha", "מעלות-תרשיחא", 
        "Maghar", "מגאר", "Migdal HaEmek", "מגדל העמק", "Nahariyya", "נהריה", "Nazareth", "נצרת", 
        "Nof HaGalil", "נוף הגליל", "Safed", "צפת", "Sakhnin", "סכנין", "Shefa-'Amr", "שפרעם", 
        "Tamra", "טמרה", "Tiberias", "טבריה", "Yokneam", "יוקנעם", "Abu Sinan", "אבו סינאן", 
        "Basmat Tab'un", "בסמת טבעון", "Beit Jann", "בית ג'ן", "Bi'ina", "בענה", "Bir al-Maksur", "ביר אל-מכסור", 
        "Bu'eine Nujeidat", "בועיינה נוג'ידאת", "Buq'ata", "בוקעתא", "Daburiyya", "דבוריה", 
        "Deir al-Asad", "דייר אל-אסד", "Deir Hanna", "דייר חנא", "Eilabun", "עילבון", "Ein Qiniyye", "עין קנייה", 
        "Ein Mahil", "עין מאהל", "Fassuta", "פסוטה", "Ghajar", "ג'וחר", "Hazor HaGelilit", "חצור הגלילית", 
        "Hurfeish", "חורפיש", "I'billin", "עיבלין", "Iksal", "עכסאל", "Ilut", "עילוט", "Jadeidi-Makr", "ג'דיידה-מכר", 
        "Jish", "ג'יש", "Julis", "ג'וליס", "Ka'abiyye-Tabbash-Hajajre", "כאביה-תבאש-חג'אג'רה", 
        "Kabul", "כאבול", "Kafr Kanna", "כפר כנא", "Kafr Manda", "כפר מנדא", "Kafr Yasif", "כפר יסיף", 
        "Kaukab Abu al-Hija", "כוכב אבו אל-היג'ה", "Katzrin", "קצרין", "Kfar Kama", "כפר כאמה", "Kfar Tavor", "כפר תבור", 
        "Kfar Vradim", "כפר ורדים", "Kisra-Sumei", "כסרא-סומיע", "Majd al-Krum", "מג'דל כרום", "Majdal Shams", "מג'דל שמס", 
        "Mas'ada", "מסעדה", "Mashhad", "משהד", "Mazra'a", "מזרעה", "Metula", "מטולה", "Migdal", "מגדל", 
        "Mi'ilya", "מיליה", "Nahf", "נחף", "Peki'in", "פקיעין", "Ramat Yishai", "רמת ישי", "Rameh", "רמאה", 
        "Reineh", "רינה", "Rosh Pinna", "ראש פינה", "Sajur", "סאג'ור", "Sha'ab", "שיעב", 
        "Shibli-Umm al-Ghanam", "שבלי-אום אל-גאנם", "Shlomi", "שלומי", "Tuba-Zangariyye", "טובה-זנגריה", 
        "Tur'an", "תורעאן", "Yafa an-Naseriyye", "יאפה-אנה-נאסריה", "Yanuh-Jat", "יאנוח-ג'ת", 
        "Yavne'el", "יבנאל", "Yesod HaMa'ala", "יסוד המעלה", "Yirka", "ירכא", "Zarzir", "זרזיר", 
        "al-Batuf", "אל בטוף", "Bustan al-Marj", "בוסתן אל-מרג'", "Emek HaYarden", "עמק הירדן", 
        "Gilboa", "גלבוע", "Golan", "גולן", "Jezreel Valley", "עמק יזרעאל", "Lower Galilee", "הגליל התחתון", 
        "Ma'ale Yosef", "מעלה יוסף", "Matte Asher", "מטה אשר", "Megiddo", "מגידו", "Merom HaGalil", "מרום הגליל", 
        "Mevo'ot HaHermon", "מבואות החרמון", "Misgav", "משגב", "Upper Galilee", "הגליל העליון", "Valley of Springs", "בקעת בית שאן"
    ],
    "jerusalem" : [
        "Beit Shemesh", "בית שמש", "Jerusalem", "ירושלים", "Abu Ghosh", "אבו גוש", "Kiryat Ye'arim", "קריית יערים", 
        "Mevaseret Zion", "מבשרת ציון", "Mateh Yehuda", "מטה יהודה"
    ],
    "haifa" : [
        "Baqa al-Gharbiyye", "בקעה אל-גרביה", "Hadera", "חדרה", "Haifa", "חיפה", "Harish", "חריש", 
        "Kiryat Ata", "קריית אתא", "Kiryat Bialik", "קריית ביאליק", "Kiryat Motzkin", "קריית מוצקין", 
        "Kiryat Yam", "קריית ים", "Nesher", "נשר", "Or Akiva", "אור עקיבא", "Tirat Carmel", "טירת כרמל", 
        "Umm al-Fahm", "אום אל-פחם", "Ar'ara", "ערערה", "Basma", "בסמה", "Binyamina", "בנימינה", 
        "Daliyat al-karmel", "דלית אל-כרמל", "Fureidis", "פריידס", "Isfiya", "עוספיה", "Jatt", "ג'ת", 
        "Jisr az-Zarqa", "ג'סר אל-זרקא", "Kafr Qara", "כפר קארה", "Kiryat Tivon", "קריית טבעון", 
        "Ma'ale Iron", "מעלה עיון", "Pardes Hanna-Karkur", "פרדס חנה-כרכור", "Rekhasim", "רכסים", 
        "Zikhron Ya'akov", "זכרון יעקב", "Alona", "אלונה", "Hof HaCarmel", "חוף הכרמל", "Menashe", "מנשה", 
        "Zevulun", "זבולון"
    ],
    "central" : [
        "Be'er Ya'akov", "באר יעקב", "El'ad", "אלעד", "Ganei Tikva", "גני תקווה", "Giv'at Shmuel", "גבעת שמואל", 
        "Hod Hasharon", "הוד השרון", "Kafr Qasim", "כפר קאסם", "Kfar Saba", "כפר סבא","kfar shmaryahu", "כפר שמריהו", "Kfar Yona", "כפר יונה", 
        "Lod", "לוד", "Modi'in-Maccabim-Re'ut", "מודיעין-מכבים-רעות", "Ness Ziona", "נס ציונה", "Netanya", "נתניה", 
        "Petah Tikva", "פתח תקווה", "Qalansawe", "קאלנסווה", "Ra'anana", "רעננה", "Ramla", "רמלה", 
        "Rehovot", "רחובות", "Rishon LeZion", "ראשון לציון", "Rosh HaAyin", "ראש העין", "Tayibe", "טייבה", 
        "Tira", "טירה", "Yavne", "יבנה", "Yehud-Monosson", "יהוד-מונוסון", "Beit Dagan", "בית דגן", 
        "Bnei Ayish", "בני עייש", "Elyakhin", "אליחין", "Even Yehuda", "אבן יהודה", "Gan Yavne", "גן יבנה", 
        "Gedera", "גדרה", "Jaljulia", "ג'לג'וליה", "Kadima-Tzoran", "קדימה-צורן", "Kfar Bara", "כפר ברא", 
        "Kiryat Ekron", "קריית עקרון", "Kokhav Yair", "כוכב יאיר", "Mazkeret Batya", "מזכרת בתיה", "Pardesiya", "פרדסיה", 
        "Savyon", "סביון", "Shoham", "שוהם", "Tel Mond", "תל מונד", "Zemer", "זמר", "Brenner", "ברנר", 
        "Drom HaSharon", "דרום השרון", "Gan Rave", "גן רווה", "Gederot", "גדרות", "Gezer", "גזר", 
        "Hefer Valley (Emek Hefer)", "עמק חפר", "Hevel Modi'in", "הבל מודיעין", "Hevel Yavne", "הבל יבנה", 
        "Hof HaSharon", "חוף השרון", "Lev HaSharon", "לב השרון", "Nahal Sorek", "נחל שורק", "Sdot Dan", "סדנאים"
    ],
    "south": [
        "Arad", "ערד", "Beersheba", "באר שבע", "Eilat", "אילת", "Dimona", "דימונה", 
        "Hura", "חורה", "Mitzpe Ramon", "מצפה רמון", "Ofakim", "אופקים", "Omer", "עומר", 
        "Rahat", "רהט", "Sderot", "שדרות", "Tel Sheva", "תל שבע", "Yeruham", "ירוחם", 
        "Kuseife", "כיסייפה", "Meitar", "מיתר", "Mitzpe Hila", "מצפה הילה", "Nitzana", "נצנה", 
        "Shuva", "שובה", "Tamar", "תמר", "Tse'elim", "צאלים", "Zikim", "זיקים", "Ashalim", "אשלים",
        "Yated", "יתד"
    ],
    "tel aviv": [
        "Bat Yam", "בת ים", "Givatayim", "גבעתיים", "Holon", "חולון", "Lod", "לוד", "Rishon LeZion", 
        "ראשון לציון", "Tel Aviv", "תל אביב", "Herzliya", "הרצליה", "Petah Tikva", "פתח תקווה", 
        "Ramat Gan", "רמת גן", "Rehovot", "רחובות", "Kiryat Ono", "קריית אונו", "Kiryat Shalom", 
        "קריית שלום", "Ramat Hasharon", "רמת השרון", "Bnei Brak", "בני ברק", "Holon", "חולון", 
        "Jaffa", "יפו", "Yafo", "יפו", "Bat Yam", "בת ים"
    ],
    "judea and samaria": [
        "Ariel", "אריאל", "Beitar Illit", "ביתר עילית", "Efrat", "אפרת", "Elazar", "אלעזר", "Gush Etzion", 
        "גוש עציון", "Hebron", "חברון", "Itamar", "איתמר", "Kiryat Arba", "קריית ארבע", "Ma'ale Adumim", 
        "מעלה אדומים", "Nokdim", "נוקדים", "Ofra", "עפרה", "Shilo", "שילה", "Tekoa", "תקוע", 
        "Yitzhar", "יצהר", "Zaatara", "זעתרה", "Neve Daniel", "נווה דניאל", "Kfar Tapuach", "כפר תפוח",
        "Kochav Ya'akov", "כוכב יעקב", "Mitzpeh Yericho", "מצפה יריחו", "Teneh Omarim", "תניו עומרי"]
    
}



# Function to determine city region
def classify_city(city):
    for region, cities in regions.items():
        if city in cities:
            return region
    return "Unknown"

# Read .docx files
def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

# Read .pdf files
def read_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(p.extract_text() for p in reader.pages if p.extract_text())

def normalize_text(text):
    # Convert to lowercase, replace hyphens and apostrophes with spaces, and strip extra spaces
    text = text.lower()
    text = text.replace("-", " ").replace("'", " ")
    return text.strip()

def extract_city(text):
    normalized_text = normalize_text(text)
    for region_cities in regions.values():
        for city in region_cities:
            normalized_city = normalize_text(city)
            if normalized_city in normalized_text:
                return city
    return None

# Main logic to process all files in the folder
def process_folder(folder_path):

    # Loop over all files in the directory
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Skip directories, process files only
        if os.path.isdir(file_path):
            continue
        
        ext = os.path.splitext(filename)[1].lower()
        text = ""

        # Read the file based on its type
        if ext == ".docx":
            text = read_docx(file_path)
        elif ext == ".pdf":
            text = read_pdf(file_path)
        else:
            print(f"Skipping unsupported file type: {filename}")
            continue

        # Extract city and classify
        city = extract_city(text)
        if city:
            region = classify_city(city)
            print(f"Classified {filename} as {region}")

            # Move the file to the corresponding region folder
            destination_folder = os.path.join(folder_path, region)
            shutil.move(file_path, os.path.join(destination_folder, filename))
        else:
            print(f"No city found in {filename}, skipping.")

base_path =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder_names = ["north", "jerusalem", "haifa", "central", "south", "tel aviv", "judea and samaria"]

for folder_name in folder_names:
    folder_path = os.path.join(base_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

process_folder(base_path)