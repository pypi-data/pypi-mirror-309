import os
try :
    import requests
    import base64
    import json

    class Github:
        def __init__(self, token, Owner, Repo):
            self.token = token
            self.Owner = Owner
            self.Repo = Repo

        def new_file(self, file_name, file_content, message = "Ajout d'un nouveau fichier"):
            if isinstance(file_content, str):
                # Convertir une chaîne en octets si nécessaire
                file_content = file_content.encode('utf-8')

            contenu_base64 = base64.b64encode(file_content).decode('utf-8')
            url = f'https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{file_name}'  # Correction ici
            headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            data = {
                'message': message,
                'content': contenu_base64  # Encodage base64 du contenu
            }
            response = requests.put(url, json=data, headers=headers)
            if response.status_code == 201:
                print('Fichier créé avec succès !')
                return "True"
            else:
                print(f"Erreur : {response.status_code}, {response.text}")
                return "False"

        def new_file_content(self, file_name, file_content, message = "Mise à jour du fichier"):
            url_get = f'https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{file_name}'  # Correction ici
            headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            response = requests.get(url_get, headers=headers)
            if response.status_code == 200:
                file_data = response.json()
                sha = file_data['sha']  # On récupère le SHA pour la modification

                # Encodage du nouveau contenu en base64
                if isinstance(file_content, str):
                    # Convertir une chaîne en octets si nécessaire
                    file_content = file_content.encode('utf-8')

                contenu_base64 = base64.b64encode(file_content).decode('utf-8')

                # URL pour mettre à jour le fichier
                url_put = f'https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{file_name}'  # Correction ici

                data = {
                    'message': message,
                    'content': contenu_base64,
                    'sha': sha  # On inclut le SHA pour identifier le fichier à modifier
                }

                # Requête pour mettre à jour le fichier
                response = requests.put(url_put, json=data, headers=headers)

                if response.status_code == 200:
                    print('Fichier modifié avec succès !')
                else:
                    print(f"Erreur : {response.status_code}, {response.text}")
            else:
                print(f"Erreur lors de la récupération du fichier : {response.status_code}, {response.text}")
        def del_file(self, file_name, message = "suppression d'un fichier"):
            url_get = f'https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{file_name}'
            headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            response = requests.get(url_get, headers=headers)
            if response.status_code == 200:
                file_data = response.json()
                sha = file_data['sha']
                url_delete = f'https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{file_name}'

                data = {
                    'message': message,
                    'sha': sha  # On inclut le SHA pour identifier le fichier à supprimer
                }
                response = requests.delete(url_delete, json=data, headers=headers)
                if response.status_code == 200:
                    print('Fichier supprimé avec succès !')
                else:
                    print(f"Erreur : {response.status_code}, {response.text}")
            else:
                print(f"Erreur lors de la récupération du fichier : {response.status_code}, {response.text}")
        def create_folder(self, folder_name, file_name = "File.txt", file_content = "",message = "création d'un nouveau dossier"):
            url = f'https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{folder_name}/{file_name}'
            headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            data = {
                'message': message,
                'content': base64.b64encode(file_content.encode()).decode()  # Contenu encodé en base64
            }
            response = requests.put(url, json=data, headers=headers)
            if response.status_code == 201:
                print('Dossier et fichier créés avec succès !')
            else:
                print(f"Erreur : {response.status_code}, {response.text}")
        def del_folder(self, folder_name, message="Suppression du dossier et de ses fichiers"):
            headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }

            # URL pour obtenir la liste des fichiers dans le dossier
            url_list_files = f'https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{folder_name}'

            # Récupérer la liste des fichiers dans le dossier
            response = requests.get(url_list_files, headers=headers)

            if response.status_code == 200:
                files_data = response.json()
                for file_info in files_data:
                    if file_info['type'] == 'file':  # Vérifier si l'élément est un fichier
                        file_path = file_info['path']
                        sha = file_info['sha']

                        # URL pour supprimer le fichier
                        url_delete = f'https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{file_path}'
                        data = {
                            'message': message,
                            'sha': sha
                        }
                        delete_response = requests.delete(url_delete, json=data, headers=headers)

                        if delete_response.status_code == 200:
                            print(f'Fichier {file_path} supprimé avec succès !')
                        else:
                            print(f"Erreur lors de la suppression de {file_path}: {delete_response.status_code}, {delete_response.text}")
            else:
                print(f"Erreur lors de la récupération des fichiers: {response.status_code}, {response.text}")
        def GetFileContent(self, file_path):
            url = f"https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{file_path}"

            # Ajouter le token d'authentification dans les headers
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }

            # Faire la requête à l'API
            response = requests.get(url, headers=headers)

            # Vérifier que la requête a réussi
            if response.status_code == 200:
                # Décoder le contenu du fichier (base64)
                content = base64.b64decode(response.json()["content"]).decode()
                return content  # Affiche le contenu du fichier
            else:
                print(f"Erreur {response.status_code}: {response.text}")

        def GetFileSize(self, file_path, branch = "main"):
            url = f"https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{file_path}?ref={branch}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("size")  # Taille en octets
                else:
                    print(f"Erreur: {response.status_code} - {response.json().get('message')}")
                    return None
            except Exception as e:
                print(f"Erreur lors de la requête : {e}")
                return None

    if __name__ == "__main__":
        token = Github("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", "Grivy16", "Juste-Suite")
        print(token.GetFileContent("test.txt"))

except ModuleNotFoundError :
        os.system(f'start requirements.md')