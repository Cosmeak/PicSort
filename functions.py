# Import librairies
from exif import Image

# Files contain all functions use for the script main.py 


#check if the file is an img
def is_img(file):
  return img.has_exif 


# Collect exif we want to have and place it in dict
def exif_collect(): 
  img_data = {
    'name': file,
    'date': img.get('datetime_original'),
    'location': [img.get('gps_longitude'), img.get('gps_latitude')]
  }
  return img_data