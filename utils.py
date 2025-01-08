import unicodedata, re

def clean_str(chaine):
    # Normaliser les caractères pour supprimer les accents
    chaine = unicodedata.normalize('NFD', chaine)
    chaine = ''.join(c for c in chaine if unicodedata.category(c) != 'Mn')
    
    # Enlever les caractères spéciaux non désirés (garder lettres, chiffres et espaces)
    chaine = re.sub(r'[^a-zA-Z0-9\s]', '', chaine)
    
    # Supprimer les espaces superflus
    chaine = re.sub(r'\s+', ' ', chaine).strip()
    
    return chaine