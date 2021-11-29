# Import librairies
import exif
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
  
  for i in range (len(location)):
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
  location = {
    'country': location[0],
    'city': location[-1]
  }
  return location