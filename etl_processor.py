import pandas as pd
import os
import glob

BASE_DIR = os.getcwd() 

# Folder Names (Matches your provided list)
FOLDERS = {
    'bio': 'api_data_aadhar_biometric',
    'enrol': 'api_data_aadhar_enrolment',
    'demo': 'api_data_aadhar_demographic'
}

JUNK_NAMES = {
    '?', 'invalid', 'idpl colony', 'near dhyana ashram', 
    'near uday nagar nit garden', 'near university thana', 
    'near meera hospital', 'naihati anandabazar', 
    'bally jagachha', 'domjur', 'south dumdum(m)', 'dist : thane'
}

district_fixer = {
    'Ananthapur': 'Anantapur', 'Ananthapuramu': 'Anantapur',
    'Chittoor': 'Chittoor', 'chittoor': 'Chittoor',
    'Cuddapah': 'YSR District', 'Y. S. R': 'YSR District', 'Y.S.R': 'YSR District',
    'K.V.Rangareddy': 'Ranga Reddy', 'Rangareddi': 'Ranga Reddy', 'Rangareddy': 'Ranga Reddy',
    'Mahabubnagar': 'Mahbubnagar', 'Mahabub Nagar': 'Mahbubnagar',
    'Spsr Nellore': 'Nellore', 'Sri Potti Sriramulu Nellore': 'Nellore',
    'Visakhapatanam': 'Visakhapatnam',
    'Warangal (urban)': 'Hanumakonda', 'Warangal Urban': 'Hanumakonda',
    'Warangal Rural': 'Warangal',
    'Sibsagar': 'Sivasagar',
    'Kamrup Metro': 'Kamrup Metropolitan',
    'Ri Bhoi': 'Ri-Bhoi', 
    'Kaimur (Bhabua)': 'Kaimur', 'Bhabua': 'Kaimur',
    'Purnea': 'Purnia',
    'Pashchim Champaran': 'West Champaran',
    'Purbi Champaran': 'East Champaran',
    'Jehanabad': 'Jahanabad',
    'Janjgir - Champa': 'Janjgir-Champa', 'Janjgir Champa': 'Janjgir-Champa', 'Janjgir-champa': 'Janjgir-Champa',
    'Kabeerdham': 'Kabirdham', 'Kawardha': 'Kabirdham',
    'Uttar Bastar Kanker': 'Kanker',
    'Dakshin Bastar Dantewada': 'Dantewada',
    'Ahmadabad': 'Ahmedabad',
    'Banaskantha': 'Banaskantha', 'Banas Kantha': 'Banaskantha',
    'Sabarkantha': 'Sabarkantha', 'Sabar Kantha': 'Sabarkantha',
    'Dohad': 'Dahod',
    'Panch Mahals': 'Panchmahal', 'Panchmahals': 'Panchmahal',
    'The Dangs': 'Dang',
    'Kachchh': 'Kutch',
    'Gurgaon': 'Gurugram',
    'Mewat': 'Nuh',
    'Bengaluru': 'Bangalore', 'Bengaluru Urban': 'Bangalore', 
    'Belgaum': 'Belagavi',
    'Bellary': 'Ballari',
    'Bijapur': 'Vijayapura', 'Bijapur(KAR)': 'Vijayapura',
    'Chickmagalur': 'Chikkamagaluru', 'Chikmagalur': 'Chikkamagaluru',
    'Davanagere': 'Davangere',
    'Gulbarga': 'Kalaburagi',
    'Mysore': 'Mysuru',
    'Shimoga': 'Shivamogga',
    'Tumkur': 'Tumakuru',
    'Uttara Kannada': 'Uttar Kannad',
    'Kasargod': 'Kasaragod',
    'Hoshangabad': 'Narmadapuram',
    'East Nimar': 'Khandwa',
    'West Nimar': 'Khargone',
    'Narsimhapur': 'Narsinghpur',
    'Ahmed Nagar': 'Ahmednagar', 'Ahilyanagar': 'Ahmednagar', 'Ahmadnagar': 'Ahmednagar',
    'Aurangabad': 'Chhatrapati Sambhajinagar', 'Chatrapati Sambhaji Nagar': 'Chhatrapati Sambhajinagar', 'Aurangabad(bh)': 'Aurangabad', 'Aurangabad(BH)': 'Aurangabad',
    'Beed': 'Bid',
    'Buldana': 'Buldhana',
    'Osmanabad': 'Dharashiv',
    'Gondiya': 'Gondia',
    'Mumbai( Sub Urban )': 'Mumbai Suburban',
    'Raigarh(MH)': 'Raigad',
    'Dist : Thane': 'Thane',
    'Angul': 'Angul', 'Anugul': 'Angul', 'Anugal': 'Angul', 'ANGUL': 'Angul',
    'Baleswar': 'Baleshwar',
    'Baudh': 'Boudh',
    'Jajapur': 'Jajpur',
    'Keonjhar': 'Kendujhar',
    'Khorda': 'Khordha',
    'Nabarangapur': 'Nabarangpur',
    'Sonepur': 'Subarnapur',
    'Sundergarh': 'Sundargarh',
    'Firozpur': 'Ferozepur',
    'S.A.S Nagar': 'SAS Nagar', 'S.A.S Nagar(Mohali)': 'SAS Nagar', 'Mohali': 'SAS Nagar',
    'Muktsar': 'Sri Muktsar Sahib',
    'Chittaurgarh': 'Chittorgarh',
    'Dhaulpur': 'Dholpur',
    'Jalor': 'Jalore',
    'Jhunjhunun': 'Jhunjhunu',
    'Kancheepuram': 'Kanchipuram',
    'Kanniyakumari': 'Kanyakumari',
    'Thoothukkudi': 'Tuticorin',
    'Thiruvallur': 'Tiruvallur',
    'Villupuram': 'Viluppuram',
    'Allahabad': 'Prayagraj',
    'Bara Banki': 'Barabanki',
    'Bulandshahar': 'Bulandshahr',
    'Faizabad': 'Ayodhya',
    'Jyotiba Phule Nagar': 'Amroha',
    'Kanshi Ram Nagar': 'Kasganj',
    'Mahrajganj': 'Maharajganj',
    'Sant Ravidas Nagar': 'Bhadohi', 'Sant Ravidas Nagar Bhadohi': 'Bhadohi',
    'Siddharth Nagar': 'Siddharthnagar',
    'Shrawasti': 'Shravasti',
    'Kheri': 'Lakhimpur Kheri',
    'Hardwar': 'Haridwar',
    'Barddhaman': 'Bardhaman', 'Burdwan': 'Bardhaman',
    'Coochbehar': 'Cooch Behar', 'Koch Bihar': 'Cooch Behar',
    'Darjiling': 'Darjeeling',
    'Hugli': 'Hooghly',
    'Haora': 'Howrah', 'Hawrah': 'Howrah',
    'Maldah': 'Malda',
    'Medinipur West': 'Paschim Medinipur', 'West Midnapore': 'Paschim Medinipur', 'West Medinipur': 'Paschim Medinipur',
    'East Midnapore': 'Purba Medinipur', 'East midnapore': 'Purba Medinipur',
    '24 Paraganas North': 'North 24 Parganas', 'North Twenty Four Parganas': 'North 24 Parganas',
    '24 Paraganas South': 'South 24 Parganas', 'South Twenty Four Parganas': 'South 24 Parganas', 'South 24 pargana': 'South 24 Parganas',
    'Puruliya': 'Purulia',
    'Dinajpur Uttar': 'Uttar Dinajpur', 'North Dinajpur': 'Uttar Dinajpur',
    'Dinajpur Dakshin': 'Dakshin Dinajpur', 'South Dinajpur': 'Dakshin Dinajpur',
    'Kolkata': 'Kolkata', 'Calcutta': 'Kolkata'
}

def clean_district_name(name):
    name = str(name).strip()
    name_lower = name.lower()
    
    if name_lower in JUNK_NAMES or '?' in name or 'invalid' in name_lower:
        return "INVALID"
    if name.isnumeric(): 
        return "INVALID"
    
    name = name.replace('*', '').strip()
    
    if name in district_fixer:
        return district_fixer[name]
    
    # Fallback: check Title Case
    return district_fixer.get(name.title(), name)

def load_all_csvs_in_folder(folder_name):
    path = os.path.join(BASE_DIR, folder_name, "*.csv")
    all_files = glob.glob(path)
    
    print(f"--> Found {len(all_files)} files in {folder_name}")
    
    df_list = []
    for filename in all_files:
        try:
            df = pd.read_csv(filename, low_memory=False)
            df_list.append(df)
        except Exception as e:
            print(f"    ERROR reading {filename}: {e}")
            
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame()

print("--- STARTING DATA LOADING ---")
bio_df = load_all_csvs_in_folder(FOLDERS['bio'])
enrol_df = load_all_csvs_in_folder(FOLDERS['enrol'])
demo_df = load_all_csvs_in_folder(FOLDERS['demo'])

print("\n--- STARTING CLEANING ---")

for df in [bio_df, enrol_df, demo_df]:
    if not df.empty and 'district' in df.columns:
        df['district_clean'] = df['district'].apply(clean_district_name)
        df = df[df['district_clean'] != 'INVALID']

print("\n--- AGGREGATING DATA ---")

if not bio_df.empty:
    bio_grouped = bio_df.groupby('district_clean')[['bio_age_5_17', 'bio_age_17_']].sum().reset_index()
else:
    bio_grouped = pd.DataFrame(columns=['district_clean', 'bio_age_5_17', 'bio_age_17_'])

if not demo_df.empty:
    demo_grouped = demo_df.groupby('district_clean')[['demo_age_5_17', 'demo_age_17_']].sum().reset_index()
else:
    demo_grouped = pd.DataFrame(columns=['district_clean', 'demo_age_5_17', 'demo_age_17_'])

if not enrol_df.empty:
    enrol_grouped = enrol_df.groupby('district_clean')[['age_5_17', 'age_18_greater']].sum().reset_index()
else:
    enrol_grouped = pd.DataFrame(columns=['district_clean', 'age_5_17', 'age_18_greater'])

print("\n--- MERGING DATASETS ---")

master_df = pd.merge(enrol_grouped, bio_grouped, on='district_clean', how='outer')
master_df = pd.merge(master_df, demo_grouped, on='district_clean', how='outer')
master_df = master_df.fillna(0)

output_filename = "AADHAAR_MASTER_DATA.csv"
master_df.to_csv(output_filename, index=False)

print(f"\nSUCCESS! Saved cleaned data to: {output_filename}")
print(f"Total Unique Districts Found: {len(master_df)}")
print("\nTop 5 Districts by Enrolment (18+):")
print(master_df.sort_values('age_18_greater', ascending=False)[['district_clean', 'age_18_greater']].head(5))