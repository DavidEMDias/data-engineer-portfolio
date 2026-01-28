import pandas as pd
import simplejson

def model(dbt, session):

    dbt.config(
        materialized="table",
        packages = ["pandas","simplejson"]
    )

    df = dbt.ref("stg_btc").to_pandas() # snowpark dataframe convert to pandas

    df["OUTPUTS"] = df["OUTPUTS"].apply(simplejson.loads) #convert outputs string column into an actual dictionary

    df_exploded = df.explode("OUTPUTS").reset_index(drop=True) #transform each element into a row

    df_outputs = pd.json_normalize(df_exploded["OUTPUTS"])[["address", "value"]] #normalize semi structure json data into a flat table

    #create final df
    df_final = pd.concat([df_exploded.drop(columns="OUTPUTS"), df_outputs],axis=1)

    df_final = df_final[df_final["address"].notnull()]

    df_final.columns = [col.upper() for col in df_final.columns] #upper case all columns in dataframe 

    return df_final