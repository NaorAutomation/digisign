from supabase import create_client, Client
from datetime import datetime

# אתחול לקוח Supabase עם מפתח service_role
url = "https://eyptzafolyszoyetupuv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5cHR6YWZvbHlzem95ZXR1cHV2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NjMxMjI4NywiZXhwIjoyMDYxODg4Mjg3fQ.EL4CjO8kKVznv220fKwKgUhT1YgjaEsiwiE3VXc2c5w"
supabase: Client = create_client(url, key)

# פעולות עסק
def get_business_by_id_number(business_id_number):
    """קבלת עסק לפי מספר ח.פ."""
    response = supabase.table('businesses').select('*').eq('business_id_number', business_id_number).execute()
    return response.data[0] if response.data else None

def get_business(business_id):
    """קבלת עסק לפי מזהה פנימי."""
    response = supabase.table('businesses').select('*').eq('business_id', business_id).execute()
    return response.data[0] if response.data else None

def create_business(business_data):
    """יצירת עסק חדש."""
    response = supabase.table('businesses').insert(business_data).execute()
    return response.data[0]['business_id'] if response.data else None

def update_business(business_id, business_data):
    """עדכון פרטי עסק."""
    response = supabase.table('businesses').update(business_data).eq('business_id', business_id).execute()
    return response.data[0] if response.data else None

# פעולות חוזה
def create_contract(contract_data):
    """יצירת חוזה חדש."""
    response = supabase.table('contracts').insert(contract_data).execute()
    return response.data[0]['contract_id'] if response.data else None

def get_contract(contract_id):
    """קבלת חוזה לפי מזהה."""
    response = supabase.table('contracts').select('*').eq('contract_id', contract_id).execute()
    return response.data[0] if response.data else None

def get_contract_by_url(unique_url):
    """קבלת חוזה לפי URL ייחודי."""
    response = supabase.table('contracts').select('*').eq('unique_url', unique_url).execute()
    return response.data[0] if response.data else None

def get_business_contracts(business_id):
    """קבלת כל החוזים לעסק מסוים."""
    response = supabase.table('contracts').select('*').eq('business_id', business_id).order('created_at', desc=True).execute()
    return response.data if response.data else []

def update_contract(contract_id, contract_data):
    """עדכון פרטי חוזה."""
    response = supabase.table('contracts').update(contract_data).eq('contract_id', contract_id).execute()
    return response.data[0] if response.data else None