<!-- Utility functions -->
- read_json_file(file_path: str) -> dict
- write_json_file(file_path: str, data: dict) -> None
- validate_url_format(url: str) -> bool
- download_file_from_url(url: str, dest_path: str) -> None
- get_environment_variable(var_name: str, default: str) -> str
- send_email(smtp_server: str, port: int, sender: str, recipient: str, subject: str, body: str) -> None
- validate_email_address(email: str) -> bool
- generate_random_password(length: int, include_special_chars: bool) -> str
- compress_directory_to_zip(dir_path: str, zip_path: str) -> None
- extract_zip_to_directory(zip_path: str, extract_to: str) -> None

<!-- Decorators -->
- measure_execution_time(func) -> float
- retry_on_exception(func, retries: int, delay: int) -> Any
