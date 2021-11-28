# Import librairies
import os, shutil

folder = input('Copy paste link of your pictures folder')

files = os.listdir(folder) # On liste tout les éléments se trouvant dans le dossier

os.mkdir (f'{folder}/others') # On crée un dossier qui va contenir tout ce qui n'est pas une image

for i in range (len(files)): # Parcout de l'entiereté des fichiers
  file = files[i]
  file_path = f'{folder}/{file}'

  with open(file_path, 'rb') as img_file:
    img = Image(img_file)

  if is_img(img) == true:
    img_data = exif_collect(img)

  else:
    #envoyer le fichier dans un dossier avec tout ce qui n'est pas une photo 
    shutil.move(file_path, f'{folder}/others/{file}')