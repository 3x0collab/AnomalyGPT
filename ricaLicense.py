import datetime
import os
import socket
import uuid
from datetime import datetime as dt
from AnomalyPromptGRP.ricaED import E

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ricabackend.settings')


class genLicense():

    def __init__(self, gen_key=None, server_name=None, db_name="", mac_addr=None,
                 expiry_date=None, expired_in=60, no_of_users=10):

        if gen_key:
            # f"{self.server_name}.{self.db_name}.{self.get_mac()}.{expiry_date}"
            gen_key = E('ot',char_only=False).D(gen_key) 
            split_key = gen_key.split(".*")
            self.server_name = split_key[0]
            self.mac = split_key[1]
            self.no_of_users = split_key[2]
            self.db_name = split_key[3]
            self.expiry_date = split_key[4]
        else:
            self.server_name = "ADR" #server_name or socket.gethostname()
            self.db_name = db_name
            self.mac = "OIT" #mac_addr or self.get_mac()
            self.no_of_users = no_of_users
            self.expired_in = (24*60)*int(expired_in)  # 7 days
            self.expiry_date = expiry_date or self.gen_expire_date(
                datetime.datetime.now(), self.expired_in)  # 2022-08-18      
        self.key = self.create()
        print("key==",no_of_users,expiry_date)

    def create_date(self, date):
        if not date:
            return None
        return datetime.date(date.year, date.month, date.day)

    def get_present_date(self):
        # try:
        # 	x = requests.get("http://worldtimeapi.org/api/timezone/Arica/Lagos")
        # 	x_val = x.json()['datetime']
        # 	return parse(x.json()['datetime'])
        # except:
        return dt.now()

    def create_datetime(self, date, minute=0):
        if not date:
            return None
        return datetime.datetime(date.year, date.month, date.day) + datetime.timedelta(minutes=int(minute))

    def gen_expire_date(self, date, expired_in):
        v_date = self.create_datetime(date, expired_in)
        return self.create_date(v_date)

    def verify_license(self, license_code):
        if self.key == license_code:
            if self.has_expire():
                print(f"This License Code: {license_code} has EXPIRED, update your License.")
                return 'EXPIRED'
            elif len(license_code.replace("-","")) > 20 or len( license_code.replace("-","")) < 20:
                print(f"This License Code: {license_code} is INVALID, update your License.")
                return 'INVALID'
            print(f"License: {license_code} is VALID")
            return 'VALID'
        else:
            if not license_code or license_code == " ":
                return "NO LICENSE"
            print(f"This License Code: {license_code} is INVALID, update your License.")
            return 'INVALID'

    def gen_code(self):
        en = E('ot',char_only=False)
        body = f"{self.server_name}.*{self.get_mac()}.*{self.no_of_users}.*{self.db_name}.*{self.expiry_date}"
        code = en.E(body)
        # print(f"Gen Key: {body}, Encrypted Code: {code}")
        return code

    def has_expire(self):
        string_input_with_date = str(self.expiry_date)
        expire_date = dt.strptime(string_input_with_date, "%Y-%m-%d")
        present = self.get_present_date()
        if expire_date.date() < present.date():
            return True

    def get_mac(self, real=False):
        # from RICA_workstation.views import get_mac_address as gma
        # mac_address = gma().replace(":", "")
        return 'OIT'
        # return ':'.join(re.findall('..', '%012x' % uuid.getnode())) if real else ''.join(re.findall('..', '%012x' % uuid.getnode()))

    def create_key(self, body):
        c = body.split("+")
        cdate = c[-1]
        d1 = cdate[0:2]
        d2 = cdate[2:4]
        d3 = cdate[4:8]
        d4 = cdate[8:]
        en = E('ot',char_only=False)
        hash_split = f"{self.hash(c[0]+c[2])[-2:]+d1}-{self.hash(c[2])[-2:]+d2}-{d3}-{self.hash(c[1])[-4:]}-{en.E(d4)}".split("-")
        return '-'.join(hash_split)

    def extract_date(self, license):
        c = license.split("-")
        ex_date = f"{c[0][-2:]}{c[1][-2:]}-{c[2][:2]}-{c[2][2:]}"
        return ex_date
    def extract_noofusers(self, license):
        c = license.split("-")
        no = c[4]
        return  E('ot',char_only=False).D(no) 

        # year

    def hash(self, body):
        hash_str = uuid.uuid5(uuid.NAMESPACE_DNS, body)
        return str(hash_str)

    def create(self):
        expiry_date = self.expiry_date
        body = f"{self.db_name}+{self.mac}+{self.server_name}+{expiry_date}{self.no_of_users}".replace(
            ".", "").replace("/", "").replace("-", "").replace(":", "")
        # print('body===',body)
        license_code = self.create_key(body)
        # print(
        # f"License Code: {license_code} for {self.no_of_users} users, will expired on {self.extract_date(license_code)}")
        return license_code
        # return license_code


if __name__ == '__main__':

    # Generate a new gen key for license.
    # license_creator = genLicense()
    # gen_key = license_creator.gen_code()

    # # Generate a new license code that expire in 30 days from gen key.
    license_creator2 = genLicense(
        gen_key=r'vAHKY.*VP0.*87.*87.b7.8f.99b:8ccb/pjvujlwAb.*979a-7g-9b', expired_in=60)
    license = license_creator2.key
    print(
        f"License Code: {license} for {license_creator2.no_of_users}, will expired on {license_creator2.extract_date(license)}")

 #    # # Verify if a license is valid
 #    license_creator3 = genLicense()
 #    extract_date = license_creator3.extract_date(license)
 #    print(extract_date)
 #    license_creator3 = genLicense(expiry_date=extract_date)
 #    print(license_creator3.verify_license(license)) 
 # 