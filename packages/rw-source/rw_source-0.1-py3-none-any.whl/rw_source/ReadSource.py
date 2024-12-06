import pandas as pd
import json
import requests


def get_asn(token):
  df = pd.DataFrame(columns=['name','nameLong','aka','asn','website','estimatedUsers'])
  asn_data = requests.get('https://stat.ripe.net/data/country-resource-list/data.json?resource=ua',
                 headers={"Content-Type ": "application/json"})

  list_of_asn = json.loads(asn_data.text)['data']['resources']['asn']

  for asn in list_of_asn:
    asn_info = requests.get(f"https://api.cloudflare.com/client/v4/radar/entities/asns/{asn}",
                 headers={"Authorization": f"Bearer {token}" ,
                          "Content-Type ": "application/json"})
    print(asn_info.status_code)
    if asn_info.status_code == 200:
      if 'asn' in json.loads(asn_info.text)['result']:
        asn_response = json.loads(asn_info.text)['result']['asn']
        new_row = [asn_response['name'],
               asn_response['nameLong'],
               asn_response['aka'],
               asn_response['asn'],
               asn_response['website'],
               asn_response['estimatedUsers']['estimatedUsers']]
        df.loc[len(df.index)] = new_row
        print(asn)

  return df

def get_ip():
  df = pd.DataFrame(columns=['asn' , 'start_ip' , 'end_ip'])

  asn_data = requests.get('https://stat.ripe.net/data/country-resource-list/data.json?resource=ua',
                 headers={"Content-Type ": "application/json"})
  list_of_asn = json.loads(asn_data.text)['data']['resources']['asn']

  for asn in list_of_asn:
    org_info = requests.get(f"https://rest.db.ripe.net/ripe/aut-num/AS{asn}.json")

    if org_info.status_code == 200:
      org = json.loads(org_info.text)['objects']['object'][0]['attributes']['attribute']

      for i in org:
        for j in i:
          if i[j] == 'org':
            ip_data = requests.get(f'https://rest.db.ripe.net/search.json?inverse-attribute=org&type-filter=inetnum&source=ripe&query-string={i["value"]}')
            if ip_data.status_code == 200:
              ip_address = json.loads(ip_data.text)['objects']['object'][0]['primary-key']['attribute'][0]['value']
              print(ip_address)
              new_row=[asn , ip_address.split(' ')[0] , ip_address.split(' ')[2]]
              df.loc[len(df.index)] = new_row

  return df

def Read_Source(SourceName:str, usecache:bool=False, renamed:bool=False , token=None)->pd.DataFrame:
  """
  Read_Source
  :SourceName: n
  :usecache: if true load datasource from cache parqeut file
  """

  match SourceName:

    case 'asn_info':
        df = get_asn(token)
        df.drop(columns='nameLong' , inplace=True)
        return df

    case 'ip_info':
        df = get_ip()
        df['asn'] = df['asn'].astype(int)
        return df


    case _ :
      raise ValueError(f"Unknow source name: {SourceName}")