from google.cloud import storage, bigquery 
import requests , json

project_id ='single-cycling-426112-e2'
bucket_name='gcsproject'
dataset= 'cleandata'
table_name = 'users_data' 

row_file ='row_data.json'
processed_file ='clean_data.json'           
def data_fetch() :
    api = requests.get("https://randomuser.me/api/?results=50")
  
    return api

def gcs_upload(api):
  
    client = storage.Client(project=project_id)
    bucket =client.bucket(bucket_name)
    blob =bucket.blob(row_file)
    blob.upload_from_string(json.dumps(api.json()), content_type="application/json")
    print("row file uploaded to GCS!")

def transform_data(api):

    if api.status_code == 200:
        data_results = api.json()['results']
        jsonl_data = ""
        
        for user_data in data_results:
            employee_data = {
                'name': f"{user_data['name']['first']} {user_data['name']['last']}",
                'gender': user_data['gender'],
                'age': user_data['dob']['age'],
                'country': user_data['location']['country'],
                'email': user_data['email']
            }
            jsonl_data += json.dumps( employee_data) + "\n"  
        client = storage.Client(project=project_id)
        bucket =client.bucket(bucket_name)
        blob =bucket.blob(processed_file)
        blob.upload_from_string(jsonl_data, content_type="application/json")
        print("processed_file uploaded to GCS!") 
        
        return(len(data_results))
       
    else:
     print('Failed to fetch data')
     return 0
def load_to_bigquery():
 client = bigquery.Client(project=project_id)
 table_id = f"{project_id}.{dataset}.{table_name}"
 job_config =bigquery.LoadJobConfig(
    source_format =bigquery.SourceFormat.NEWLINE_DELIMITED_JSON ,
    autodetect=True ,
    write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

 )
 uri =f"gs://{bucket_name}/{processed_file}"
 load_job = client.load_table_from_uri(
    uri,table_id ,job_config=job_config
 )
 load_job.result() 
 print(f"Loaded {load_job.output_rows} rows into {table_id}.")
if __name__ == "__main__":
 Connector= data_fetch()
 gcs_upload(Connector)
 transform_data(Connector)
 load_to_bigquery ()
 

