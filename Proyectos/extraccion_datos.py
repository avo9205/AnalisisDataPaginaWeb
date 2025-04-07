import requests
from lxml import html
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

# variables
count = 1
dicDataH = {'tipo':[],'genero':[],'studios':[],'idiomas':[],'episodios':[],'duracion':[],'emitido':[],'estado':[],'gustados':[],'nombre':[]}

# Beautifulsoup variables
url = 'https://hentaijk.com/'
#user-agent dentificacion de busquedas como un navedor
headers = {
	"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/666 Safari/537.36"
}


# =========Inicio de programa

while True:
	
	try:
	 
		# obtenemos el html de la pagina
		print('comprobacion de datos')
		res = requests.get(url+'directorio/'+str(count), headers = headers)
			
	except:
		
		print('Error en la solicitud!!')
		break

	else:
		if res.status_code == 200:
			print('inicio Extraccion Pagina: ', count)
			# incio de la lista de la pagina
			listaH = []
			# obtener info de la pagina
			Hsoup = BeautifulSoup(res.text, 'html.parser')
			
			#obtenemos la data 
			Hlist = Hsoup.select('script')
			Hlist = Hlist[3].text
			# print(Hlist)
			# filtramos la data para obtemer los nombres de los H
			Hdict = re.compile(r'"slug":"([\w\-]*?)"')
			Hvar = Hdict.findall(Hlist)
			
			# guardamos en una lista para su busqueda
			
			for v in Hvar:
				# v = v.replace('"slug":','')
				listaH.append(v)
				# print('porcentaje pagina {count}: ','{c}%')
				
			print(listaH, len(listaH))
			if listaH == []:
				print('Termino')
				break
			
			else:
				
				for l in range(len(listaH)):
						
					# ==============
					# pagina entrada	
					res = requests.get(url+listaH[l], headers = headers)
					Hsoup2 = BeautifulSoup(res.content, 'html.parser')

					# data de la pagina info
					pageDataH = Hsoup2.select('ul')
					pageDataH = pageDataH[9].text
					# data de la pagina likes 
					pageDataH2 = Hsoup2.select('div > a > span', class_ = 'anime__details__btn pc')
					pageDataH2 = pageDataH2[0].text
					# print(pageDataH)
					
					# busqueda data pagina info
					infoH = re.compile(r"(\w+:\s*[\s\S]*?)(?=\s*\w+:|$)") #revisar regex para aprender
					infoH = infoH.findall(pageDataH)

					# filtra la palabra Calidad para evitar errores en la busqueda
					infoH = list(filter(lambda x: not re.search(r'Calidad|Demografia', x, re.IGNORECASE), infoH))
					
					# insertar datos faltantes gustados,nombre
					infoH.append('Gustados:'+ pageDataH2) 	#gustado
					infoH.append('Nombre:'+ listaH[l])	#nombre
						
					# print(infoH)
					# print('infoH',len(infoH))
					
					if infoH == []:
						print('Termino')
						break	
					else:		
						# insetar datos en el diccionario y limpieza de datos
						infocount = 0
						for i in range(len(list(dicDataH.keys()))):
								
							# any retorna un True
							if any(list(dicDataH.keys())[i].capitalize() in p for  p in infoH):

								list(dicDataH.values())[i].append(infoH[infocount].replace(list(dicDataH.keys())[i].capitalize()+':','').replace(' ','').strip())
								infocount += 1
								
							else:
								list(dicDataH.values())[i].append(None)

									
						print('porcentaje:',l)
					
				print(dicDataH) 	
				count += 1

		else:
			print('No se pudo acceder a la pagina!!')
			break				


print('salimos')

df = pd.DataFrame(dicDataH)
df.to_csv('ListaH.csv',index = False)














# Forma de buscar en beautiful soup
# sigH = Hsoup.find_all('div' , class_='navigation')
# print(sigH)
# if sigH == []:
# 	print('final')
# 	break
# else:	
# 	for sigH in divs:
# 		a_tag = sigH.find('a', rel='nofollow')
# 		if a_tag:
# 			print(a_tag.text)