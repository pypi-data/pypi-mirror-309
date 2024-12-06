from datetime import datetime
import logging
import time
from typing import Optional, Dict, Tuple
import requests

from .exceptions import APIError, ValidationError, TimeoutError
from .models import DetectionResult

class SecureLine:
    """
    SecureLine client for content security detection
    
    Args:
        api_key (str): Your SecureLine API key
        denied_topics (str, optional): Default denied topics
        ppi_information (str, optional): Default PPI information types
        word_filters (str, optional): Default word filters
        timeout (int, optional): Request timeout in seconds. Defaults to 10
        
    Examples:
        >>> # Initialize with default filters
        >>> sl = SecureLine(
        ...     api_key="your-api-key",
        ...     denied_topics="medical diagnoses, competitors",
        ...     ppi_information="SSN, Medical Records",
        ...     word_filters="profanity"
        ... )
        >>> 
        >>> # Use default filters
        >>> result1 = sl.detect("Check this text")
        >>> 
        >>> # Override filters for specific check
        >>> result2 = sl.detect(
        ...     text="Check this text",
        ...     denied_topics="custom topic",
        ...     ppi_information="custom PPI"
        ... )
    """
    
    BASE_URL = "https://secureline.framewise.ai"

    def __init__(
        self,
        api_key: str,
        denied_topics: str = "",
        ppi_information: str = "",
        word_filters: str = "",
        timeout: int = 10
    ):
        self.api_key = api_key
        self.denied_topics = denied_topics
        self.ppi_information = ppi_information
        self.word_filters = word_filters
        self.timeout = timeout
        
        self.logger = logging.getLogger('secureline')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None
    ) -> Tuple[Dict, float]:
        """
        Make HTTP request to API
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            data (dict, optional): Request body
            params (dict, optional): Query parameters
            
        Returns:
            Tuple[Dict, float]: Tuple of (response_json, elapsed_time_ms)
            
        Raises:
            ValidationError: If API returns 422 validation error
            APIError: If request fails
            TimeoutError: If request times out
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = {
            "Content-Type": "application/json",
            "X-API-Token": self.api_key
        }
        
        try:
            start_time = time.time()
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 422:
                error_detail = response.json().get('detail', 'Validation error occurred')
                raise ValidationError(f"API validation error: {error_detail}")
            
            response.raise_for_status()
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            return response.json(), elapsed_time
            
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise APIError(f"API request failed: {str(e)}")

    def detect(
        self,
        text: str,
        denied_topics: Optional[str] = None,
        ppi_information: Optional[str] = None,
        word_filters: Optional[str] = None,
        retry_count: int = 3,
        retry_delay: float = 1.0
    ) -> DetectionResult:
        if not text or not isinstance(text, str):
            raise ValidationError("Text must be a non-empty string")

        payload = {
            "denied_topics": denied_topics if denied_topics is not None else self.denied_topics,
            "ppi_information": ppi_information if ppi_information is not None else self.ppi_information,
            "word_filters": word_filters if word_filters is not None else self.word_filters,
            "text": text
        }

        last_error = None
        for attempt in range(retry_count):
            try:
                response_json, elapsed_time = self._make_request("POST", "/api/v1/inference", data=payload)
                return DetectionResult(
                    raw_response=response_json,
                    elapsed_time=elapsed_time
                )
            except TimeoutError as e:
                last_error = e
                self.logger.warning(f"Attempt {attempt + 1} failed due to timeout. Retrying...")
                if attempt < retry_count - 1:
                    time.sleep(retry_delay)
            except Exception as e:
                last_error = APIError(f"Request failed with no specific error: {str(e)}")
                self.logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                if attempt < retry_count - 1:
                    time.sleep(retry_delay)

        raise last_error



    def update_filters(
        self,
        denied_topics: Optional[str] = None,
        ppi_information: Optional[str] = None,
        word_filters: Optional[str] = None
    ) -> None:
        """
        Update default filters
        
        Args:
            denied_topics (str, optional): New denied topics
            ppi_information (str, optional): New PPI information types
            word_filters (str, optional): New word filters
        """
        if denied_topics is not None:
            self.denied_topics = denied_topics
        if ppi_information is not None:
            self.ppi_information = ppi_information
        if word_filters is not None:
            self.word_filters = word_filters