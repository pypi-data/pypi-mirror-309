import pandas_gbq

def write_source(SourceName , df ,dataset , SOURCE_FOLDER, project_id):
    match SourceName:

      case 'asn_info':
        df.to_excel(f'{SOURCE_FOLDER}/01_raw/asn_info.xlsx')
        df.to_parquet(f'{SOURCE_FOLDER}/01_raw/asn_info.parquet')
        pandas_gbq.to_gbq(df, f'{dataset}.asn_info', project_id=project_id , if_exists='replace')

      case 'ip_info':
        df.to_excel(f'{SOURCE_FOLDER}/01_raw/ip_info.xlsx')
        df.to_parquet(f'{SOURCE_FOLDER}/01_raw/ip_info.parquet')
        pandas_gbq.to_gbq(df, f'{dataset}.ip_info', project_id=project_id , if_exists='replace')

      case 'asn_agg':
        df.to_excel(f'{SOURCE_FOLDER}/02_intermediate/asn_agg.xlsx')
        df.to_parquet(f'{SOURCE_FOLDER}/02_intermediate/asn_agg.parquet')
        pandas_gbq.to_gbq(df, f'{dataset}.asn_agg', project_id=project_id , if_exists='replace')