# Tools to mainpulate dataframes. Convert any Natural Language query to a pandas query and process data frames..

import logging
import os
import json
import csv
from typing import List, Optional
from fastapi import HTTPException
import pandas as pd
from pydantic import BaseModel
import time
import os
from openai import LengthFinishReasonError, AsyncOpenAI, OpenAIError
import csv
from dhisana.utils.assistant_tool_tag import assistant_tool

class FileItem:
    def __init__(self, file_path: str):
        self.file_path = file_path

class FileList:
    def __init__(self, files: List[FileItem]):
        self.files = files

class PandasQuery(BaseModel):
    pandas_query: str
    

@assistant_tool   
async def get_structured_output(message: str, response_type, model: str = "gpt-4o-2024-08-06"):
    """
    Asynchronously retrieves structured output from the OpenAI API based on the input message.

    :param message: The input message to be processed by the OpenAI API.
    :param response_type: The expected format of the response (e.g., JSON).
    :param model: The model to be used for processing the input message. Defaults to "gpt-4o-2024-08-06".
    :return: A tuple containing the parsed response and a status string ('SUCCESS' or 'FAIL').
    """
    try:
        client = AsyncOpenAI()
        completion = await client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": "Extract structured content from input. Output is in JSON Format."},
                {"role": "user", "content": message},
            ],
            response_format=response_type,
        )

        response = completion.choices[0].message
        if response.parsed:
            return response.parsed, 'SUCCESS'
        elif response.refusal:
            logging.warning("ERROR: Refusal response: %s", response.refusal)
            return response.refusal, 'FAIL'
        
    except LengthFinishReasonError as e:
        logging.error(f"Too many tokens: {e}")
        raise HTTPException(status_code=502, detail="The request exceeded the maximum token limit.")
    except OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=502, detail="Error communicating with the OpenAI API.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing your request.")  

@assistant_tool
async def query_dataframes(user_query: str, input_files: Optional[List[str]], output_file_path: Optional[str] = None) -> str:
    """
    Query multiple dataframes based on a user query and write the output dataframe to a specified output file path.

    Args:
        user_query (str): User query in natural language.
        input_files (List[str]): List of paths to CSV files to be loaded into dataframes.
        output_file_path (Optional[str]): Path to the output file where the resulting dataframe will be saved.
            If not specified, a unique file path will be generated in '/tmp/run_interim_outputs/'.

    Returns:
        str: A JSON string representing the FileList containing the path to the output file if created, otherwise an empty list.
    """
    max_retries = 3
    # Check if the list of CSV files or the user query is empty
    if not input_files or not user_query:
        # Return an empty FileList as JSON
        return json.dumps({"files": []})

    # If output_file_path is not specified, generate one
    if not output_file_path:
        output_folder = '/tmp/run_interim_outputs/'
        # Ensure output_folder exists
        os.makedirs(output_folder, exist_ok=True)
        # Generate a unique filename
        unique_number = int(time.time() * 1000)  # milliseconds since epoch
        output_file_name = f'query_dataframe_{unique_number}.csv'
        output_file_path = os.path.join(output_folder, output_file_name)
    else:
        # Ensure the directory exists
        output_folder = os.path.dirname(output_file_path)
        if output_folder:
            os.makedirs(output_folder, exist_ok=True)

    # Load CSV files into dataframes, skipping empty files
    data_frames = []
    df_names = []
    for idx, file in enumerate(input_files):
        # Check if the file is empty
        if os.path.getsize(file) == 0:
            # Skip empty files
            continue
        df = pd.read_csv(file)
        data_frames.append(df)
        df_name = f'df{idx+1}'
        df_names.append(df_name)

    # Check if any dataframes were loaded
    if not data_frames:
        # Return an empty FileList as JSON
        return json.dumps({"files": []})

    # Create a context with the dataframes and their schemas
    schema_info = ""
    for df_name, df in zip(df_names, data_frames):
        schema_info += f"DataFrame '{df_name}' columns: {', '.join(df.columns)}\n"

    # Initialize the error message as empty
    error_message = ""

    for attempt in range(max_retries):
        # Prepare the message
        message = f"""
        You are an expert data analyst. Given the following DataFrames and their schemas:

        {schema_info}

        Write a pandas query to answer the following question:

        \"\"\"{user_query}\"\"\"

        Your query should use the provided DataFrames ({', '.join(df_names)}) and produce a DataFrame named 'result_df'. Do not include any imports or explanations; only provide the pandas query code that assigns the result to 'result_df'.
        """
        if error_message:
            message += f"\nThe previous query returned the following error:\n{error_message}\nPlease fix the query."

        # Get structured output
        pandas_query_result, status = await get_structured_output(message, PandasQuery)
        if status == 'SUCCESS' and pandas_query_result and pandas_query_result.pandas_query:
            pandas_query = pandas_query_result.pandas_query
            # Execute the query safely
            local_vars = {name: df for name, df in zip(df_names, data_frames)}
            global_vars = {}
            try:
                exec(pandas_query, global_vars, local_vars)
                result_df = local_vars.get('result_df')
                if result_df is None:
                    raise ValueError("The query did not produce a DataFrame named 'result_df'.")
                # If execution is successful, break out of the loop
                break
            except Exception as e:
                # Capture the error message
                error_message = str(e)
                # If this was the last attempt, raise the error
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Error executing generated query after {max_retries} attempts: {error_message}")
                # Otherwise, continue to the next iteration
                continue
        else:
            # If unable to get a valid response, raise an error
            if attempt == max_retries - 1:
                raise RuntimeError("Failed to get a valid pandas query after multiple attempts.")
            continue

    # Write the resulting DataFrame to the output file
    result_df.to_csv(output_file_path, index=False)

    # Create FileList object
    file_list = FileList(files=[FileItem(file_path=output_file_path)])

    # Convert FileList to JSON
    def file_item_to_dict(file_item):
        return {"file_path": file_item.file_path}

    file_list_dict = {
        "files": [file_item_to_dict(file_item) for file_item in file_list.files]
    }
    file_list_json = json.dumps(file_list_dict, indent=2)
    return file_list_json

@assistant_tool
async def load_csv_file(input_file_path: str):
    """
    Loads data from a CSV file and returns it as a list of dictionaries.

    Args:
        input_file_path (str): The path to the input CSV file.

    Returns:
        List[Dict[str, Any]]: List of rows from the CSV file, where each row is a dictionary.
    """
    with open(input_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
 