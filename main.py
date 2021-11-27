import os
from exif import Image

folder = input('Copy paste link of your pictures folder')

files = os.listdir(folder) #On liste tout les éléments se trouvant dans le dossier

for i in range (len(files)): #parcout de l'entiereté des fichiers
  img_path = f'{folder}/{files[i]}'

  with open(img_path, 'rb') as img_file: #On crée une classe qui va nous servir à vérifier que le fichier est bien une image
    img = Image(img_file)

  if img.has_exif == true: #*On vérifie que le fichier et une image, si c'est le on récupère les données, sinon on va faire une boucle récursive qui va faire ouvrir le dossier si s'en ai un sinon déplacer ce fichier dans un dossier rebus

    #On va récupérer toutes les données exif de la photo qui nous intéresse et nous servirions à les trier plus tard
    img_name = files[i]
    datetime = img.get('datetime')
    datetime_digitized = img.get('datetime_digitized')
    datetime_original = img.get('datetime_original')
    place = [img.get('gps_longitude'), img.get(gps_latitude)]

    date = [

    ]
    #Il faut créer les dictionnaire puis append dedans les données exif que l'on vient de récuperer