from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
import httplib2, socket


SHEETS_DISCOVERY_URL='https://sheets.googleapis.com/$discovery/rest?version=v4'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


class GoogleSpreadsheet:
    def __init__(self, credentials_json_data, spreadsheet_id, range_name, data=None, major_dimension="ROWS",
                 value_input_option="RAW"):
        self.credentials_json_data = credentials_json_data
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        self.data = data
        self.major_dimension = major_dimension
        self.value_input_option = value_input_option

    def get_sheets_service(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.credentials_json_data, scopes=SCOPES)
        http = credentials.authorize(httplib2.Http(timeout=120))

        return discovery.build(
            'sheets',
            'v4',
            http=http,
            discoveryServiceUrl=SHEETS_DISCOVERY_URL
        )

    def update(self):
        final_payload = {
            "range": self.range_name,
            "majorDimension": self.major_dimension,
            "values": self.data
        }

        service = self.get_sheets_service()

        try:
            result = service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id, range=self.range_name,
                valueInputOption=self.value_input_option,
                body=final_payload
            ).execute()

            response = {
                "data": result
            }

        except (httplib2.HttpLib2Error, socket.error) as ex:
            response = {
                "error": {
                    "code": 408,
                    "message": "Timeout error. Acessing google spreadsheet api."
                }
            }

        except (HttpError) as ex:
            response = {
                "error": {
                    "code": 400,
                    "message": ex
                }
            }

        return response

    def get(self):
        service = self.get_sheets_service()

        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=self.range_name,
                majorDimension=self.major_dimension
            ).execute()['values']

            response = {
                "data": result
            }

        except (httplib2.HttpLib2Error, socket.error) as ex:
            response = {
                "error": {
                    "code": 408,
                    "message": "Timeout error. Acessing google spreadsheet api."
                }
            }

        except (HttpError) as ex:
            response = {
                "error": {
                    "code": 400,
                    "message": ex
                }
            }

        return response


def main(method_name="", credentials_json_data=None, spreadsheet_id="", range_name="", data=None,
         major_dimension="ROWS", value_input_option="RAW"):
    google_spreadsheet = GoogleSpreadsheet(
        credentials_json_data=credentials_json_data,
        spreadsheet_id=spreadsheet_id,
        range_name=range_name,
        data=data,
        major_dimension=major_dimension,
        value_input_option=value_input_option
    )

    if method_name:
        response = getattr(google_spreadsheet, method_name)()
    else:
        response = {
            "error": {
                "code": 404,
                "message": "Can't find method {}.".format(method_name)
            }
        }
    print response
    return response


if __name__ == '__main__':
    import argparse
    import json
    import ast

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--method_name',
        help="Name of the spreadsheet method. Methods available: 'update, get'"
    )
    parser.add_argument(
        '--spreadsheet_id',
        help="Id of the spreadsheet."
    )
    parser.add_argument(
        '--credentials_json_data',
        help="Crendential from google appengine service account. Pass it as json converted as string"
    )
    parser.add_argument(
        '--range_name',
        help="range of the spreadhsheet to get, update, append etc."
    )
    parser.add_argument(
        '--data',
        help="data of the spreadhsheet to update, append, bold etc."
    )
    parser.add_argument(
        '--major_dimension',
        help="Not required",
        default="ROWS"
    )
    parser.add_argument(
        '--value_input_option',
        help="Not required",
        default="RAW"
    )

    args = parser.parse_args()
    args.data = ast.literal_eval(args.data) if args.data else None
    args.credentials_json_data = json.loads(args.credentials_json_data)

    main(**vars(args))


# run in terminal
'''

json_data='{
  "type": "service_account",
  "project_id": "symph-git-hooks",
  "private_key_id": "2d257d0cbf2dfbd0d1f21a5dc952246d88f6dc17",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCZoJXP4zzCIiSO\nxuf4QAypH38mb6rKnTnuP7gIH2a7LNbinhKczc1g/woykIKq6bn+h4VkBfWnYELZ\n7Y0cwtuQsWPv4boLZYiL5a0SQTOa0NhPGGrkPAjSHz8OVmInPiPldIl32h2SpbYh\n2sVPgZd792i0J45XKmojBQ8YDVbHpqU2ljKS+TUGVSM5OoE+wlNbKAHrqlm9vWIf\nVk3PWW9KpHb30dT2FJ3RGPkDWwwEr/q5OTLW/siAFH/N4ox0+/9eCyrJCER92Gg9\nimHRmUrbPLnNPF15F2ubIIgwtLCmaesjtccp8EkmFkKKOTpDWY+hJHevyP7jFFxh\nwSBuVdJ3AgMBAAECggEAJW3Bci+72tR0sbB2Tb5VF1NMKDImm0ypE4nErX3xCoNH\nK1k10aw2cH5SnrUkkL13CjM8ZX0qN4g1YWEF807qLZt6bLRDHomzNdpUS1FFYF+n\ng8XALTEPORpRw416RnNWTY4R+/hRIixrbl4dmlxJavOBN/s3K7dyumt+HO8LCIMJ\ntDLqbMDIujvCbb85y0F8YFQ9tCvCmNHe749ZbC6WgCaZg+eapnjuovsuDRXF/ieP\nSrCWIcf8XqUZitUCeAsNUcxvdWZiR/XkKt9f/yPy5BrF5Vy5k6lqA70dMswFFhIP\nje4tErsqk9Mu9F2vA/ORAJpGorT4ZX/tg2u/dwaWOQKBgQDINy5cH37SvgUp01FJ\nC/YK7dYulhzRRdbNPOAVq3G8PHGonEPXpiRL3aTH4OQsFvt2Q6V/d0/jCp7b+6CU\nfRqe7xrZgg6kCuh0sgx2f6kJVPK9a4FqP+lfIYSPfNna06B+rXCQlzr4mYPjMcCM\nfA5DmrSdO7DUvrjIkg31oRu8NQKBgQDEbmSCREoVqQABtgzBk/xncB2SvxM4dDzX\n6XazWIqd1PVz8GdbYIYNGzwfr7fvh6VTst+Sb5olqUE9qOIup/7Ko4f4XEkbl+w+\n41gp1z0BeLr8pvN70aNysw2+P1bJ7Ob+orflzMrPXu3w2lhVgZrm4sZhRp1p7hi8\nPbsKkBNxewKBgQCDwxz1b5zNIFTRk8p44jBIPQGpowzQBMA6TYfDexLcqIK8Tiqv\nrx1P+EvLZwuCoJVY3Wf7HRAsAP9PEqg5UKPGWOE4p8ju2Gbm9Y4SJi2egJNHaYq/\n29O/0ZUlwSq2QnPrKkVcQsqCdLVBParUSYgxoYyftXrIZ8O/667YKfDQyQKBgBR/\njJ+Hbs+51hVXoRcmUUWeDof8xo2ym5LQeyGWEMkNqxuRL8f6V6LQf8KyvJgTaK5G\nUUxftw9NDVDY6dmCkHUnAY5qWvq1LOMXKGEdY/FeXuz0ox39r3fNtZZv16e0wBo8\ncsJZT6S6PExRDLzHjJmheqA2FUEzpoMmUfl1NYI3AoGBAIUP1K/5pudurRAm2b2T\nMeieXEWBxi1THY50IHX+OAQ2RCB36xXqptPfF7jTTj4gon0OjWVDEYmOpTgK97M2\nuJ3XcmOIWxAMRgtYKaAdv4SUWEWtzzk7VwbJEz6BEIYpeObM71bbWpXVIbAS9EUs\nxTv7fRBRVPBz6jvXhNdUi67g\n-----END PRIVATE KEY-----\n",
  "client_email": "symph-git-hooks@appspot.gserviceaccount.com",
  "client_id": "112209603279888659603",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/symph-git-hooks%40appspot.gserviceaccount.com"
}'

python main.py "update" $json_data "1GlTG4aDsIp2C7VdNYlfeJMYxtWo7QHciJjnceW_fl7Y" "Sheet1A1" "[['hello']]"

'''