import random
import uuid
from faker import Faker
import faker
from app.crud.user_types import create as create_user_type 
from app.crud.user_types import get_all as user_types_get_all
from app.crud.users import create as create_user
from app.crud.users import get_all as get_all_users
from app.crud.vendor_types import create as create_vendor_type
from app.crud.clients import create as create_client
from app.crud.realtors import create as create_realtor
from app.crud.vendors import create as create_vendor
from app.crud.vendors import get_all as get_all_vendors
from app.crud.listings import create as create_listing
from app.crud.listings import get_all as get_all_listings
from app.crud.reports import create as create_report
from app.crud.reports import get_all as get_all_reports
from app.crud.issues import create as create_issue
from app.crud.issues import get_all as get_all_issues
from app.crud.realtor_firms import create as create_realtor_firm
from app.crud.realtor_firms import get_all as get_all_realtor_firms
from app.crud.attachments import create as create_attachment
from app.crud.comments import create as create_comment
from app.crud.notes import create as create_note
from app.crud.issue_offers import create as create_issue_bid
from app.crud.issue_assessments import create as create_issue_assessment

from app.schema.properties import Attachments, Comments, Issue_Assessments, Issue_Bids, Listings, Notes, Reports, Issues
from app.schema.types import Status, User_Types, User_Type, Vendor_Types, Vendor_Type
from app.schema.users import Users, Clients, Realtors, Vendors
from app.schema.realtor_firms import Realtor_Firms



fake = Faker()

realtor_firms_made = []
admin_users_made = []
client_users_made = []
realtor_users_made = []
vendor_users_made = []
users_made = []

def get_user_data():
    global admin_users_made, client_users_made, realtor_users_made, vendor_users_made, users_made, realtor_firms_made

    users_made = get_all_users()
    realtor_firms_made = get_all_realtor_firms()
    client_users_made = [client_user for client_user in users_made if client_user['user_type']=='client']
    realtor_users_made = [realtor_user for realtor_user in users_made if realtor_user['user_type']=='realtor']
    vendor_users_made = [vendor_user for vendor_user in users_made if vendor_user['user_type']=='vendor']
    admin_users_made = [admin_user for admin_user in users_made if admin_user['user_type']=='admin']
    
def populate_user_types():
    """
    Populate the user_types table using the create method.
    """

    for user_type in User_Type:
        try:
            user_type_obj = User_Types(user_type=user_type)
            result = create_user_type(user_type_obj)  
            print(f"Inserted: {result}")
        except Exception as e:
            print(f"Skipping {user_type.value}: {str(e)}")

def populate_vendor_types():
    """
    Populate the vendor_types table.
    """
    for vendor_type in Vendor_Type: 
        try:
            vendor_type_obj = Vendor_Types(vendor_type=vendor_type)
            result = create_vendor_type(vendor_type_obj)
            print(f"Inserted vendor type: {result}")
        except Exception as e:
            print(f"Error inserting vendor type {vendor_type.value}: {str(e)}")

def make_admins():
    """
    Populates 5 admins using real data
    """
    



def populate_users(admin_records: int = 5, client_records: int = 20, realtor_records: int=10, vendor_records: int = 20):
    """Populate the users table."""

    user_types = user_types_get_all()
    if not user_types:
        print("No user types found. Please create user types first.")
        return

    user_types_in_db = []
    for user_type_dict in user_types:  
        user_types_in_db.append(user_type_dict['user_type'])

    
    
    if 'admin' in user_types_in_db:
        print(f"Making {admin_records} users with type as admins")
        for _ in range(admin_records):
            try:
                
                user_data = {
                    "user_type": {
                        "user_type" : User_Type.ADMIN
                    },  
                    "firebase_id": str(uuid.uuid4()) 
                }

                user = Users(**user_data)
                created_user = create_user(user) 
                admin_users_made.append(created_user)
                print(f"Inserted user: {created_user}")

            except Exception as e:
                print(f"Error inserting user: {str(e)}")
    
    
    if 'client' in user_types_in_db:
        print(f"Making {client_records} users with type as clients")
        for _ in range(client_records):
            try:
               
                user_data = {
                    "user_type": {
                        "user_type" : User_Type.CLIENT
                    },  
                    "firebase_id": str(uuid.uuid4()) 
                }

                user = Users(**user_data)
                created_user = create_user(user) 
                client_users_made.append(created_user)
                print(f"Inserted user: {created_user}")

            except Exception as e:
                print(f"Error inserting user: {str(e)}")


    if 'realtor' in user_types_in_db:
        print(f"Making {realtor_records} users with type as realtor")
        for _ in range(realtor_records):
            try:
               
                user_data = {
                    "user_type": {
                        "user_type" : User_Type.REALTOR
                    },  
                    "firebase_id": str(uuid.uuid4()) 
                }

                user = Users(**user_data)
                created_user = create_user(user) 
                realtor_users_made.append(created_user)
                print(f"Inserted user: {created_user}")

            except Exception as e:
                print(f"Error inserting user: {str(e)}")
    
    
    if 'vendor' in user_types_in_db:
        print(f"Making {vendor_records} users with type as vendors")
        for _ in range(vendor_records):
            try:
                
                user_data = {
                    "user_type": {
                        "user_type" : User_Type.VENDOR
                    },  
                    "firebase_id": str(uuid.uuid4()) 
                }

                user = Users(**user_data) 
                created_user = create_user(user)
                vendor_users_made.append(created_user)
                print(f"Inserted user: {created_user}")

            except Exception as e:
                print(f"Error inserting user: {str(e)}")



def populate_clients():
    """Populate the clients table."""

    for i in range(len(client_users_made)):
        try:
            client_data = { 
                "user_id": client_users_made[i]['id'],
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "address": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "country": fake.country(),
                "postal_code": fake.postcode(),
            }

            client = Clients(**client_data)
            created_client = create_client(client)
            print(f"Inserted client: {created_client}")

        except Exception as e:
            print(f"Error inserting client: {str(e)}")

def populate_realtor_firms(num_firms: int = 5):
    """Populate the realtor_firms table."""

    for _ in range(num_firms):
        try:
            realtor_firm_data = {
                "name": fake.company(),
                "code": fake.lexify('?????'),  
                "email": fake.email(),
                "phone": fake.phone_number(),
                "address": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "country": fake.country(),
                "postal_code": fake.postcode(),
                "rating": random.randint(1, 5),  
                "review": fake.text(), 
            }

            realtor_firm = Realtor_Firms(**realtor_firm_data) 
            created_realtor_firm = create_realtor_firm(realtor_firm)  
            print(f"Inserted realtor firm: {created_realtor_firm}")

        except Exception as e:
            print(f"Error inserting realtor firm: {str(e)}")

def populate_realtors():
    """Populate the realtors table using existing realtor users and firms. Picks realtor firm randomly"""

    for realtor_user in realtor_users_made: 
        try:
            realtor_firm = random.choice(realtor_firms_made) 
            realtor_data = {
                "realtor_user_id": realtor_user['id'], 
                "realtor_firm_id": realtor_firm['id'],  
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "address": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "country": fake.country(),
                "postal_code": fake.postcode(),
                "rating": random.randint(1, 5),
                "review": fake.text(),
            }

            realtor_create = Realtors(**realtor_data)
            created_realtor = create_realtor(realtor_create)
            print(f"Inserted realtor: {created_realtor}")
        except Exception as e:
            print(f"Error inserting realtor : {str(e)}")

def populate_real_admins():
    """Populate 5 real admins as realtors"""
        
    try:
        realtor_firm = random.choice(realtor_firms_made)  # Randomly choose a firm
        realtor_data = {
            "realtor_user_id": admin_users_made[0]['id'],  # Use existing user ID
            "realtor_firm_id": realtor_firm['id'],  # Use ID of randomly chosen firm
            "first_name": 'Abid Al',
            "last_name": 'Labib',
            "email": 'getabidallabib@gmail.com',
            "phone": '9297296392',
            "address": '8630 132nd Street Richmondhill',
            "city": 'Jamaica',
            "state": 'NY',
            "country": 'USA',
            "postal_code": '11418',
            "rating": random.randint(1, 5),
            "review": fake.text(),
        }

        realtor_create = Realtors(**realtor_data)
        created_realtor = create_realtor(realtor_create)
        print(f"Inserted realtor: {created_realtor}")
    except Exception as e:
        print(f"Error inserting realtor : {str(e)}")


    try:
        realtor_firm = random.choice(realtor_firms_made)  # Randomly choose a firm
        realtor_data = {
            "realtor_user_id": admin_users_made[1]['id'],  # Use existing user ID
            "realtor_firm_id": realtor_firm['id'],  # Use ID of randomly chosen firm
            "first_name": 'Sharhad',
            "last_name": 'Bashar',
            "email": 'sharhadbashar09@gmail.com',
            "phone": '6466838387',
            "address": 'Financial District',
            "city": 'Manhattan',
            "state": 'NY',
            "country": 'USA',
            "postal_code": '10038',
            "rating": random.randint(1, 5),
            "review": fake.text(),
        }

        realtor_create = Realtors(**realtor_data)
        created_realtor = create_realtor(realtor_create)
        print(f"Inserted realtor: {created_realtor}")
    except Exception as e:
        print(f"Error inserting realtor : {str(e)}")
    
    
    try:
        realtor_firm = random.choice(realtor_firms_made)  # Randomly choose a firm
        realtor_data = {
            "realtor_user_id": admin_users_made[2]['id'],  # Use existing user ID
            "realtor_firm_id": realtor_firm['id'],  # Use ID of randomly chosen firm
            "first_name": 'Yousef',
            "last_name": 'Ouda',
            "email": 'Ouda.yousef@gmail.com',
            "phone": '226-984-1252',
            "address": 'Somewhere in Canada',
            "city": 'London',
            "state": 'ON',
            "country": 'Canada',
            "postal_code": 'T2N T2N',
            "rating": random.randint(1, 5),
            "review": fake.text(),
        }

        realtor_create = Realtors(**realtor_data)
        created_realtor = create_realtor(realtor_create)
        print(f"Inserted realtor: {created_realtor}")
    except Exception as e:
        print(f"Error inserting realtor : {str(e)}")
    
    
    try:
        realtor_firm = random.choice(realtor_firms_made)  # Randomly choose a firm
        realtor_data = {
            "realtor_user_id": admin_users_made[3]['id'],  # Use existing user ID
            "realtor_firm_id": realtor_firm['id'],  # Use ID of randomly chosen firm
            "first_name": 'Manzur',
            "last_name": 'Mulk',
            "email": 'manzurmmulk@gmail.com',
            "phone": '5193196471',
            "address": 'A place in canada',
            "city": 'London',
            "state": 'ON',
            "country": 'Canada',
            "postal_code": 'T2V T2V',
            "rating": random.randint(1, 5),
            "review": fake.text(),
        }

        realtor_create = Realtors(**realtor_data)
        created_realtor = create_realtor(realtor_create)
        print(f"Inserted realtor: {created_realtor}")
    except Exception as e:
        print(f"Error inserting realtor : {str(e)}")
    
    
    try:
        realtor_firm = random.choice(realtor_firms_made)  # Randomly choose a firm
        realtor_data = {
            "realtor_user_id": admin_users_made[4]['id'],  # Use existing user ID
            "realtor_firm_id": realtor_firm['id'],  # Use ID of randomly chosen firm
            "first_name": 'Mohammed',
            "last_name": 'Alaa',
            "email": 'hamadax.alaa@gmail.com',
            "phone": '2121212',
            "address": 'Somewhere in Canada',
            "city": 'London',
            "state": 'ON',
            "country": 'Canada',
            "postal_code": 'T3A T2A',
            "rating": random.randint(1, 5),
            "review": fake.text(),
        }

        realtor_create = Realtors(**realtor_data)
        created_realtor = create_realtor(realtor_create)
        print(f"Inserted realtor: {created_realtor}")
    except Exception as e:
        print(f"Error inserting realtor : {str(e)}")


def populate_vendors():
    """Populate the vendors table, one of each type, then the rest are random types."""

    vendor_types = list(Vendor_Type)  # Get all vendor types as a list
    vendors_created_for_type = set() # Keep track of the vendor types created
    vendor_users_available = list(vendor_users_made) # Create a copy to be able to remove elements.

    print("picking each vendor type once")
    for vendor_type in vendor_types:
        for vendor_user in vendor_users_available:
            try:
                vendor_type_instance = Vendor_Types(vendor_type=vendor_type)
                vendor_data = {
                    "vendor_user_id": vendor_user['id'],
                    "vendor_type": vendor_type_instance,
                    "code": fake.lexify('?????'),
                    "name": fake.company(),
                    "email": fake.email(),
                    "phone": fake.phone_number(),
                    "address": fake.street_address(),
                    "city": fake.city(),
                    "state": fake.state(),
                    "country": fake.country(),
                    "postal_code": fake.postcode(),
                    "rating": random.randint(1, 5),
                    "review": fake.text(),
                }

                vendor_create = Vendors(**vendor_data)
                created_vendor = create_vendor(vendor_create)
                print(f"Inserted vendor: {created_vendor}")
                vendors_created_for_type.add(vendor_type) # Add to the set
                vendor_users_available.remove(vendor_user) # Remove the user from the list
                break # Break out of the inner loop once the vendor is created
            except Exception as e:
                print(f"Error inserting vendor: {str(e)}")

    print("Randomly picking vendor types")
    for vendor_user in vendor_users_available:
        try:
            vendor_type_enum = random.choice(list(Vendor_Type))
            vendor_type_instance = Vendor_Types(vendor_type=vendor_type_enum)

            vendor_data = {
                "vendor_user_id": vendor_user['id'],
                "vendor_type": vendor_type_instance,
                "code": fake.lexify('?????'),
                "name": fake.company(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "address": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "country": fake.country(),
                "postal_code": fake.postcode(),
                "rating": random.randint(1, 5),
                "review": fake.text(),
            }

            vendor_create =Vendors(**vendor_data)
            created_vendor = create_vendor(vendor_create)
            print(f"Inserted vendor: {created_vendor}")

        except Exception as e:
            print(f"Error inserting vendor: {str(e)}")

def populate_listings(num_listings: int = 40):
    """
    Populate the listings table.
    """

    users_available = realtor_users_made + client_users_made 

    for _ in range(num_listings): 
        try:
            user = random.choice(users_available) 
            listing_data = {
                "user_id": user['id'],
                "address": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "country": fake.country(),
                "postal_code": fake.postcode(),
                "image_url": fake.image_url(),  
            }

            listing_create = Listings(**listing_data)
            created_listing = create_listing(listing_create)
            print(f"Inserted listing: {created_listing}")

        except Exception as e:
            print(f"Error inserting listing: {str(e)}")

def populate_reports():
    """Populate the reports table, one report for each listing."""

    listings = get_all_listings()  
    if not listings:
        print("No listings found. Please create listings first.")
        return

    users_available = realtor_users_made + client_users_made 
    if not users_available:
        print("No users found. Skipping report creation.")
        return
    
    for listing in listings:
        try:
            user = random.choice(users_available) 
            report_data = {
                "user_id": user['id'],
                "listing_id": listing['id'], 
                "aws_link": fake.url(), 
                "name": fake.catch_phrase(), 
            }

            report_create = Reports(**report_data)  
            created_report = create_report(report_create)  
            print(f"Inserted report: {created_report}")

        except Exception as e:
            print(f"Error inserting report: {str(e)}")

def populate_issues(issues_per_report: int = 3):
    """Populate the issues table, a specified number taken as param per report."""

    reports = get_all_reports()
    if not reports:
        print("No reports found. Please create reports first.")
        return
  
    for report in reports:
        for _ in range(issues_per_report):
            try:
                vendors_available = get_all_vendors()
                if not vendors_available:
                    print("No vendors found. Skipping issue creation.")
                    return 
                vendor = random.choice(vendors_available) 
                issue_data = {
                    "report_id": report['id'],
                    "vendor_id": vendor['id'],  
                    "type": fake.random_element(elements=('general','structural','electrician','plumber','painter','cleaner','hvac','roofing','insulation','drywall','plaster','carpentry','landscaping','other')),
                    "description": fake.text(),
                    "summary": fake.catch_phrase(),
                    "severity": fake.random_element(elements=("low", "medium", "high")),
                    "status": random.choice(list(Status)), 
                    "active": random.choice([True, False]),
                    "cost": round(random.uniform(0, 1000), 2), 
                    "image_url": fake.image_url(), 
                }

                issue_create = Issues(**issue_data)
                created_issue = create_issue(issue_create)
                print(f"Inserted issue: {created_issue}")

            except Exception as e:
                print(f"Error inserting issue: {str(e)}")
    
def populate_attachments(attachments_per_issue: int = 2):
    """Populate the attachments table, a specified number per issue. user id is randomly chosen from existing users"""

    issues = get_all_issues()
    if not issues:
        print("No issues found. Please create issues first.")
        return

    for issue in issues:
        for _ in range(attachments_per_issue):
            try:
                if not users_made:
                    print("No users found. Skipping attachment creation.")
                    break

                user = random.choice(users_made)
                attachment_data = {
                    "issue_id": issue['id'],
                    "user_id": user['id'],  #
                    "name": fake.file_name(),  
                    "type": fake.random_element(elements=("image", "document", "video", "other")), # Random type
                    "url": fake.url(),  # Or your URL generation
                }

                attachment_create = Attachments(**attachment_data)
                created_attachment = create_attachment(attachment_create)
                print(f"Inserted attachment: {created_attachment}")

            except Exception as e:
                print(f"Error inserting attachment: {str(e)}")

def populate_comments(comments_per_issue: int = 2):
    """Populate the comments table, a specified number per issue. users ids are randomly chosen from existing users"""

    issues = get_all_issues()
    if not issues:
        print("No issues found. Please create issues first.")
        return

    if not users_made: # Check if there are any users available
        print("No users found. Skipping comment creation.")
        return

    for issue in issues:
        for _ in range(comments_per_issue):
            try:

                user = random.choice(users_made)  # Randomly choose a user
                comment_data = {
                    "issue_id": issue['id'],
                    "user_id": user['id'],  # Random user ID
                    "comment": fake.text(),  # Or your comment generation
                }

                comment_create = Comments(**comment_data)
                created_comment = create_comment(comment_create)
                print(f"Inserted comment: {created_comment}")

            except Exception as e:
                print(f"Error inserting comment: {str(e)}")

def populate_notes(notes_per_report: int = 2):
    """Populate the notes table, a specified number per report, using the report's user ID."""

    reports = get_all_reports()
    if not reports:
        print("No reports found. Please create reports first.")
        return

    for report in reports:
        for _ in range(notes_per_report):
            try:
                note_data = {
                    "report_id": report['id'],
                    "user_id": report['user_id'], 
                    "note": fake.text(), 
                }

                note_create = Notes(**note_data)
                created_note = create_note(note_create)
                print(f"Inserted note: {created_note}")

            except Exception as e:
                print(f"Error inserting note: {str(e)}")

def populate_issue_bids():
    """Populate the issue_bids table, 1-3 bids per issue. Randomly chooses a vendor id from existing vendors"""

    issues = get_all_issues()
    if not issues:
        print("No issues found. Please create issues first.")
        return

    vendors_available = get_all_vendors()
    if not vendors_available:  
        print("No vendors found. Skipping issue bid creation.")
        return

    for issue in issues:
        num_bids = random.randint(1, 3)  

        for _ in range(num_bids):
            try:
                vendor = random.choice(vendors_available) 
                status = random.choice(['received','accepted','rejected']) 
                issue_bid_data = {
                    "issue_id": issue['id'],
                    "vendor_id": vendor['id'],
                    "price": round(random.uniform(100, 5000), 2),  
                    "status": status, 
                    "comment_vendor": fake.text(),
                    "comment_client": fake.text(),
                    "active": random.choice([True, False]),
                }

                print(issue_bid_data)
                issue_bid_create = Issue_Bids(**issue_bid_data)
                created_issue_bid = create_issue_bid(issue_bid_create)
                print(f"Inserted issue bid: {created_issue_bid}")

            except Exception as e:
                print(f"Error inserting issue bid: {str(e)}")

def populate_issue_assessments():
    """Populate the issue_assessments table, 1-3 assessments per issue. Vendor id is chosen randomly"""

    issues = get_all_issues()
    if not issues:
        print("No issues found. Please create issues first.")
        return

    vendors_available = get_all_vendors()
    if not vendors_available:
        print("No vendors found. Skipping issue assessment creation.")
        return

    for issue in issues:
        num_assessments = random.randint(1, 3)  

        for _ in range(num_assessments):
            try:
                vendor = random.choice(vendors_available) 
                assessment_date = str(fake.date_time_between(start_date="-1y", end_date="now"))
                status = random.choice(['received','accepted','rejected']) 
                issue_assessment_data = {
                    "issue_id": issue['id'],
                    "vendor_id": vendor['id'],
                    "date": assessment_date,
                    "status": status, 
                    "comment_vendor": fake.text(),
                    "comment_client": fake.text(),
                }

                issue_assessment_create = Issue_Assessments(**issue_assessment_data)
                created_issue_assessment = create_issue_assessment(issue_assessment_create)
                print(f"Inserted issue assessment: {created_issue_assessment}")

            except Exception as e:
                print(f"Error inserting issue assessment: {str(e)}")

def run():
    """ Run all population methods in order or selectively by commenting out the ones you don't want to populate"""
    populate_user_types()
    populate_vendor_types()
    populate_realtor_firms()
    populate_users( )
    get_user_data()
    populate_clients()
    populate_realtors()
    populate_vendors()
    populate_real_admins()
    populate_listings()
    populate_reports()
    populate_issues()
    populate_attachments()
    populate_comments()
    populate_notes()
    populate_issue_bids()
    populate_issue_assessments()

if __name__ == "__main__":
    run()