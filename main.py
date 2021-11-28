# Import librairies
import os, shutil
from exif import Image
from functions import is_img, exif_collect

def pictures_sort(folder):
  files = os.listdir(folder) # On liste tout les éléments se trouvant dans le dossier

  for i in range (len(files)): # Parcout de l'entiereté des fichiers
    file = files[i]
    file_path = f'{folder}\{file}'

    with open(file_path, 'rb') as img_file:
      img = Image(img_file)

    if is_img(img) == True:
      img_data = exif_collect(img, file)

      os.rename(f'{img_data.get("name")}', f'{img_data.get("location")}_{img_data.get("date")}_{i}.{img_data.get("format")}')
    
    # else: #envoyer le fichier dans un dossier avec tout ce qui n'est pas une photo puis retrier les éléments déplacer (dossier à trouver et à renvoyer être trier -> récursivité)
    #   shutil.move(file_path, f'{folder}\others')
    #   return pictures_sort(f'{folder}\others')

    img_file.closed

  return 'All files are sort !'



##############################################################################
# Instruction
##############################################################################

folder = input('Copy paste link of your pictures folder : ')

pictures_sort(folder)

# os.mkdir(f'{folder}/others') # On crée un dossier qui va contenir tout ce qui n'est pas une image