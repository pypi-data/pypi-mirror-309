import pandas as pd
import re
import time
import json
import asyncio
import pytz
import datetime
from typing import Any, Dict, List
from tqdm import tqdm
import google.generativeai as genai
import nest_asyncio
nest_asyncio.apply()

# Initialize progress bar for pandas
tqdm.pandas()

class GeminiBot:
    # Utility Functions
    def india_time() -> str:
        """
        Get the current time in the Indian timezone.

        Returns:
            str: Current time in 'Asia/Kolkata' timezone.
        """
        return datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')


    def normalize_json_string(self, json_string: str) -> str:
        """
        Normalize a JSON string by fixing formatting issues.

        Args:
            json_string (str): Input JSON string.

        Returns:
            str: Normalized JSON string.
        """
        try:
            json_string = json_string.strip()
            json_string = re.sub(r"(?<!\\)'", '"', json_string)
            json_string = re.sub(r'\s+', ' ', json_string)
            json_string = re.sub(r'(-+)', '-', json_string)
            json_string = re.sub(r'(\[\s*)\{', '[{', json_string)
            json_string = re.sub(r'\}\s*(\])', '}]', json_string)
            json_string = re.sub(r',\s*}', '}', json_string)
            json_string = re.sub(r',\s*]', ']', json_string)
            json_string = re.sub(r'\s*,\s*([}\]])', r'\1', json_string)
        except Exception as e:
            print(f"Error normalizing JSON string: {e}")
        return json_string


    def lowercase_keys(self ,d: Any) -> Any:
        """
        Recursively convert all dictionary keys to lowercase.

        Args:
            d (Any): Input dictionary or list.

        Returns:
            Any: Transformed dictionary or list with lowercase keys.
        """
        if isinstance(d, dict):
            return {k.lower(): self.lowercase_keys(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [self.lowercase_keys(i) for i in d]
        return d


    # Recipe Model Class
    class RecipeModel:
        """
        Represents a recipe model with a schema definition.
        """
        def __init__(self, fields: Dict[str, Any]):
            self.fields = fields

        def schema(self) -> Dict[str, Any]:
            """
            Get the schema as a dictionary.
            """
            return self.fields


    # Helper Functions
    def extract_json(self,model: str, id: Any, content: str) -> List[Dict[str, Any]]:
        """
        Extract JSON data from a response.

        Args:
            model (str): Model name.
            id (Any): Record ID.
            content (str): Response content.

        Returns:
            List[Dict[str, Any]]: Extracted data.
        """
        try:
            json_data = json.loads(content)
            normalized_json_data = self.normalize_json_string(content)
            dic_set = json_data if not isinstance(json_data, str) else json.loads(normalized_json_data)

            if isinstance(dic_set, dict):
                dic_set = [dic_set]

            return [
                self.lowercase_keys({**item, 'id': id, 'model': model, 'content': content})
                for item in dic_set
            ]
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        except Exception as e:
            print(f"Error extracting JSON: {e}")
        return [{'id': id, 'model': model, 'content': content}]


    def generate_prompt(self,row: pd.Series, prompt_template: str) -> str:
        """
        Generate a prompt using a row of data.

        Args:
            row (pd.Series): Data row.
            prompt_template (str): Template string.

        Returns:
            str: Generated prompt.
        """
        try:
            return prompt_template.format(row=row)
        except Exception as e:
            print(f"Error generating prompt: {e}")
            return ""


    # Async Bot Functions
    async def gemini_bot(self,content: str, id: Any, recipe_model: RecipeModel) -> tuple:
        """
        Use the Gemini bot to generate a response.

        Args:
            content (str): Input content.
            id (Any): Record ID.
            recipe_model (RecipeModel): Recipe schema.
            mentions_key_name (List[str]): Keys to verify.

        Returns:
            tuple: Model name, response, and ID.
        """
        try:
            model = genai.GenerativeModel(self.model)
            query = f"{content}"
            response = model.generate_content(
                query,
                generation_config={
                    "response_mime_type": "application/json",
                    'response_schema': {
                        "type": "object",
                        "properties": {key: {"type": "string"} for key in recipe_model.schema()},
                        "required": list(recipe_model.schema().keys()),
                    }
                }
            )
            return self.model, response.text, id
        except Exception as e:
            if "API key not valid" in str(e):
                raise Exception("API is not Vaild. Kindly Check it.")
            elif "429" in str(e):
                raise Exception(f"Rate Limit Exceeded. Please try after some time.")
            else:
                print(f"Error with Gemini bot: {e}")

    def model_list(api_key: str):
        genai.configure(api_key=api_key)
        data = genai.list_models()
        for model in data:
            if 'generateContent' in model.supported_generation_methods:
                if 'vision' not in model.name.lower():
                    print(model)
                    
    # Main Functionality
    async def process_data(self,input_dataset: pd.DataFrame, recipe_model: RecipeModel):
        """
        Process the input data through Gemini and PLAM bots.

        Args:
            input_dataset (pd.DataFrame): Input dataset.
            recipe_model (RecipeModel): Output schema.
            prompt_template (str): Template string for prompts.
            mentions_key_name (List[str]): Output keys.
        """
        queries = input_dataset['prompt'].to_list()
        ids = input_dataset['id'].to_list()
        zip_list = list(zip(queries, ids))

        results = []
        bar = tqdm(total=len(zip_list), desc="Processing")

        for query, id in zip_list:
            response = await self.gemini_bot(query, id, recipe_model)
            results.append(response)
            bar.update(1)

        bar.close()
        result_df = pd.DataFrame(results, columns=['model', 'response', 'id'])
        extracted_data = result_df.apply(lambda row: self.extract_json(row['model'], row['id'], row['response']), axis=1)
        final_df = pd.json_normalize(extracted_data.explode())
        merged_df = pd.merge(input_dataset, final_df, on='id', how='left')
        merged_df.to_csv('output_dataset.csv', index=False)


    # Entry Point
    def __init__(self,input_file: str, prompt_template: str, key_names: str,api_key: str,model: str):
        self.model = model
        genai.configure(api_key=api_key)
        if '.csv' in input_file:
            input_dataset = pd.read_csv(input_file, low_memory=False)
        elif '.xlsx' in input_file:
            input_dataset = pd.read_excel(input_file)
        else:
            raise ValueError("Invalid file format. Please provide a CSV or Excel file.")
        input_dataset.columns = input_dataset.columns.str.lower().str.replace(' ', '_')
        input_dataset['id'] = range(len(input_dataset))

        mentions_key_name = key_names.split(',')
        fields = {key.strip().lower(): "str" for key in mentions_key_name}
        recipe_model = self.RecipeModel(fields)

        input_dataset['prompt'] = input_dataset.apply(lambda row: self.generate_prompt(row, prompt_template), axis=1)
        asyncio.run(self.process_data(input_dataset, recipe_model))
