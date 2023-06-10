import urllib.request
import re
import random
from bs4 import BeautifulSoup
import threading

# dichiarazione della lista degli useragents per evitare che il sito ci blocchi per le numerose richieste
useragents=["AdsBot-Google ( http://www.google.com/adsbot.html)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0) Asus;Galaxy6",
			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
			"Mozilla/4.0 (PDA; PalmOS/sony/model prmr/Revision:1.1.54 (en)) NetFront/3.0",
			"Mozilla/4.0 (PSP (PlayStation Portable); 2.00)",
			"Mozilla/4.1 (compatible; MSIE 5.0; Symbian OS; Nokia 6600;452) Opera 6.20 [en-US]",
			"Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)",
			"Mozilla/4.8 [en] (Windows NT 5.1; U)",
			"Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)",
			"Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1",
			"Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1",
			"Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.9a1) Gecko/20060702 SeaMonkey/1.5a",
			"Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1  (KHTML, Like Gecko) Version/6.0.0.141 Mobile Safari/534.1",
			"Mozilla/5.0 (compatible; bingbot/2.0  http://www.bing.com/bingbot.htm)",
			"Mozilla/5.0 (compatible; Exabot/3.0;  http://www.exabot.com/go/robot) ",
			"Mozilla/5.0 (compatible; Googlebot/2.1;  http://www.google.com/bot.html)",
			"Mozilla/5.0 (compatible; Konqueror/3.3; Linux 2.6.8-gentoo-r3; X11;",
			"Mozilla/5.0 (compatible; Konqueror/3.5; Linux 2.6.30-7.dmz.1-liquorix-686; X11) KHTML/3.5.10 (like Gecko) (Debian package 4:3.5.10.dfsg.1-1 b1)",
			"Mozilla/5.0 (compatible; Konqueror/3.5; Linux; en_US) KHTML/3.5.6 (like Gecko) (Kubuntu)",
			"Mozilla/5.0 (compatible; Konqueror/3.5; NetBSD 4.0_RC3; X11) KHTML/3.5.7 (like Gecko)",
			"Mozilla/5.0 (compatible; Konqueror/3.5; SunOS) KHTML/3.5.1 (like Gecko)",
			"Mozilla/5.0 (compatible; Konqueror/4.1; DragonFly) KHTML/4.1.4 (like Gecko)",
			"Mozilla/5.0 (compatible; Konqueror/4.1; OpenBSD) KHTML/4.1.4 (like Gecko)",
			"Mozilla/5.0 (compatible; Konqueror/4.2; Linux) KHTML/4.2.4 (like Gecko) Slackware/13.0",
			"Mozilla/5.0 (compatible; Konqueror/4.3; Linux) KHTML/4.3.1 (like Gecko) Fedora/4.3.1-3.fc11",
			"Mozilla/5.0 (compatible; Konqueror/4.4; Linux 2.6.32-22-generic; X11; en_US) KHTML/4.4.3 (like Gecko) Kubuntu",
			"Mozilla/5.0 (compatible; Konqueror/4.4; Linux) KHTML/4.4.1 (like Gecko) Fedora/4.4.1-1.fc12",
			"Mozilla/5.0 (compatible; Konqueror/4.5; FreeBSD) KHTML/4.5.4 (like Gecko)",
			"Mozilla/5.0 (compatible; Konqueror/4.5; NetBSD 5.0.2; X11; amd64; en_US) KHTML/4.5.4 (like Gecko)",
			"Mozilla/5.0 (compatible; Konqueror/4.5; Windows) KHTML/4.5.4 (like Gecko)",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
			"Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/5.0)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; WOW64; Trident/5.0)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)",
			"Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html)",
			"Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
			"Mozilla/5.0 (en-us) AppleWebKit/525.13 (KHTML, like Gecko; Google Web Preview) Version/3.1 Safari/525.13",
			"Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
			"Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
			"Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
			"Mozilla/5.0 (iPad; U; CPU OS 4_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5",
			"Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_0 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5A347 Safari/525.200",
			"Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16",
			"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/531.22.7",
			"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; da-dk) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
			]

# urls vari
nurls = ["https://www.my-proxy.com/free-socks-4-proxy.html", "https://www.my-proxy.com/free-socks-5-proxy.html",
		"https://socks-list.blogspot.com/", "https://sock5us.blogspot.com/", "https://sockslist.blogspot.com/",
	        "http://www.aliveproxy.com/high-anonymity-proxy-list/", "http://www.aliveproxy.com/anonymous-proxy-list/",
		"http://www.aliveproxy.com/fastest-proxies/", "http://www.aliveproxy.com/us-proxy-list/", "http://www.aliveproxy.com/gb-proxy-list/",
		"http://www.aliveproxy.com/fr-proxy-list/", "http://www.aliveproxy.com/de-proxy-list/", "http://www.aliveproxy.com/jp-proxy-list/",
		"http://www.aliveproxy.com/ca-proxy-list/", "http://www.aliveproxy.com/ru-proxy-list/", "http://www.aliveproxy.com/proxy-list-port-80/",
		"http://www.aliveproxy.com/proxy-list-port-81/", "http://www.aliveproxy.com/proxy-list-port-3128/", "http://www.aliveproxy.com/proxy-list-port-8000/",
		"http://www.aliveproxy.com/proxy-list-port-8080/", "http://webanetlabs.net/publ/24", "http://www.proxz.com/proxy_list_high_anonymous_0.html",
		"http://www.proxz.com/proxy_list_anonymous_us_0.html", "http://www.proxz.com/proxy_list_uk_0.html", "http://www.proxz.com/proxy_list_ca_0.html",
		"http://www.proxz.com/proxy_list_cn_ssl_0.html", "http://www.proxz.com/proxy_list_jp_0.html", "http://www.proxz.com/proxy_list_fr_0.html",
		"http://www.proxz.com/proxy_list_port_std_0.html", "http://www.proxz.com/proxy_list_port_nonstd_0.html", "http://www.proxz.com/proxy_list_transparent_0.html",
		"http://www.proxylists.net/", "https://www.my-proxy.com/free-proxy-list.html","https://www.my-proxy.com/free-elite-proxy.html",
		"https://www.my-proxy.com/free-anonymous-proxy.html", "https://www.my-proxy.com/free-transparent-proxy.html","https://jffjdjkbfek.000webhostapp.com/proxy.txt",
		"https://raw.githubusercontent.com/SonuModder1/Githg/main/proxylets.txt",
		"https://cyber-hub.net/proxy/http.txt",
		"https://24h-sock.blogspot.com/2012/04/socks-proxy-list.html", "https://socks5-lists.blogspot.com/"]

def proxyget(url): # scarica proxy da altri siti
	try:
		req = urllib.request.Request(url) # url corrispondente a una serie di urls impostati sotto.
		req.add_header("User-Agent", random.choice(useragents)) # aggiunge uno user agent a caso dalla lista sopra
		sourcecode = urllib.request.urlopen(req, timeout = 10) # scaricamento sourcecode pagina + timeout impostato a 10
		for line in sourcecode :
				ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}):(?:[\d]{1,5})", str(line)) # cerca ip proxy
				ipf = list(filter(lambda x: x if not x.startswith("0.") else None, ip)) # evita di cattutrare anche ip inutili
				if ipf: # se trova ip prosegue
					for x in ipf:
						ipfinal = x # se lo prende ipfinal
						out_file = open("proxy.txt","a")
						while True:
							out_file.write(x+"\n") # scrive ip uno per uno nel file proxy.txt
							out_file.close()
							break # appena finisce ferma il ciclo
	except:
		print("\nAn error occurred, skipping to the next website.")

def proxyget2(url): # lo dice il nome, questa funzione scarica i proxies
	try:
		req = urllib.request.Request((url))       # qua impostiamo il sito da dove scaricare.
		req.add_header("User-Agent", random.choice(useragents)) # siccome il format del sito e' identico sia
		sourcecode = urllib.request.urlopen(req, timeout=10)    # per free-proxy-list.net che per socks-proxy.net,
		part = str(sourcecode.read())                           # imposto la variabile urlproxy in base a cosa si sceglie.
		part = part.split("<tbody>")          # va a fare scraping nel sito
		part = part[1].split("</tbody>")      # per trovare la parte
		part = part[0].split("<tr><td>")      # che riguarda i proxies
		proxies = ""
		for proxy in part:
			proxy = proxy.split("</td><td>")  # una volta trovata li salva
			try:
				proxies=proxies + proxy[0] + ":" + proxy[1] + "\n"
			except:
				pass
		out_file = open("proxy.txt","a")      # e li scrive nel file, aperto come a, per non sovrascrivere proxy gia presenti all'interno
		out_file.write(proxies)
		out_file.close()
	except:
		print("\nAn error occurred, skipping to the next website.")

def blogspotget(url, word): # anche questa funzione scarica proxy pero' dai siti blogspot
	try:
		soup = BeautifulSoup(urllib.request.urlopen(url))
		for tag in soup.find_all(word): # bs4, dopo aver processato la source, trova la parte riguardante le proxylist
			try:
				links = tag.a.get("href")				# prende i link delle proxylist
			except:
				pass
			result = urllib.request.urlopen(links)	# finalmente apre i link trovati
			for line in result :
				ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}):(?:[\d]{1,5})", str(line)) # cerca gli ip:porta nelle pagine
				if ip: # se ha trovato gli ip prosegue
					for x in ip:
						out_file = open("proxy.txt","a") # scrittura singolo ip nella proxy.txt
						while True:
							out_file.write(x+"\n") # scrive ip uno per uno nel file proxy.txt
							out_file.close()
							break # il ciclo si ferma non appena ha finito
	except:
		print("\nAn error occurred, skipping to the next website.")

def proxylist(): # funzione per la creazione della proxylist
	global proxies
	print ("\nChecking for duplicates...")
	proxies = open("proxy.txt").readlines() # la lista txt presenta doppioni, quindi:
	proxiesp = []
	for i in proxies:
		if i not in proxiesp: # se il proxy non è già presente in proxiesp
			proxiesp.append(i) # li aggiunge in proxiesp
	filepr = open("proxy.txt", "w") # prima cancella contenuto del file
	filepr.close()
	filepr = open("proxy.txt", "a") # dopo lo apre in modalità a per non sovrascrivere i proxy
	for i in proxiesp:
		filepr.write(i)             # e scrive
	print("Current IPs in proxylist: %s" % (len(open("proxy.txt").readlines()))) # per vedere quante lines (e quindi quanti proxy) ci sono nel file
	print ("\nProxylist Updated!\n")

def proxycheckerinit():
	global out_file
	candidate_proxies = open("proxy.txt").readlines() # vede gli attuali proxy "candidati" lol
	filedl = open("proxy.txt", "w") # prima cancella contenuto
	filedl.close()
	out_file = open("proxy.txt", "a") # e poi lo apre non in riscrivibile
	threads = [] # crea una lista che ci servirà dopo
	for i in candidate_proxies:
		t = threading.Thread(target=proxychecker, args=[i]) # crea un thread per proxy per velocizzare
		t.start() # e lo avvia
		threads.append(t) # e lo inserisce nella lista precedente

	for t in threads: # per tutti i threads che hanno finito il loro lavoro,
		t.join()      # questo li fa aspettare che tutti abbiano finito

	out_file.close()  # chiude il file precedentemente aperto
	print("\n\nCurrent IPs in proxylist: %s\n" % (len(open("proxy.txt").readlines()))) # quando finisce tutto printa la quantità di proxy FINALE

def proxychecker(i):
	proxy = 'http://' + i
	proxy_support = urllib.request.ProxyHandler({'socks' : proxy}) # compone la richiesta con il proxy
	opener = urllib.request.build_opener(proxy_support)
	urllib.request.install_opener(opener)
	req = urllib.request.Request(("http://www.google.com"))			# compone la richiesta a google
	req.add_header("User-Agent", random.choice(useragents))			# aggiunge useragent random per fare sembrare più realistica la req
	try:
		urllib.request.urlopen(req, timeout=60)						# apre il sito
		print ("%s works!\n\n" % proxy) # se funziona printa "it works"
		out_file.write(i)				# e lo scrive nel file.
	except:
		print ("%s does not respond.\n\n" % proxy) # altrimenti dice che non risponde


def main(): # funzione effettiva del programma.
	try:
		out_file = open("proxy.txt","w") # prima di tutto cancella il contenuto di proxy.txt
		out_file.close()

		print ("\nDownloading from socks-proxy.net in progress...")
		url = "https://www.socks-proxy.net/"
		proxyget2(url) # manda url alla funzione
		print("Current IPs in proxylist: %s" % (len(open("proxy.txt").readlines()))) # printa la lunghezza attuale del file, che sarebbe il numero di proxy

		print ("\nDownloading from blogspot in progress...\n")
		url = "https://2freesocks5list.blogspot.com/"
		word = "strong"
		blogspotget(url,word)
		print("Current IPs in proxylist: %s" % (len(open("proxy.txt").readlines())))

		print ("\nDownloading from various mirrors in progress...")
		for position, url in enumerate(nurls):
			proxyget (url)
			print("Completed downloads: (%s/%s)\nCurrent IPs in proxylist: %s" % (position+1, len(nurls), len(open("proxy.txt").readlines())))

		proxylist() # dopo esegue questa funzione che setta meglio la lista

		print("\n")
		while True:
			choice = input("\nDo you want to check the socks? [Y/n] > ") # scelta di quello che vuole l'utente
			if choice == 'Y' or choice == 'y' or choice == 'yes' or choice == 'Yes' or choice == '': # se si vuole checkare starta funzione del check
				proxycheckerinit()
				break
			if choice == 'N' or choice == 'n' or choice == 'no' or choice == 'No': # altrimenti esce
				exit(0)
			else: # se scrivi male input
				print ("Please write correctly.")
	except:
		print ("\n\nAn error occurred.")




if __name__ == '__main__':

	while True:
		choice = input("\nDo you want to download socks? [Y/n] > ")
		if choice == 'Y' or choice == 'y' or choice == 'yes' or choice == 'Yes' or choice == '': # se si vuole scaricare i proxy va in main()
			main()
			break
		if choice == 'N' or choice == 'n' or choice == 'no' or choice == 'No': # altrimenti checka solo i proxy
			proxycheckerinit()
			break
		else: # se scrivi male richiede l'input
			print ("Please write correctly.")
