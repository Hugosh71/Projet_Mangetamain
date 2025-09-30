import pandas as pnd

class ExcelHandler:
    def __init__(self, file_path):
        """
        Initialise la classe avec le chemin du fichier Excel.
        """
        self.file_path = file_path
        self.data = None

    def read_excel(self, sheet_name=0):
        """
        Lit le fichier Excel et charge les données dans un DataFrame.
        """
        try:
            self.data = pd.read_excel(self.file_path, sheet_name=sheet_name, engine='openpyxl')
            print("Fichier Excel chargé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")

   
    def filter_data(self, column_name, value):
        """
        Filtre les données en fonction d'une colonne et d'une valeur.
        """
        if self.data is not None:
            self.data = self.data[self.data[column_name] == value]
            print(f"Données filtrées sur {column_name} = {value}.")
        else:
            print("Aucune donnée chargée. Veuillez lire un fichier Excel d'abord.")

    def display_data(self):
        """
        Affiche les données actuellement chargées.
        """
        if self.data is not None:
            print(self.data)
        else:
            print("Aucune donnée à afficher. Veuillez lire un fichier Excel d'abord.")
