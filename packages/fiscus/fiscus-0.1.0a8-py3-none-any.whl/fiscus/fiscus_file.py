from typing import TypedDict, Union

class FiscusFile(TypedDict):
    """
	The `FiscusFile` class is a utility for managing file uploads in the Fiscus SDK.

	This class simplifies the handling of files by providing a structured way to define
	metadata and content for files to be uploaded to the Fiscus platform. It supports
	mapping files to specific fields in request parameters and ensures compatibility with
	various input formats.

	### Attributes:
	- **targetField** (`str`): The field in the API parameters where this file will be mapped.
	- **name** (`str`): The name of the file (e.g., "document.pdf").
	- **type** (`str`): The MIME type of the file (e.g., "application/pdf", "image/png").
	- **content** (`Union[str, bytes]`): The file's content, which can be:
	- A file path as a string (e.g., "/path/to/file").
	- A direct string representing the content (e.g., JSON content as a string).
	- Binary content (e.g., image or document bytes).

	### Usage:
	The `FiscusFile` class is intended to be used with Fiscus SDK methods requiring file
	uploads. By standardizing the input format, it ensures smooth integration and
	processing of file data.

	Example:
	```python
	file_upload = FiscusFile(
		targetField="user_profile_image",
		name="profile.png",
		type="image/png",
		content=open("path/to/image.png", "rb").read()  # File content as bytes
	)
	"""
    targetField: str  # Field in params where this file should be mapped
    name: str         # Name of the file
    type: str         # MIME type of the file
    content: Union[str, bytes]  # Content can be a file path, direct string, or bytes