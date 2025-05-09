import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
from supabase import create_client, Client

# אתחול לקוח Supabase עם מפתח service_role
url = "https://eyptzafolyszoyetupuv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5cHR6YWZvbHlzem95ZXR1cHV2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NjMxMjI4NywiZXhwIjoyMDYxODg4Mjg3fQ.EL4CjO8kKVznv220fKwKgUhT1YgjaEsiwiE3VXc2c5w"
supabase: Client = create_client(url, key)

def generate_unique_filename(original_filename):
    """יצירת שם קובץ ייחודי."""
    file_ext = os.path.splitext(original_filename)[1]
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    random_str = str(uuid.uuid4())[:8]
    return f"{timestamp}-{random_str}{file_ext}"

def upload_logo(file):
    """העלאת לוגו של עסק."""
    filename = secure_filename(file.filename)
    unique_filename = generate_unique_filename(filename)
    
    # קריאת תוכן הקובץ
    file_content = file.read()
    
    # העלאה לאחסון
    response = supabase.storage.from_('logos').upload(unique_filename, file_content)
    
    # קבלת URL ציבורי
    public_url = supabase.storage.from_('logos').get_public_url(unique_filename)
    
    return public_url

def upload_document(file):
    """העלאת מסמך חוזה."""
    filename = secure_filename(file.filename)
    unique_filename = generate_unique_filename(filename)
    
    # קריאת תוכן הקובץ
    file_content = file.read()
    
    # העלאה לאחסון
    response = supabase.storage.from_('pdf').upload(unique_filename, file_content)
    
    # קבלת URL ציבורי
    public_url = supabase.storage.from_('pdf').get_public_url(unique_filename)
    
    return public_url

def upload_id(file):
    """העלאת תעודת זהות לקוח."""
    try:
        filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(filename)
        
        # קריאת תוכן הקובץ וחזרה לתחילת הקובץ
        file.seek(0)
        file_content = file.read()
        
        # וידוא שהתוכן לא ריק
        if not file_content:
            print("תוכן קובץ ת.ז ריק")
            return None
        
        print(f"העלאת ת.ז: גודל הקובץ {len(file_content)} בייטים")
        
        # העלאה לאחסון
        response = supabase.storage.from_('id').upload(unique_filename, file_content)
        
        # שמירת נתיב פנימי
        file_path = f"id/{unique_filename}"
        
        return file_path
    except Exception as e:
        print(f"שגיאה בהעלאת ת.ז: {str(e)}")
        raise

def upload_signature(file):
    """העלאת חתימת לקוח."""
    try:
        filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(filename)
        
        # קריאת תוכן הקובץ וחזרה לתחילת הקובץ
        file.seek(0)
        file_content = file.read()
        
        # וידוא שהתוכן לא ריק
        if not file_content:
            print("תוכן קובץ החתימה ריק")
            return None
        
        print(f"העלאת חתימה: גודל הקובץ {len(file_content)} בייטים")
        
        # העלאה לאחסון
        response = supabase.storage.from_('id').upload(f"signatures/{unique_filename}", file_content)
        
        # שמירת נתיב פנימי
        file_path = f"id/signatures/{unique_filename}"
        
        return file_path
    except Exception as e:
        print(f"שגיאה בהעלאת חתימה: {str(e)}")
        raise

def get_public_url(file_path):
    """קבלת URL ציבורי עבור קובץ בסטורג'."""
    try:
        print(f"מנסה להשיג URL ציבורי עבור: {file_path}")
        
        # במקרה שהנתיב כבר מכיל URL מלא
        if file_path.startswith('http'):
            return file_path
            
        # טיפול בנתיבים מיוחדים
        if file_path.startswith('id/signatures/'):
            # תיקון נתיב של חתימה - הסרת "id/" מתחילת הנתיב
            clean_path = file_path.replace('id/', '')
            url = supabase.storage.from_('id').get_public_url(clean_path)
            print(f"נתיב חתימה מתוקן: {clean_path} -> URL: {url}")
            return url
            
        elif file_path.startswith('id/'):
            # תיקון נתיב של תעודת זהות - הסרת "id/" מתחילת הנתיב
            clean_path = file_path.replace('id/', '')
            url = supabase.storage.from_('id').get_public_url(clean_path)
            print(f"נתיב ת.ז מתוקן: {clean_path} -> URL: {url}")
            return url
            
        elif file_path.startswith('signatures/'):
            # חתימות בתיקיית signatures
            url = supabase.storage.from_('id').get_public_url(file_path)
            print(f"נתיב חתימה: {file_path} -> URL: {url}")
            return url
            
        else:
            # קביעת באקט מתאים לפי תחילת הנתיב
            bucket = 'id'  # ברירת מחדל
            
            if file_path.startswith('logos/'):
                bucket = 'logos'
            elif file_path.startswith('pdf/'):
                bucket = 'pdf'
                
            url = supabase.storage.from_(bucket).get_public_url(file_path)
            print(f"נתיב כללי בבאקט {bucket}: {file_path} -> URL: {url}")
            return url
            
    except Exception as e:
        print(f"שגיאה בקבלת URL ציבורי: {str(e)}")
        # החזרת הנתיב המקורי במקרה של שגיאה
        return file_path