import sys, re, argparse, requests
from colorama import Fore, init
from time import sleep
from os import path, walk, mkdir, name, system
from concurrent.futures import ThreadPoolExecutor
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
init()


class M3U:
    def __init__(self):
        """A Cool & Simple Python M3U Playlist Checker/Downloader/Maker/Parser & XPSF To M3U Playlist Converter."""
        self.vc = 0
        self.done = []
        self.hd = path.join(path.expanduser('~'), 'Desktop', 'M3U_Playlists')
        self.vf = path.join(self.hd, 'm3u_valid.txt')
        self.red=Fore.LIGHTRED_EX
        self.blue=Fore.LIGHTBLUE_EX
        self.green=Fore.LIGHTGREEN_EX
        self.yellow=Fore.LIGHTYELLOW_EX
        self.white=Fore.LIGHTWHITE_EX
        self.cyan=Fore.LIGHTCYAN_EX
    
    def __flist(self, fn: str) -> list:
        """
        Return List From String Containing Single Or Multiple Arguments Split By Comma.
        :param fn: String Containing Single Or Multiple File Arguments Seperated By Comma ','.
        """
        return [i for i in fn.split(',') if path.exists(i)]
    
    def __list(self, l: list, e: str=None) -> list:
        """
        Return Playlist Files As List.
        :param l: List Containing Playlist Filename(s) &Or Name(s) Of Folders Containing Playlist Files.
        :param e: Optional String Of Playlist File Extension To Retrieve (e.g .m3u | .xpsf).
        """
        ol = []
        for i in l:
            if path.isfile(i):ol.append(i)
            elif path.isdir(i) and e:ol.extend([path.join(str(a),y) for a,b,c in walk(i) for y in c if y.endswith(e)])
        return ol
    
    def __convert(self, fn: str, d: str):
        """
        Parse XPSF Playlist Using Regex & Create M3U Playlist Of Same Filename With Parsed Data.
        :param fn: String XPSF Playlist Filename To Be Converted To M3U Playlist.
        :param d: String Output Direcotry Path.
        """
        o = path.splitext(fn)[0]
        l = self.__read(fn, '<location>(.*)</location>\n\t\t\t<title>(.*)</title>')
        if l:
            self.vc += 1
            self.__write(l,self.__valid(o,d),1,0)
    
    def __data(self, f: str) -> str:
        """
        Returns Data Read From Specified File As String.
        :param f: String Filename Containing Data To Be Read
        """
        return open(f, 'r', encoding='ISO-8859-1').read()
    
    def __read(self, f: str, r: str) -> list:
        """
        Returns Parsed Regex Data From Specified File As List.
        :param f: String Filename Containing Data To Be Read & Parsed.
        :param r: Regex String To Parse Data For.
        """
        d = self.__data(f)
        l = re.findall(r, d, re.IGNORECASE)
        return l
    
    def __search(self, f: str, d: str, t: str='', g: str='', h: int=1, c: int=0):
        """
        Parse M3U Playlist For Title Or Group-Title & Create M3U Playlist With Parsed Data.
        :param f: String Playlist File To Be Parsed.
        :param d: String Output Direcotry Path.
        :param t: Optional String Title To Search Playlist For.
        :param g: Optional String Group-Title To Search Playlist For.
        :param h: Optional Integer Amount Of Playlist Per Host To Create (Default = 1).
        :param c: Optional Integer Increment To Create Playlist Filename Resulting In No Duplicates (Default = 0).
        """
        r = r'(,.*%s.*)\n(.*)'%(t)
        if g:
            r = r'(group-title=".*%s.*)\n(.*)'%(g)
            t = g
        o = self.__valid(t, d, c=c)
        l = self.__read(f, r)
        if l:
            url = l[0][1].split('/')[2]
            if self.done.count(url) >= h:return
            self.vc += 1
            self.done.append(url)
            self.__write(l,o,0,1,c='p')
    
    def __create(self, fa: list, dd: str, tt: str='', ss: int=1, ep: int=1, am: int=0):
        """
        Create M3U Playlist From Arguments & File(s) Specified.
        :param fa: List Containing File(s) To Be Used.
        :param dd: String Output Direcotry Path.
        :param tt: Optional String Title For Links In Created Playlist (Default=None).
        :param ss: Optional Integer Season To Increment Titles From (Default=1).
        :param ep: Optional Integer Episode To Increment Titles From (Default=1).
        :param am: Optional Integer Amount Of Episodes Per Season (Default=0).
        """
        ml = []
        da = self.__data(fa[0])
        if len(fa) == 2:
            db = self.__data(fa[1])
            ml = [i for i in zip(da.splitlines(),db.splitlines())]
        elif not tt:ml = re.findall(r'(.*?)\n(.*?)\n', da+'\n')
        else:
            tl = []
            el = da.splitlines()
            ae = len(el)
            if am > 0:ae = am
            while len(tl) < len(el):
                for i in range(ep,ae+1):
                    if len(str(i)) == 1:i = '0'+str(i)
                    tl.append(f'{tt} S0{ss} E{i}')
                ep = 1
                ss += 1
            ml = [x for x in zip(tl,el)]
        if ml:
            self.vc += 1
            self.__write(ml,self.__valid('Created',dd),0,1)
    
    def __write(self, l: list, o: str, a: int, b: int, c: str=None):
        """
        Create Playlist File.
        :param l: List Of Tuples Containing Links & Titles In Either Order To Create M3U Playlist With.
        :param o: String Playlist Filename.
        :param a: Integer Specifying Tuple Index To Be Written As Title.
        :param b: Integer Specifying Tuple Index To Be Written As Link.
        :param c: Optional String To Specify Data Format To Be Written In Playlist.
        """
        with open(o, 'a', encoding='utf-8') as fw:
            fw.write('#EXTM3U\n')
            for i in l:
                if c:fw.write(f'#EXTINF:{i[a]}\n{i[b]}\n')
                else:fw.write(f'#EXTINF:,{i[a]}\n{i[b]}\n')
    
    def __valid(self, a: str, d: str, c: int=0, e: str='.m3u') -> str:
        """
        Check, Renames (With Incremented Number If Already Exists) & Returns Playlist File Path To Be Created.
        :param a: String Filename Without File Extension To Check & Edit If Exists In Output Folder.
        :param d: String Output Directory Path To Check & Rename Playlist If It Exists.
        :param c: Integer To Start Incrementing From If Playlist Exists (Default = 0).
        :param e: String Playlist File Extension (Default = .m3u).
        """
        a = path.join(d, a)
        while path.exists(f'{a}{e}'):
            c += 1
            if a[-1].isdigit():
                c = int(a[-1]) + 1
                a = f'{a[:-1]}{c}'
            else:a = f'{a}_{c}'
            
        return f'{a}{e}'
    
    def __check(self, u: str, d: bool=False):
        """
        Check Then Save Valid M3U Link To 'm3u_valid.txt' &Or Download M3U Url As Local Playlist File.
        :param u: M3u Url Link To Download.
        :param d: Bool Specifying Download Playlist (Default=False).
        """
        try:
            um = u.split('/')
            hd = {
"Host": um[2],
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:76.0) Gecko/20100101 Firefox/76.0",
"Accept": "*/*",
"Accept-Language": "de,en-gb;q=0.7,en;q=0.3",
"Cache-Control": "no-cache",
"Accept-Encoding": "gzip, deflate"
            }
            res = requests.get(u, headers=hd, timeout=5, verify=False, stream=d)
            if res.status_code == 200:
                assert int(res.headers['Content-Length'])>0            #Verify Playlist Has Content
                self.vc += 1
                c = um[2].split('.')[0],'m3u'
                if len(um[-1].split('.'))==2:c = um[-1].split('.')
                if res.headers.get('Content-Disposition'):
                    a = res.headers['Content-Disposition']
                    c = re.search(r'filename="(.*?)"', a).group(1).split('.')
                fn = self.__valid(c[0], self.hd, e=f'.{c[1]}')
                if d:
                    with open(fn, 'wb') as fw:
                        for c in res.iter_content(chunk_size=1024):    #Download Playlist Content In 1 MB Chunks
                            fw.write(c)
                with open(self.vf, 'a', encoding='utf-8') as fd:
                    fd.write(f'{u}\n')
        except:pass
    
    def main(self, args: dict):
        """
        Execute Check/Create/Download/Parse/Convert Tasks From Argparse NameSpace Arguments Specified.
        :param args: Argparse NameSpace Arguments.
        """
        ml = []
        print(self.cyan+"[*]Executing Tasks Hang On...")
        if args.legit:
            ml = [args.legit]
            if path.isfile(args.legit):ml = self.__data(args.legit).splitlines()
        elif args.file:
            a = '.m3u' if args.parse else '.xpsf'
            fa = self.__flist(args.file)
            ml = self.__list(fa, e=a)
        if args.output:self.hd = args.output
        if not path.exists(self.hd):mkdir(self.hd)
        if args.create:self.__create(fa, self.hd, tt=args.title, ss=args.season, ep=args.episode, am=args.amount)
        elif ml:
            c = 0
            with ThreadPoolExecutor(args.threads) as exec:
                for m in ml:
                    try:
                        c += 1
                        if args.legit:exec.submit(self.__check(m, args.download))
                        elif args.convert:exec.submit(self.__convert(m, self.hd))
                        elif args.parse:
                            exec.submit(self.__search(m, self.hd, t=args.title, g=args.group, h=args.hosts, c=c))
                    except KeyboardInterrupt:break
                    except:pass
        clear_screen()
        if self.vc != 0:
            if args.create:print(self.blue+f"\n{self.vc} Playlists Created In {self.hd}"+self.white)
            elif args.legit:
                print(self.blue+f"\n{self.vc} Valid Playlists Saved To {self.vf}"+self.white)
                if args.download:print(self.blue+f"\n{self.vc} Playlists Downloaded To {self.hd}"+self.white)
            elif args.convert:print(self.blue+f"\n{self.vc} Playlists Converted & Saved To {self.hd}"+self.white)
            elif args.parse:print(self.blue+f"\n{self.vc} Playlists Parsed & Saved To {self.hd}"+self.white)
        else:print(self.red+"\n...Nothing There Fam, Input Valid Arguments..."+self.white)
    
    def slow_print(self, doc: str, sp: float=0.0005):
        """
        Print String By Speed In Seconds Less Is Faster.
        :param doc: String To Be Printed
        :param sp:  Speed To Print String `e.g 0.0001 or 0.0005 used`
        """
        for d in doc:
            sys.stdout.write(self.green+d)
            sleep(sp)

def clear_screen():
    """Clear Command Line Screen."""
    if name=='nt':system('cls')
    else:system('clear')

def cli_main():
    """
    Wuddz-M3U Entry Point Executing Specified Argparse NameSpace Arguments.
    """
    clear_screen()
    doc="""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░██╗░░░░░░░██╗██╗░░░██╗██████╗░██████╗░███████╗░░░░░░███╗░░░███╗██████╗░██╗░░░██╗░░░░░░
░░░░██║░░██╗░░██║██║░░░██║██╔══██╗██╔══██╗╚════██║░░░░░░████╗░████║╚════██╗██║░░░██║░░░░░░
░░░░╚██╗████╗██╔╝██║░░░██║██║░░██║██║░░██║░░███╔═╝█████╗██╔████╔██║░█████╔╝██║░░░██║░░░░░░
░░░░░████╔═████║░██║░░░██║██║░░██║██║░░██║██╔══╝░░╚════╝██║╚██╔╝██║░╚═══██╗██║░░░██║░░░░░░
░░░░░╚██╔╝░╚██╔╝░╚██████╔╝██████╔╝██████╔╝███████╗░░░░░░██║░╚═╝░██║██████╔╝╚██████╔╝░░░░░░
░░░░░░╚═╝░░░╚═╝░░░╚═════╝░╚═════╝░╚═════╝░╚══════╝░░░░░░╚═╝░░░░░╚═╝╚═════╝░░╚═════╝░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
[*]Descr:     WUDDZ-M3U IS A PYTHON M3U PLAYLIST CHECKER/DOWNLOADER/MAKER/PARSER & XPSF TO
              M3U PLAYLIST CONVERTER.                                                     
[*]Email:     wuddz_devs@protonmail.com                                                   
[*]Github:    https://github.com/wuddz-devs/wuddz-m3u                                     
[*]Donation:                                                                              
    Btc   ->  bc1qa7ssx0e4l6lytqawrnceu6hf5990x4r2uwuead                                  
    Erc20 ->  0xbF4d5309Bc633d95B6a8fe60E6AF490F11ed2Dd1                                  
    Ltc   ->  LdbcFiQVUMTfc9eJdc5Gw2nZgyo6WjKCj7                                          
    Tron  ->  TY6e3dWGpqyn2wUgnA5q63c88PJzfDmQAD                                          
    Doge  ->  DFwLwtcam7n2JreSpq1r2rtkA48Vos5Hgm                                          
"""
    us=r"""
[*]Examples:
wudz-m3u -f "C:\M3U" -t "Billions S05" -p   [Parse Playlists In 'c:\m3u' For Billions Season 5]
wudz-m3u -f "C:\titles.txt,C:\urls.txt" -c  [Create Playlist From 'titles' & 'urls' Files]
                                            (Always Titles Before Links For Playlist Creation)
wudz-m3u -f "C:\file.xpsf" -v -o C:\Users   [Convert Xpsf To M3u Playlist In 'c:\users']
wudz-m3u -l "C:\valid.txt" -d               [Download Valid M3u Urls In File To Output Folder]
wudz-m3u -l "C:\m3u.txt"                    [Save Valid M3u Urls To 'm3u_valid.txt' In Output Folder]
"""
    pl=M3U()
    pl.slow_print(doc)
    print(pl.yellow+us+pl.white)
    parser = argparse.ArgumentParser(description="A Cool & Simple Python M3U Playlist Checker/Downloader/Maker/Parser & XPSF To M3U Playlist Converter.")
    parser.add_argument("-f", "--file", type=str, default='', help="File(s) Or Directory With Files To Be Used (e.g a.txt | c:\\Tv | 'a.txt,b.txt').")
    parser.add_argument("-o", "--output", type=str, default='', help="Output Directory (e.g C:\\M3U | Default = 'M3U_Playlists' Folder On User's Desktop.")
    parser.add_argument("-g", "--group", type=str, default='', help="Parse M3U Playlist(s) For Group-Title (e.g SERIES | HIP Radio | ADULT).")
    parser.add_argument("-t", "--title", type=str, default='', help="Title(s) To Create In Or Parse From M3U Playlist (e.g 'House Of Cards' | Billions).")
    parser.add_argument("-s", "--season", type=int, default=1, help="Season # To Start Incrementing From (e.g 2 | 3 | Default = 1).")
    parser.add_argument("-e", "--episode", type=int, default=1, help="Episode # To Start Incrementing From (e.g 3 | 10 | Default = 1).")
    parser.add_argument("-a", "--amount", type=int, default=0, help="Amount Of Episodes Per Season (e.g 10 | 20 | Default = 0).")
    parser.add_argument("-u", "--hosts", type=int, default=1, help="Amount Of Playlists To Create Per Host (e.g 1 | 5 | Default = 1).")
    parser.add_argument("-x", "--threads", type=int, default=20, help="Amount Of Threads To Execute With (e.g 10 | 30 | Default = 20).")
    parser.add_argument("-l", "--legit", type=str, default='', help="Check M3U Url Or File With M3U Urls & Save Legit Urls To 'm3u_valid.txt' In Output Folder.")
    parser.add_argument("-d", "--download", action="store_true", help="Download Legit Specified Playlist(s) In '-l' Argument.")
    parser.add_argument("-p", "--parse", action="store_true", help="Parse Playlists For Title Or Group-Title & Create M3U Playlists.")
    parser.add_argument("-c", "--create", action="store_true", help="Create Playlist From File(s) &Or Arguments Specified.")
    parser.add_argument("-v", "--convert", action="store_true", help="Convert XPSF To M3U Playlist(s).")
    if len(sys.argv)>1:pl.main(parser.parse_args())
