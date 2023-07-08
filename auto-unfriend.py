# ------ [ Author & Creator ] ------ #
Developer = 'Dvanmeploph Ferly Afriliyan'
Author = 'Dapunta Adyapaksi R.'
Version = 0.1
Facebook = 'Facebook.com/freya.xyz'
Instagram = 'Instagram.com/afriliyanferlly_shishigami'

# --> Modules
import requests,bs4,sys,os,datetime,re,time,json
from bs4 import BeautifulSoup as bs
from datetime import datetime

# -->  Clear Terminal
def clear():
    if "linux" in sys.platform.lower():os.system("clear")
    elif "win" in sys.platform.lower():os.system("cls")

# --> Ubah Bahasa
def language(cookie):
    try:
        with requests.Session() as xyz:
            req = xyz.get('https://mbasic.facebook.com/language/',cookies=cookie)
            pra = bs(req.content,'html.parser')
            for x in pra.find_all('form',{'method':'post'}):
                if 'Bahasa Indonesia' in str(x):
                    bahasa = {
                        "fb_dtsg": re.search(
                            'name="fb_dtsg" value="(.*?)"', req.text
                        )[1],
                        "jazoest": re.search(
                            'name="jazoest" value="(.*?)"', req.text
                        )[1],
                        "submit": "Bahasa Indonesia",
                    }
                    url = 'https://mbasic.facebook.com' + x['action']
                    exec = xyz.post(url,data=bahasa,cookies=cookie)
    except Exception as e:pass

# --> Waktu
def start():
    global Mulai_Jalan
    Mulai_Jalan = datetime.now()
def akhir():
    global Akhir_Jalan, Total_Waktu
    Akhir_Jalan = datetime.now()
    Total_Waktu = Akhir_Jalan - Mulai_Jalan
    try:
        Menit = str(Total_Waktu).split(':')[1]
        Detik = str(Total_Waktu).split(':')[2].replace('.',',').split(',')[0] + ',' + str(Total_Waktu).split(':')[2].replace('.',',').split(',')[1][:1]
        print('\nProgram Selesai Dalam Waktu %s Menit %s Detik\n'%(Menit,Detik))
    except Exception as e:
        print('\n\nProgram Selesai Dalam Waktu 0 Detik\n')

# --> Login
class login:
    def __init__(self):
        self.xyz = requests.Session()
        self.cek_cookies()
        main_dump()
    def cek_cookies(self):
        try:
            self.cookie     = {'cookie':open('login/cookie.json','r').read()}
            self.token_eaag = open('login/token_eaag.json','r').read()
            self.token_eaab = open('login/token_eaab.json','r').read()
            language(self.cookie)
            req1 = self.xyz.get(
                f'https://graph.facebook.com/me?fields=name,id&access_token={self.token_eaag}',
                cookies=self.cookie,
            ).json()['name']
            req2 = self.xyz.get(
                f'https://graph.facebook.com/me/friends?fields=summary&limit=0&access_token={self.token_eaab}',
                cookies=self.cookie,
            ).json()['summary']['total_count']
            clear()
            print('Login Sebagai %s\n'%(req1))
        except Exception as e:
            self.insert_cookie()
    def insert_cookie(self):
        print('\nCookie Invalid!')
        time.sleep(2)
        clear()
        print('Apabila Akun A2F On, Pergi Ke')
        print('https://business.facebook.com/business_locations')
        print('Untuk Memasukkan Kode Autentikasi')
        ciko = input('Masukkan Cookie : ')
        self.token_eaag = self.generate_token_eaag(ciko)
        self.token_eaab = self.generate_token_eaab(ciko)
        try:os.mkdir("login")
        except:pass
        open('login/cookie.json','w').write(ciko)
        open('login/token_eaag.json','w').write(self.token_eaag)
        open('login/token_eaab.json','w').write(self.token_eaab)
        self.cek_cookies()
    def generate_token_eaag(self,cok):
        url = 'https://business.facebook.com/business_locations'
        req = self.xyz.get(url,cookies={'cookie':cok})
        return re.search('(\["EAAG\w+)', req.text)[1].replace('["', '')
    def generate_token_eaab(self,cok):
        url = 'https://www.facebook.com/adsmanager/manage/campaigns'
        req = self.xyz.get(url,cookies={'cookie':cok})
        set = re.search('act=(.*?)&nav_source',str(req.content))[1]
        nek = f'{url}?act={set}&nav_source=no_referrer'
        roq = self.xyz.get(nek,cookies={'cookie':cok})
        return re.search('accessToken="(.*?)"',str(roq.content))[1]

class main_dump:
    # --> Trigger
    def __init__(self):
        self.xyz         = requests.Session()
        self.token_eaag  = open('login/token_eaag.json','r').read()
        self.token_eaab  = open('login/token_eaab.json','r').read()
        self.cookie      = {'cookie':open('login/cookie.json','r').read()}
        self.pilih()
    # --> Menu Dump
    def pilih(self):
        print('[ Pilih Interaksi Berdasar ]')
        print('[1] React')
        print('[2] Comment')
        print('[3] React + Comment')
        xb = input('Pilih : ')
        print('')
        if   xb in ['1','01','a']: self.pilih2(); self.friendlist(); self.dump(); dump_react();         self.sortir(); unfriend()
        elif xb in ['2','02','b']: self.pilih2(); self.friendlist(); self.dump(); dump_comment();       self.sortir(); unfriend()
        elif xb in ['3','03','c']: self.pilih2(); self.friendlist(); self.dump(); dump_react_comment(); self.sortir(); unfriend()
        else: exit('\nIsi Yang Benar !\n')
    def pilih2(self):
        print('[ Pilih Privasi Post ]')
        print('[1] Semua')
        print('[2] Publik')
        print('[3] Teman')
        print('[4] Hanya Saya')
        xc = input('Pilih : ')
        print('')
        if   xc in ['1','01','a']: self.privacy = 'ALL'         # Semua Privasi
        elif xc in ['2','02','b']: self.privacy = 'EVERYONE'    # Publik
        elif xc in ['3','03','c']: self.privacy = 'ALL_FRIENDS' # Teman
        elif xc in ['4','04','d']: self.privacy = 'SELF'        # Hanya Saya
        else: exit('\nIsi Yang Benar !\n')
    def tempo(self):
        print('[ Postingan Setelah ]')
        print('Format : Tgl-Bln-Thn')
        print('Contoh : 29-10-2022')
        self.tempo = int(input(''))
        print('')
    # --> Execute Dump
    def dump(self):
        global tamp1
        self.tamp1 = []
        tamp1 = self.tamp1
        url = f'https://graph.facebook.com/me/posts?fields=id,created_time,privacy&limit=10000&access_token={self.token_eaag}'
        req = self.xyz.get(url,cookies=self.cookie).json()
        self.tamp1.extend(
            x
            for x in req['data']
            if self.privacy != 'ALL'
            and self.privacy == 'ALL_FRIENDS'
            and x['privacy']['value'] == 'ALL_FRIENDS'
            or self.privacy != 'ALL'
            and self.privacy != 'ALL_FRIENDS'
            and self.privacy == 'EVERYONE'
            and x['privacy']['value'] == 'EVERYONE'
            or self.privacy != 'ALL'
            and self.privacy != 'ALL_FRIENDS'
            and self.privacy != 'EVERYONE'
            and self.privacy == 'SELF'
            and x['privacy']['value'] == 'SELF'
            or self.privacy == 'ALL'
        )
        print(f'Mendapatkan {len(tamp1)} Postingan')
    # --> Dump Friendlist
    def friendlist(self):
        self.tamp3 = []
        url = f'https://graph.facebook.com/me/friends?fields=id,name&limit=5000&access_token={self.token_eaab}'
        req = self.xyz.get(url,cookies=self.cookie).json()
        try:
            for y in req['data']:
                try:
                    if y['id'] + '|' + y['name'] not in self.tamp3:
                        self.tamp3.append(y['id']+'|'+y['name'])
                except Exception as e:continue
        except Exception as e:pass
        print(f'Mendeteksi {len(self.tamp3)} Teman')
    # --> Sortir ID
    def sortir(self):
        global tamp3
        tamp3 = self.tamp3
        for z in tamp2:
            try:self.tamp3.remove(z)
            except Exception as e:pass
        print('Mendeteksi %s Teman Yg Tidak Pernah Berinteraksi\n'%(str(len(self.tamp3))))

class dump_react:
    def __init__(self):
        global tamp2
        self.tamp2       = []
        tamp2            = self.tamp2
        self.xyz         = requests.Session()
        self.token_eaag  = open('login/token_eaag.json','r').read()
        self.token_eaab  = open('login/token_eaab.json','r').read()
        self.cookie      = {'cookie':open('login/cookie.json','r').read()}
        for x in tamp1:
            url = f"https://graph.facebook.com/{x['id']}/reactions?limit=10000&access_token={self.token_eaab}"
            self.main_dump(url)
        print('')
    def main_dump(self,url):
        req = self.xyz.get(url,cookies=self.cookie).json()
        try:
            for y in req['data']:
                try:
                    if y['id'] + '|' + y['name'] not in self.tamp2:
                        self.tamp2.append(y['id']+'|'+y['name'])
                        print('\rMendeteksi %s Interaksi'%(str(len(tamp2))),end='')
                        sys.stdout.flush()
                except Exception as e:continue
        except Exception as e:pass

class dump_comment:
    def __init__(self):
        global tamp2
        self.tamp2       = []
        tamp2            = self.tamp2
        self.xyz         = requests.Session()
        self.token_eaag  = open('login/token_eaag.json','r').read()
        self.token_eaab  = open('login/token_eaab.json','r').read()
        self.cookie      = {'cookie':open('login/cookie.json','r').read()}
        for x in tamp1:
            url = f"https://graph.facebook.com/{x['id']}/comments?limit=10000&access_token={self.token_eaab}"
            self.main_dump(url)
        print('')
    def main_dump(self,url):
        req = self.xyz.get(url,cookies=self.cookie).json()
        try:
            for y in req['data']:
                try:
                    if y['from']['id'] + '|' + y['from']['name'] not in self.tamp2:
                        self.tamp2.append(y['from']['id']+'|'+y['from']['name'])
                        print('\rMendeteksi %s Interaksi'%(str(len(tamp2))),end='')
                        sys.stdout.flush()
                except Exception as e:continue
        except Exception as e:pass

class dump_react_comment:
    def __init__(self):
        global tamp2
        self.tamp2       = []
        tamp2            = self.tamp2
        self.xyz         = requests.Session()
        self.token_eaag  = open('login/token_eaag.json','r').read()
        self.token_eaab  = open('login/token_eaab.json','r').read()
        self.cookie      = {'cookie':open('login/cookie.json','r').read()}
        for x in tamp1:
            url = f"https://graph.facebook.com/{x['id']}/reactions?limit=10000&access_token={self.token_eaab}"
            self.main_dump1(url)
        for x in tamp1:
            url = f"https://graph.facebook.com/{x['id']}/comments?limit=10000&access_token={self.token_eaab}"
            self.main_dump2(url)
        print('')
    def main_dump1(self,url):
        req = self.xyz.get(url,cookies=self.cookie).json()
        try:
            for y in req['data']:
                try:
                    if y['id'] + '|' + y['name'] not in self.tamp2:
                        self.tamp2.append(y['id']+'|'+y['name'])
                        print('\rMendeteksi %s Interaksi'%(str(len(tamp2))),end='')
                        sys.stdout.flush()
                except Exception as e:continue
        except Exception as e:pass
    def main_dump2(self,url):
        req = self.xyz.get(url,cookies=self.cookie).json()
        try:
            for y in req['data']:
                try:
                    if y['from']['id'] + '|' + y['from']['name'] not in self.tamp2:
                        self.tamp2.append(y['from']['id']+'|'+y['from']['name'])
                        print('\rMendeteksi %s Interaksi'%(str(len(tamp2))),end='')
                        sys.stdout.flush()
                except Exception as e:continue
        except Exception as e:pass

class unfriend:
    def __init__(self):
        self.loop = 0
        self.cookie = {'cookie':open('login/cookie.json','r').read()}
        for fg in tamp3:
            id   = fg.split('|')[0]
            name = fg.split('|')[1]
            url = f'https://mbasic.facebook.com/removefriend.php?friend_id={id}'
            self.scrap1(url,id,name)
    def scrap1(self,url,id,name):
        with requests.Session() as xyz:
            req = bs(xyz.get(url,cookies=self.cookie).content,'html.parser')
            fom = req.find('form',{'method':'post'})
            dat = {
                'fb_dtsg': re.search(
                    'name="fb_dtsg" type="hidden" value="(.*?)"', str(fom)
                )[1],
                'jazoest': re.search(
                    'name="jazoest" type="hidden" value="(.*?)"', str(fom)
                )[1],
                'confirm': 'Konfirmasi',
            }
            nek = f"https://mbasic.facebook.com{fom['action']}"
            pos = xyz.post(nek,data=dat,cookies=self.cookie)
            if '<Response [200]>' in str(pos):
                self.loop += 1
                print('\r[Dihapus] %s | %s          '%(id,name))
            else:
                print('\r[ Gagal ] %s | %s          '%(id,name))
            print('\rBerhasil Menghapus %s Teman'%(str(self.loop)),end='')
            sys.stdout.flush()

if __name__=='__main__':
    clear()
    start()
    login()
    akhir()
