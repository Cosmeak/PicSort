# Import librairies
import os, shutil
from exif import Image
from geopy.geocoders import Nominatim

#check if the file is an img
def is_img(file):
  return file.has_exif 


# Collect exif we want to have and place it in dict
def exif_collect(img, file): 

  name = file

  file_format = file.split('.') # On sépare le nom du format dans une liste
  file_format = file_format[-1] # On ne garde que le dernier élément de la liste, qui correspond au format
  
  date = img.get('datetime_original')

  if date != None:
    date = date.split()
    date = date[0].split(':')
    date = "-".join(date)
  
  location = [img.get('gps_longitude'), img.get('gps_latitude')]
  
  for i in range(len(location)):
    if location[i] == None:
      location = 'location-inconnu'

  if location == list:
    location = "-".join(location)

  img_data = {
    'name': file,
    'format': file_format,
    'date': date,
    'location': location
  }
  return img_data


# Get location with latitude and longitude 
def get_location(latidute, longitude):
  geoLoc = Nominatim(user_agent="GetLoc") 
  location = geoLoc.reverse(latidute, longitude)
  location = location.split("")
  location = [location[-1], location[0]] # location [-1] = pays - location[0] = ville 
  location = "_".join(location)
  return location


#Sort function
def pictures_sort(folder):
  os.chdir(folder)
  files = os.listdir(folder) # On liste tout les éléments se trouvant dans le dossier

  for i in range (len(files)): # Parcout de l'entiereté des fichiers
    file = files[i]
    file_path = f'{folder}\{file}'

    with open(file_path, 'rb') as img_file:
      img = Image(img_file)

    if is_img(img) == True:
      img_data = exif_collect(img, file)

      os.rename(f'{img_data.get("name")}', f'{img_data.get("location")}_{img_data.get("date")}_{i}.{img_data.get("format")}')

      print('File sort !')
    
    # else: #envoyer le fichier dans un dossier avec tout ce qui n'est pas une photo puis retrier les éléments déplacer (dossier à trouver et à renvoyer être trier -> récursivité)
    #   shutil.move(file_path, f'{folder}\others')
    #   return pictures_sort(f'{folder}\others')

    img_file.closed

  print('All files are sort !')
  return



##############################################################################
# Instruction
##############################################################################

folder_src = input('Copy paste link of your pictures folder : ')

pictures_sort(folder_src)

# os.mkdir(f'{folder}\others') # On crée un dossier qui va contenir tout ce qui n'est pas une image
# os.mkdir(f'{folder}\need_to_sort') # On crée un dossier qui va contenir les dossiers qui se trouver dans le dossier source et qui doivent être trier aussi

