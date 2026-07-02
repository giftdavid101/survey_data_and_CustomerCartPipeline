import sys
import pandas as pd
import loader

def load_bronze():
    try:
        print('started processing bronze_layer')
        df = pd.read_excel(r"/opt/airflow/my_files/Survey Data.xlsx")

        print(df.head(3))

        loader.write_to_db(data_df=df, table_name='survey_data'
                        ,mode='replace',schema='bronze_layer')
        print("Done processing bronze_data")

    except Exception as err:
        print(f'failed processing bronze data with Error : {err}')
        raise


def load_silver_data():
    try:
        print("Started processing silver data")
        query = """SELECT CAST("Timestamp" AS DATE) AS survey_date,
        "How old are you?" AS age_range,
        "What industry do you work in?" AS industry,
        "Job title" AS job_title,
        "If your job title needs additional context, please clarify here"  AS job_title_context,
        "What is your annual salary? (You'll indicate the currency in a "  AS annual_salary,
        "How much additional monetary compensation do you get, if any (f"   AS additional_compensation,
        "Please indicate the currency"  AS currency,
        'If "Other," please indicate the currency here:'  AS other_currency,
        "If your income needs additional context, please provide it here"  AS income_context,
        "What country do you work in?"  AS country,
        "If you're in the U.S., what state do you work in?"  AS us_state,
        "What city do you work in?"  AS city,
        "How many years of professional work experience do you have over"  
        AS total_years_experience,
        "How many years of professional work experience do you have in y"  
        AS field_years_experience,
        "What is your highest level of education completed?" AS education_level,
        "What is your gender?" AS gender,
        "What is your race? (Choose all that apply.)" AS race FROM bronze_layer.survey_data"""

        df = loader.read_df(query=query)

        print("Successfully processed bronze_data from DB")

        print(df.head(3))

        loader.write_to_db(data_df=df, table_name='survey_data_transformed'
                        ,mode='replace',schema='silver_layer')
        
        print("Done processing silver data")
    except Exception as err:
        print(f'Failed processing silver data with Error : {err}')

if __name__ == '__main__':
    run_module = sys.argv[1]
    if run_module == '1':
        load_bronze()
    elif run_module == '2':
        load_silver_data()