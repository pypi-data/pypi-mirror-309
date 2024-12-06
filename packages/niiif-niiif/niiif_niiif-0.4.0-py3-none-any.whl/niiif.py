import requests
import json
import argparse
import sys
from tqdm import tqdm
from collections import defaultdict

MANIFEST_FILE_DESCRIPTION = 'IIIF manifest'

uploadsAPIHeaders = {
    'accept': 'application/json',
}

filesAPIHeaders = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

requiredStatementArgumentHelp = ("The IIIF requiredStatement property could be used to present copyright or "
                             "ownership statements, an acknowledgement of the owning and/or publishing "
                             "institution, or any other text that the publishing organization "
                             "deems critical to display to the user. Usage example: "
                             "-rslabel \"Attribution\" en "
                             "-rsvalue \"Provided by the Centre de recherche bretonne et celtique\" en "
                             "-rslabel \"Attribution\" fr "
                             "-rsvalue \"Mis à disposition par le Centre de recherche bretonne et celtique\" fr. "
                             "For more information, "
                             "please read https://iiif.io/api/presentation/3.0/#requiredstatement. For "
                             "examples, read https://samvera-labs.github.io/clover-iiif/docs/requiredStatement")

def process_args():
    parser = argparse.ArgumentParser(description="Creates JSON IIIF manifests for Nakala datas")
    parser.add_argument("-dataid", "--data_identifier", help="Nakala data identifier")
    parser.add_argument("-apikey", "--api_key", help="Nakala user API key")
    parser.add_argument("-behavior", "--behavior", help="IIIF manifests behaviors. For more information, "
                                                          "please read https://iiif.io/api/presentation/3.0/")
    parser.add_argument("-rslabel",
                        nargs=2,
                        action = "append",
                        metavar=("label", "label_BCP47_language_code"),
                        help=requiredStatementArgumentHelp)
    parser.add_argument("-rsvalue",
                        nargs=2,
                        action = "append",
                        metavar=("value", "value_BCP47_language_code"),
                        help=requiredStatementArgumentHelp)
    parser.add_argument("-label", "--label",
                        nargs=2,
                        metavar=("value", "BCP47_language_code"),
                        action="append",
                        help="IIIF label descriptive property. Repeatable parameter. Usage example: "
                             "-label \"Pomme\" fr "
                             "-label \"Apple\" en "
                             "-label \"Fruits\" fr "
                             "-label  \"Label without language\" none. "
                             "For more information about the IIIF label property, please read "
                             "https://iiif.io/api/presentation/3.0/#label.")
    args = parser.parse_args()
    if args.data_identifier is None:
        print('*** Usage error: -dataid or --data_identifier should be specified ')
        parser.print_usage()
        sys.exit(1)
    if args.api_key is None:
        print('*** Usage error: -apikey or --api_key should be specified ')
        parser.print_usage()
        sys.exit(1)
    if args.label is None:
        print('*** Usage error: At least one label and its BCP 47 language code should be specified ')
        parser.print_usage()
        sys.exit(1)
    if args.rsvalue is not None and args.rslabel is None:
        print('*** Usage error: The label of the IIIF requiredStatement property should be specified ')
        parser.print_usage()
        sys.exit(1)
    if args.rsvalue is None and args.rslabel is not None:
        print('*** Usage error: The value of the IIIF requiredStatement property should be specified ')
        parser.print_usage()
        sys.exit(1)
    return args


def get_data_metadata(apiKey, dataIdentifier):
    filesAPIHeaders['X-API-KEY'] = apiKey
    response = None
    try:
        # The response could be an error message
        response = requests.get('https://api.nakala.fr/datas/' + dataIdentifier, headers=filesAPIHeaders)
    except Exception as err:
        print(err)
    return response


def get_data_manifest_sha1_if_exists(dataMetadataJSON):
    files = dataMetadataJSON['files']
    manifest_sha1 = None
    for file in files:
        if file['name'] == 'metadata.json' and file['description'] == MANIFEST_FILE_DESCRIPTION:
            manifest_sha1 = file['sha1']
    return manifest_sha1


def delete_manifest(apiKey, dataIdentifier, sha1):
    response = None
    try:
        uploadsAPIHeaders['X-API-KEY'] = apiKey
        response = requests.delete('https://api.nakala.fr/datas/' + dataIdentifier + '/files/' + sha1,
                                   headers=uploadsAPIHeaders)
        if response.status_code == 204:
            print('Info : metadata.json file deleted for data id ' + dataIdentifier)
    except Exception as err:
        print(err)
    return response


def create_data_manifest(apiKey,
                         dataIdentifier,
                         behavior,
                         dataMetadataJSON,
                         required_statements_labels,
                         required_statements_values,
                         labels):
    """

    Parameters
    ----------

    apiKey: str
    dataIdentifier: str
    behavior: str
    dataMetadataJSON: dict
    required_statements_labels: list
        Ex. [["Attribution", en], ["Attribution", fr]]
        à partir du paramètre répétable -rslabel
        python -m niiif ... -rslabel "Attribution" en -rslabel "Attribution" fr
    required_statements_values: list
        Ex. [["Provided by the Centre de recherche bretonne et celtique", en],
        ["Mis à disposition par le Centre de recherche bretonne et celtique", fr]]
        à partir du paramètre répétable -rsvalue
        python -m niiif ... -rsvalue "Provided by the Centre de recherche bretonne et celtique" en
        -rsvalue "Mis à disposition par le Centre de recherche bretonne et celtique" fr
    labels: list
         Ex. [["Pomme", "fr"], ["Apple", "en"], ["Fruits", "fr"], ["Label sans langue", "none"]]
         à partir du paramètre répétable -label
         python -m niiif ... -label "Pomme" fr -label "Apple" en -label "Fruits" fr
         -label "Label sans langue" none

    Returns
    -------
    manifest: dict
    """
    # Attention les identifiants des documents peuvent être des DOI (10.34847/nkl.c1d1w5fj)
    # ou des Handle (11280/b4d935c2).
    # Cas d'un Carnet de Anatole Le Braz : ALBM1
    # https://nakala.fr/10.34847/nkl.c1d1w5fj
    # ID d'un des fichiers TIFF du carnet : 10.34847/nkl.c1d1w5fj/a79248c84cef396c1f2ddc57b7e028f90b4b2b1c
    # a79248c84cef396c1f2ddc57b7e028f90b4b2b1c est le SHA1
    # présent dans les résultats de la requête :
    # curl -X GET "https://api.nakala.fr/datas/10.34847%2Fnkl.c1d1w5fj/files" -H  "accept: application/json"
    # Renvoie (entre autres):
    #
    #   {
    #     "name": "CRBC_ALBM1_027.tif",
    #     "extension": "tif",
    #     "size": 12424178,
    #     "mime_type": "image/tiff",
    #     "sha1": "847ea669a1d7daf92208d31d4d95f4c0032b0754",
    #     "embargoed": "2021-04-29T00:00:00+02:00",
    #     "description": null,
    #     "humanReadableEmbargoedDelay": []
    #   }
    #
    # L'API Image de IIIF pour ce fichier TIFF est accessible depuis :
    # https://api.nakala.fr/iiif/10.34847/nkl.c1d1w5fj/a79248c84cef396c1f2ddc57b7e028f90b4b2b1c/full/max/0/default.jpg
    # https://api.nakala.fr/iiif/10.34847/nkl.c1d1w5fj/a79248c84cef396c1f2ddc57b7e028f90b4b2b1c
    # https://api.nakala.fr/iiif/10.34847/nkl.c1d1w5fj/a79248c84cef396c1f2ddc57b7e028f90b4b2b1c/info.json

    # 10.34847/nkl.37afk8kn
    # 10.34847/nkl.66bdx361
    # 10.34847/nkl.c1d1w5fj

    manifest = None
    filesAPIHeaders['X-API-KEY'] = apiKey

    try:
        canvases = []

        files = dataMetadataJSON['files']
        data_files_total_number = 0
        for file in files:
            if file['mime_type'] in {'image/tiff', 'image/jpeg'}:
                data_files_total_number += 1

        with tqdm(total=data_files_total_number) as pbar:
            for file in files:
                sha1 = file['sha1']
                if file['mime_type'] in {'image/tiff', 'image/jpeg'}:
                    # Pour récupérer la taille en pixel du fichier
                    fileMetadataJSON = None
                    width = 100
                    height = 100
                    try:
                        fileMetadata = requests.get("https://api.nakala.fr/iiif/" + dataIdentifier + "/" + str(sha1) +
                                                    "/info.json", headers=filesAPIHeaders)
                        fileMetadataJSON = fileMetadata.json()
                        width = fileMetadataJSON['width']
                        height = fileMetadataJSON['height']
                    except Exception as err:
                        print(err)
                    canvasURI = "https://api.nakala.fr/iiif/" + dataIdentifier + "/Canvas/" + str(sha1)
                    canvases.append(
                        {
                            "id": canvasURI,
                            "type": "Canvas",
                            "label": {"none": [file["name"]]},
                            "width": width,
                            "height": height,
                            "items": [
                                {
                                    "id": "https://api.nakala.fr/iiif/" + dataIdentifier +
                                          "/AnnotationPage/" + str(sha1),
                                    "type": "AnnotationPage",
                                    "items": [
                                        {
                                            "id": "https://api.nakala.fr/iiif/" + dataIdentifier +
                                                  "/Annotation/" + str(sha1),
                                            "type": "Annotation",
                                            "motivation": "painting",
                                            "target": canvasURI,
                                            "body": {
                                                "id": "https://api.nakala.fr/iiif/" + dataIdentifier + "/"
                                                      + str(sha1) + "/full/full/0/default.jpg",
                                                "type": "Image",
                                                "format": "image/jpeg",
                                                "width": width,
                                                "height": height,
                                                "service": [
                                                    {
                                                        "id": 'https://api.nakala.fr/iiif/' +
                                                              dataIdentifier + "/" + str(sha1),
                                                        "type": "ImageService3",
                                                        "profile": "level2"
                                                    }
                                                ]
                                            }
                                        }]
                                }],
                            "thumbnail": [
                                {
                                    "id": "https://api.nakala.fr/iiif/" + dataIdentifier + "/"
                                          + str(sha1) + "/full/full/0/default.jpg",
                                    "type": "Image",
                                    "service": [
                                        {
                                            "id": 'https://api.nakala.fr/iiif/' +
                                                  dataIdentifier + "/" + str(sha1),
                                            "type": "ImageService3",
                                            "profile": "level2",
                                        }
                                    ]
                                }
                            ],
                        })
                    pbar.set_postfix(file=file["name"], refresh=False)
                    pbar.update()

        # https://stackoverflow.com/a/5378250.
        label_property_values = defaultdict(list)
        for value, langcode in labels:
            label_property_values[langcode].append(value)

        # id devrait être modifié pour correspondre à l'URL de téléchargement du fichier metadata.json sur
        # Nakala (qui contient le SHA1 du fichier) mais il faudrait pourvoir modifier le fichier une fois déposé
        # sur Nakala, ce qui n'est évidemment pas possible.

        manifestData = {
            "@context": "http://iiif.io/api/presentation/3/context.json",
            "id": "https://api.nakala.fr/data/" + dataIdentifier,
            "type": "Manifest",
            "label": label_property_values,
            "items": canvases
        }

        # "requiredStatement": {
        #     "label": {"en": ["Attribution"]},
        #     "value": {"en": ["Provided by the Centre de recherche bretonne et celtique."]}
        # },
        if required_statements_labels is not None and required_statements_values is not None:
            requiredStatement_labels = defaultdict(list)
            for label, langcode in required_statements_labels:
                requiredStatement_labels[langcode].append(label)
            requiredStatement_values = defaultdict(list)
            for value, langcode in required_statements_values:
                requiredStatement_values[langcode].append(value)
            manifestData['requiredStatement'] = {"label": requiredStatement_labels,
                                                 "value": requiredStatement_values}

        if behavior == 'paged':
            manifestData['behavior'] = ["paged"]

        manifest = json.dumps(manifestData, indent=4)
    except Exception as err:
        print(f'create_data_manifest: {err}')
    return manifest


def upload_manifest_file(apiKey, dataIdentifier, manifest):
    # A FAIRE : Vérifier que le fichier n'existe pas déjà et le remplacer si nécessaire.
    files = {'file': ('metadata.json', manifest)}
    upload_file_api_url = 'https://api.nakala.fr/datas/uploads'
    uploadsAPIHeaders['X-API-KEY'] = apiKey
    filesAPIHeaders['X-API-KEY'] = apiKey
    try:
        upload_file_api_response = requests.post(upload_file_api_url, files=files, headers=uploadsAPIHeaders)
        if upload_file_api_response.status_code == 201:
            sha1 = upload_file_api_response.json()['sha1']
            add_file_api_url = 'https://api.nakala.fr/datas/' + dataIdentifier + '/files'
            data = {
                'sha1': sha1,
                'description': MANIFEST_FILE_DESCRIPTION
            }
            dataJSON = json.dumps(data)
            add_file_api_response = requests.post(add_file_api_url, headers=filesAPIHeaders, data=dataJSON)
            if add_file_api_response.status_code == 200:
                print('Manifest URL for a IIIF viewer : https://api.nakala.fr/data/' +
                      str(dataIdentifier) + '/' + str(sha1))
            else:
                print(add_file_api_response)
        else:
            print(upload_file_api_response)
    except Exception as err:
        print(f'upload_manifest_file: {err}')


def create_data_manifest_if_data_exists(apiKey,
                                        dataIdentifier,
                                        behavior,
                                        required_statements_labels,
                                        required_statements_values,
                                        labels):
    response = get_data_metadata(apiKey, dataIdentifier)
    if response.status_code == 200:
        dataMetadataJSON = response.json()
        manifest_sha1 = get_data_manifest_sha1_if_exists(dataMetadataJSON)
        if manifest_sha1 is not None:
            delete_manifest(apiKey, dataIdentifier, manifest_sha1)
        manifest = create_data_manifest(apiKey,
                                        dataIdentifier,
                                        behavior,
                                        dataMetadataJSON,
                                        required_statements_labels,
                                        required_statements_values,
                                        labels)
        if manifest is not None:
            upload_manifest_file(apiKey, dataIdentifier, manifest)
        else:
            print("The manifest could not be created")
    else:
        print(response.json()['message'])


def main():
    args = process_args()
    create_data_manifest_if_data_exists(args.api_key,
                                        args.data_identifier,
                                        args.behavior,
                                        args.rslabel,
                                        args.rsvalue,
                                        args.label)


if __name__ == '__main__':
    main()


