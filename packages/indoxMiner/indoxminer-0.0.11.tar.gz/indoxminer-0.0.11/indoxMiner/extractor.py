import asyncio
from typing import List, Dict, Any, Union, Tuple, Optional
from loguru import logger
import re
import pandas as pd
import json
from tabulate import tabulate
from tabulate import tabulate
from decimal import Decimal
from .extraction_results import ExtractionResult, ExtractionResults
from .fields import Field, FieldType
from .utils import Document


class Extractor:
    """Data extractor using LLM with validation and concurrent processing."""

    def __init__(
        self,
        llm: Any,
        schema: Any,
        max_concurrent: int = 3,
    ):
        self.llm = llm
        self.schema = schema
        self.max_concurrent = max_concurrent
        self.is_async = asyncio.iscoroutinefunction(self.llm.generate)

    def _sync_extract_chunk(
        self, text: str, chunk_index: int
    ) -> Tuple[int, ExtractionResult]:
        """Synchronous version of extract chunk."""
        try:
            prompt = self.schema.to_prompt(text)
            response = self.llm.generate(prompt)
            return self._process_response(response, chunk_index)
        except Exception as e:
            logger.error(f"Extraction failed for chunk {chunk_index}: {e}")
            return chunk_index, ExtractionResult(
                data={},
                raw_response=str(e),
                validation_errors=[f"Extraction error: {str(e)}"],
            )

    async def _async_extract_chunk(
        self, text: str, chunk_index: int
    ) -> Tuple[int, ExtractionResult]:
        """Asynchronous version of extract chunk."""
        try:
            prompt = self.schema.to_prompt(text)
            response = await self.llm.generate(prompt)
            return self._process_response(response, chunk_index)
        except Exception as e:
            logger.error(f"Extraction failed for chunk {chunk_index}: {e}")
            return chunk_index, ExtractionResult(
                data={},
                raw_response=str(e),
                validation_errors=[f"Extraction error: {str(e)}"],
            )

    def _validate_field(self, field: Field, value: Any) -> List[str]:
        """Validate a single field value against its rules."""
        errors = []
        if value is None and field.required:
            errors.append(f"{field.name} is required but missing")
            return errors

        if field.rules:
            rules = field.rules
            if rules.min_value is not None and value < rules.min_value:
                errors.append(f"{field.name} is below minimum value {rules.min_value}")
            if rules.max_value is not None and value > rules.max_value:
                errors.append(f"{field.name} exceeds maximum value {rules.max_value}")
            if (
                rules.pattern is not None
                and isinstance(value, str)
                and not re.match(rules.pattern, value)
            ):
                errors.append(f"{field.name} does not match pattern {rules.pattern}")
            if rules.allowed_values is not None and value not in rules.allowed_values:
                errors.append(f"{field.name} contains invalid value")
            if rules.min_length is not None and len(str(value)) < rules.min_length:
                errors.append(
                    f"{field.name} is shorter than minimum length {rules.min_length}"
                )
            if rules.max_length is not None and len(str(value)) > rules.max_length:
                errors.append(f"{field.name} exceeds maximum length {rules.max_length}")
        return errors

    def _process_response(
        self, response: str, chunk_index: int
    ) -> Tuple[int, ExtractionResult]:
        """Process and validate the LLM response, assuming JSON."""
        try:
            cleaned_response = self._clean_json_response(response)
            logger.debug(f"Cleaned JSON response: {cleaned_response}")

            try:
                data = json.loads(cleaned_response)
            except json.JSONDecodeError:
                fixed_json = self._fix_json(cleaned_response)
                data = json.loads(fixed_json)

            data = self._normalize_json_structure(data)
            validation_errors = self._validate_data(data)

            return chunk_index, ExtractionResult(
                data=data, raw_response=response, validation_errors=validation_errors
            )
        except json.JSONDecodeError as e:
            logger.error(
                f"JSON parsing error: {e}\nCleaned Response: {cleaned_response}"
            )
            return chunk_index, ExtractionResult(
                data={},
                raw_response=response,
                validation_errors=[f"JSON parsing error: {str(e)}"],
            )

    def extract(
        self,
        input_data: Union[str, Document, List[Document], Dict[str, List[Document]]],
    ) -> Union[ExtractionResult, ExtractionResults]:
        """Unified extraction method that handles both sync and async LLMs appropriately."""
        if not self.is_async:
            if isinstance(input_data, str):
                return self._sync_extract_chunk(input_data, 0)[1]
            elif isinstance(input_data, Document):
                return self._sync_extract_chunk(input_data.page_content, 0)[1]
            elif isinstance(input_data, list):
                results = [
                    self._sync_extract_chunk(doc.page_content, i)
                    for i, doc in enumerate(input_data)
                ]
                results.sort(key=lambda x: x[0])
                return ExtractionResults(
                    data=[result.data for _, result in results],
                    raw_responses=[result.raw_response for _, result in results],
                    validation_errors={
                        i: result.validation_errors
                        for i, (_, result) in enumerate(results)
                        if result.validation_errors
                    },
                )
            elif isinstance(input_data, dict):
                all_documents = [doc for docs in input_data.values() for doc in docs]
                return self.extract(all_documents)
            else:
                raise ValueError("Unsupported input type")
        else:
            try:
                return asyncio.run(self._async_extract(input_data))
            except Exception as e:
                logger.error(f"Async extraction failed: {str(e)}")
                raise

    async def _async_extract(
        self,
        input_data: Union[str, Document, List[Document], Dict[str, List[Document]]],
    ) -> Union[ExtractionResult, ExtractionResults]:
        if isinstance(input_data, str):
            _, result = await self._async_extract_chunk(input_data, 0)
            return result
        elif isinstance(input_data, Document):
            _, result = await self._async_extract_chunk(input_data.page_content, 0)
            return result
        elif isinstance(input_data, list):
            semaphore = asyncio.Semaphore(self.max_concurrent)

            async def extract_with_semaphore(text: str, index: int):
                async with semaphore:
                    return await self._async_extract_chunk(text, index)

            tasks = [
                extract_with_semaphore(doc.page_content, i)
                for i, doc in enumerate(input_data)
            ]
            results = await asyncio.gather(*tasks)
            results.sort(key=lambda x: x[0])
            return ExtractionResults(
                data=[result.data for _, result in results],
                raw_responses=[result.raw_response for _, result in results],
                validation_errors={
                    i: result.validation_errors
                    for i, (_, result) in enumerate(results)
                    if result.validation_errors
                },
            )
        elif isinstance(input_data, dict):
            all_documents = [doc for docs in input_data.values() for doc in docs]
            return await self._async_extract(all_documents)
        else:
            raise ValueError("Unsupported input type")

    def _clean_json_response(self, response_text: str) -> str:
        response_text = re.sub(r"```json\s*|\s*```", "", response_text.strip())
        return "\n".join(
            re.sub(r"\s*//.*$", "", line.rstrip())
            for line in response_text.split("\n")
            if line
        )

    def _fix_json(self, json_str: str) -> str:
        fixed_json = re.sub(r",(\s*[}\]])", r"\1", json_str)
        return re.sub(r"}\s*{", "},{", fixed_json)

    def _normalize_json_structure(self, data):
        if isinstance(data, list):
            data = {"items": data}
        elif isinstance(data, dict) and not any(
            isinstance(v, list) for v in data.values()
        ):
            data = {"items": [data]}
        else:
            items_field_name = None
            items = []
            common_fields = {}

            for key, value in data.items():
                if isinstance(value, list) and all(
                    isinstance(item, dict) for item in value
                ):
                    items_field_name = key
                    items = value
                elif not isinstance(value, (list, dict)):
                    common_fields[key] = value

            if items_field_name and items:
                data = {"items": [{**common_fields, **{items_field_name: items}}]}
            else:
                data = {"items": [data]}

        return data

    def _validate_data(self, data: Dict) -> List[str]:
        validation_errors = []
        for i, item in enumerate(data["items"]):
            for field in self.schema.fields:
                value = item.get(field.name)
                errors = self._validate_field(field, value)
                if errors:
                    validation_errors.extend(
                        [f"Item {i + 1}: {error}" for error in errors]
                    )
        return validation_errors

    def to_dataframe(
        self,
        results: Union[
            ExtractionResult,
            ExtractionResults,
            List[Union[ExtractionResult, ExtractionResults]],
        ],
    ) -> Optional[pd.DataFrame]:
        """Convert one or multiple extraction results to a single pandas DataFrame."""
        try:
            if not isinstance(results, list):
                results = [results]

            dataframes = []
            for result in results:
                if isinstance(result, ExtractionResult):
                    if "items" in result.data:
                        df = pd.DataFrame(result.data["items"])
                    else:
                        df = pd.DataFrame([result.data])
                elif isinstance(result, ExtractionResults):
                    if any("items" in res for res in result.data):
                        items = []
                        for res in result.data:
                            if "items" in res:
                                items.extend(res["items"])
                            else:
                                items.append(res)
                        df = pd.DataFrame(items)
                    else:
                        df = pd.DataFrame(result.data)
                else:
                    raise ValueError("Invalid result type")

                dataframes.append(df)

            final_df = pd.concat(dataframes, ignore_index=True)

            expected_columns = [field.name for field in self.schema.fields]
            final_df = final_df.reindex(columns=expected_columns)

            numeric_columns = [
                field.name
                for field in self.schema.fields
                if field.field_type in [FieldType.FLOAT, FieldType.INTEGER]
            ]
            for col in numeric_columns:
                final_df[col] = pd.to_numeric(final_df[col], errors="coerce")

            return final_df

        except Exception as e:
            logger.error(f"Failed to convert to DataFrame: {e}")
            return None

    def to_json(
        self,
        results: Union[
            ExtractionResult,
            ExtractionResults,
            List[Union[ExtractionResult, ExtractionResults]],
        ],
    ) -> Optional[str]:
        """Convert multiple extraction results to a single JSON string."""
        try:
            if not isinstance(results, list):
                results = [results]

            combined_data = [result.data for result in results]
            return json.dumps(combined_data, indent=2)
        except Exception as e:
            logger.error(f"Failed to convert to JSON: {e}")
            return None

    def to_markdown(
        self,
        results: Union[
            ExtractionResult,
            ExtractionResults,
            List[Union[ExtractionResult, ExtractionResults]],
        ],
    ) -> Optional[str]:
        """Convert one or multiple extraction results to a single Markdown formatted string."""
        try:
            if not isinstance(results, list):
                results = [results]

            markdown_output = "\n\n".join(
                self._extract_items_to_markdown(
                    result.data if isinstance(result, ExtractionResult) else item
                )
                for result in results
                for item in (
                    result.data
                    if isinstance(result, ExtractionResults)
                    else [result.data]
                )
            )
            return markdown_output
        except Exception as e:
            logger.error(f"Failed to convert to Markdown: {e}")
            return None

    def to_table(
        self,
        results: Union[
            ExtractionResult,
            ExtractionResults,
            List[Union[ExtractionResult, ExtractionResults]],
        ],
    ) -> Optional[str]:
        """Convert one or multiple extraction results to a single formatted table string."""
        try:
            if not isinstance(results, list):
                results = [results]

            table_output = " \n\n ".join(
                self._extract_items_to_table(
                    result.data if isinstance(result, ExtractionResult) else item
                )
                for result in results
                for item in (
                    result.data
                    if isinstance(result, ExtractionResults)
                    else [result.data]
                )
            )
            return table_output
        except Exception as e:
            logger.error(f"Failed to convert to table: {e}")
            return None

    def _extract_items_to_markdown(self, data: Dict[str, Any]) -> str:
        """Convert data with nested 'items' into a more readable Markdown format."""
        markdown_sections = []
        headers = [key for key in data.keys() if key != "items"]
        values = [data[key] for key in headers]
        markdown_sections.append(tabulate([values], headers=headers, tablefmt="github"))

        if "items" in data and isinstance(data["items"], list):
            for item in data["items"]:
                markdown_sections.append(self._dict_to_markdown(item))

        return " \n\n ".join(markdown_sections)

    def _extract_items_to_table(self, data: Dict[str, Any]) -> str:
        """Convert data with nested 'items' into a more readable table format."""
        table_sections = []
        headers = [key for key in data.keys() if key != "items"]
        values = [data[key] for key in headers]
        table_sections.append(tabulate([values], headers=headers, tablefmt="grid"))

        if "items" in data and isinstance(data["items"], list):
            for item in data["items"]:
                table_sections.append(self._dict_to_table(item))

        return " \n\n ".join(table_sections)

    def _dict_to_markdown(self, data: Dict) -> str:
        headers = list(data.keys())
        rows = [[data[key] for key in headers]]
        return tabulate(rows, headers=headers, tablefmt="github")

    def _dict_to_table(self, data: Dict) -> str:
        headers = list(data.keys())
        rows = [[data[key] for key in headers]]
        return tabulate(rows, headers=headers, tablefmt="grid")
