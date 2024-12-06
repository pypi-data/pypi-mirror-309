import sys, re, argparse
from os import path, walk, mkdir
from concurrent.futures import ThreadPoolExecutor


class M3U:
    def __init__(self):
        """A Cool & Simple Python M3U Playlist Maker/Parser & XPSF To M3U Playlist Converter."""
        self.done = []
        self.hd = path.join(path.expanduser('~'), 'Desktop', 'M3U_Playlists')
    
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
        if l:self.__write(l,self.__valid(o,d),1,0)
    
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
        r = r'(,[^/].*%s.*)\n(.*)'%(t)
        if g:
            r = r'(group-title=".*%s.*)\n(.*)'%(g)
            t = g
        o = self.__valid(t, d, c=c)
        l = self.__read(f, r)
        if l:
            url = l[0][1].split('/')[2]
            if self.done.count(url) >= h:return
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
        if ml:self.__write(ml,self.__valid('Created',dd),0,1)
    
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
        :param a: String Filename To Check & Edit If Exists In Output Folder.
        :param d: String Output Directory Path To Check & Rename Playlist If It Exists.
        :param c: Integer To Start Incrementing From If Playlist Exists (Default = 0).
        :param e: String Playlist File Extension (Default = .m3u).
        """
        a = path.join(d, a)
        while path.exists(f'{a}{e}'):
            c += 1
            a = f'{a}_{c}'
        return f'{a}{e}'
    
    def main(self, args: dict):
        """
        Execute Create/Parse/Convert Tasks From Argparse NameSpace Arguments Specified.
        :param args: Argparse NameSpace Arguments.
        """
        fa = self.__flist(args.file)
        if fa:
            if args.output:self.hd = args.output
            if not path.exists(self.hd):mkdir(self.hd)
            if args.create:self.__create(fa, self.hd, tt=args.title, ss=args.season, ep=args.episode, am=args.amount)
            else:
                c = 0
                a = '.m3u' if args.parse else '.xpsf'
                with ThreadPoolExecutor(args.threads) as exec:
                    for m in self.__list(fa, e=a):
                        c += 1
                        if args.convert:exec.submit(self.__convert(m, self.hd))
                        elif args.parse:
                            exec.submit(self.__search(m, self.hd, t=str(args.title), g=str(args.group), h=args.hosts, c=c))
        else:print("\nNo File(s) Found, Please Specifiy A Valid File(s) Or Directory Containing Them.")

def cli_main():
    usage = ('Examples:\n'
             '    wudz-m3u -f "C:\\Playlists" -t "Billions S05" -p\n'
             '    wudz-m3u -f "C:\\Titles.txt,C:\\Links.txt" -c (Always Specify Titles Before Links For Playlist Creation)\n'
             '    wudz-m3u -f "C:\\Links.txt" -t "House Of Cards" -s 2 -a 10 -c\n'
             '    wudz-m3u -f "C:\\file.xpsf" -v -o C:\\Users\n')
    parser = argparse.ArgumentParser(description="A Cool & Simple Python M3U Playlist Maker/Parser & XPSF To M3U Playlist Converter.",
                                     epilog=usage,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f", "--file", type=str, default=None, required=True, help="File(s) Or Directory With Files To Be Used (e.g a.txt | c:\\Tv | 'a.txt,b.txt').")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output Directory (e.g C:\M3U | Default = 'M3U_Playlists' Folder In Current User's Desktop Directory.")
    parser.add_argument("-g", "--group", type=str, default='', help="Parse M3U Playlist(s) For Group-Title (e.g SERIES | HIP Radio | ADULT).")
    parser.add_argument("-t", "--title", type=str, default='', help="Title(s) To Create In Or Parse From M3U Playlist (e.g 'House Of Cards' | Billions).")
    parser.add_argument("-s", "--season", type=int, default=1, help="Season # To Start Incrementing From (e.g 2 | 3 | Default = 1).")
    parser.add_argument("-e", "--episode", type=int, default=1, help="Episode # To Start Incrementing From (e.g 3 | 10 | Default = 1).")
    parser.add_argument("-a", "--amount", type=int, default=0, help="Amount Of Episodes Per Season (e.g 10 | 20 | Default = 0).")
    parser.add_argument("-u", "--hosts", type=int, default=1, help="Amount Of Playlists To Create Per Host (e.g 1 | 5 | Default = 1).")
    parser.add_argument("-x", "--threads", type=int, default=20, help="Amount Of Threads To Execute With (e.g 10 | 30 | Default = 20).")
    parser.add_argument("-p", "--parse", action="store_true", help="Parse Playlists For Title Or Group-Title & Create M3U Playlists.")
    parser.add_argument("-c", "--create", action="store_true", help="Create Playlist From File(s) &Or Arguments Specified.")
    parser.add_argument("-v", "--convert", action="store_true", help="Convert XPSF To M3U Playlist(s).")
    try:
        pl=M3U()
        pl.main(parser.parse_args())
    except:sys.exit(1)
