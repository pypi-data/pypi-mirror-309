# whipcode-py
[![PyPI badge](https://img.shields.io/pypi/v/whipcode?style=flat&color=blue)](https://pypi.org/project/whipcode) [![License badge](https://img.shields.io/pypi/l/whipcode?style=flat&color=blue)](https://github.com/Whipcode-API/whipcode-py/blob/main/LICENSE) [![Workflow badge](https://img.shields.io/github/actions/workflow/status/whipcode-api/whipcode-py/python-tests.yml?label=tests)](https://github.com/Whipcode-API/whipcode-py/actions/workflows/python-tests.yml)

A convenient way to access [Whipcode API](https://whipcode.app) from Python applications.

Compatible with [self-hosted](https://github.com/Whipcode-API/whipcode) instances as well.

## Installation
Get it from PyPI:
```
pip install whipcode
```

## Usage
Here's an asynchronous snippet:
```python
import asyncio

from whipcode import Whipcode, Langs
from whipcode.exceptions import RequestError, PayloadBuildError

async def main():
    whip = Whipcode()
    whip.rapid_key("YOUR_RAPIDAPI_KEY")  # not needed if the RAPID_KEY environment variable is set

    code = "echo 'Hello World!'"

    execution = whip.run_async(code, Langs.BASH)

    # Other tasks while the execution is in progress

    try:
        result = await execution

    except (RequestError, PayloadBuildError) as e:
        # Handle the error

asyncio.run(main())
```
And a synchronous one:
```python
from whipcode import Whipcode, Langs
from whipcode.exceptions import RequestError, PayloadBuildError

def main():
    whip = Whipcode()

    code = '(println "Hello World!")'

    try:
        result = whip.run(code, Langs.CLOJURE)

    except (RequestError, PayloadBuildError) as e:
        # Handle the error

main()
```
The result object:
```
ExecutionResult(status=200, stdout='Hello World!\n', stderr='', container_age=0.338638005, timeout=False, detail='', rapid={'messages': '', 'message': '', 'info': ''})
```

## Providers
Changing the provider is easy. Here's how the default provider is defined:
```python
{
  "endpoint": "https://whipcode.p.rapidapi.com/run",
  "headers": {
    "X-RapidAPI-Key": "",
    "X-RapidAPI-Host": "whipcode.p.rapidapi.com"
  },
  "query_injects": [
    {}
  ]
}
```

Just pass your custom provider to the constructor:
```python
whip = Whipcode(custom_provider)
```

Or swap it in on the already initialized object:
```python
whip.provider = custom_provider
```

An example custom provider:
```python
{
  "endpoint": "https://<host>/run",
  "headers": {
    "Authorization": "Bearer xxx"
  },
  "query_injects": []
}
```

## Reference
### Constructor
```python
Whipcode(provider: dict = Whipcode.default_provider)
```
**Parameters:**
- **provider** - *dict, optional*\
  &nbsp;&nbsp;&nbsp;The provider configuration. See the [Providers](#providers) section.

### rapid_key
```python
rapid_key(key: str)
```
Sets the RapidAPI key to use when making requests.

**Parameters:**
- **key** - *str*\
  &nbsp;&nbsp;&nbsp;Your RapidAPI key.

### run
```python
run(code: str, language: str | int, args: list = [], timeout: int = 0) -> ExecutionResult
```
Makes a request to the endpoint synchronously.

**Parameters:**
- **code** - *str*\
  &nbsp;&nbsp;&nbsp;The code to execute.
- **language** - *str, int*\
  &nbsp;&nbsp;&nbsp;Language ID of the submitted code.
- **args** - *list, optional*\
  &nbsp;&nbsp;&nbsp;A list of compiler/interpreter args.
- **timeout** - *int, optional*\
  &nbsp;&nbsp;&nbsp;Timeout in seconds for the code to run.
- **stdin** - *str, optional*\
  &nbsp;&nbsp;&nbsp;Standard input passed to the execution.
- **env** - *dict, optional*\
  &nbsp;&nbsp;&nbsp;Environment variables to set.

**Returns:**
- [ExecutionResult](#executionresult)

### run_async
```python
run_async(code: str, language: str | int, args: list = [], timeout: int = 0) -> asyncio.Task
```
Makes a request to the endpoint asynchronously.

**Parameters:**
- **code** - *str*\
  &nbsp;&nbsp;&nbsp;The code to execute.
- **language** - *str, int*\
  &nbsp;&nbsp;&nbsp;Language ID of the submitted code.
- **args** - *list, optional*\
  &nbsp;&nbsp;&nbsp;A list of compiler/interpreter args.
- **timeout** - *int, optional*\
  &nbsp;&nbsp;&nbsp;Timeout in seconds for the code to run.
- **stdin** - *str, optional*\
  &nbsp;&nbsp;&nbsp;Standard input passed to the execution.
- **env** - *dict, optional*\
  &nbsp;&nbsp;&nbsp;Environment variables to set.

**Returns:**
- A Task that returns [ExecutionResult](#executionresult).

### ExecutionResult
```python
ExecutionResult(stdout: str, stderr: str, container_age: float, timeout: bool, status: int, detail: str, rapid: dict = {})
```
Returned as the result after a request.

**Attributes**
- **stdout** - *str*\
  &nbsp;&nbsp;&nbsp;All data captured from stdout.
- **stderr** - *str*\
  &nbsp;&nbsp;&nbsp;All data captured from stderr.
- **container_age** - *float*\
  &nbsp;&nbsp;&nbsp;Duration the container allocated for your code ran, in seconds.
- **timeout** - *bool*\
  &nbsp;&nbsp;&nbsp;Boolean value depending on whether your container lived past the timeout period.
- **status** - *int*\
  &nbsp;&nbsp;&nbsp;The status code of the request response.
- **detail** - *str*\
  &nbsp;&nbsp;&nbsp;Details about why the request failed to complete.
- **rapid** - *dict*\
  &nbsp;&nbsp;&nbsp;Various keys that RapidAPI uses when returning their own error messages.

### Langs
```python
Langs:
    PYTHON     = 1
    JAVASCRIPT = 2
    BASH       = 3
    PERL       = 4
    LUA        = 5
    RUBY       = 6
    C          = 7
    CPP        = 8
    RUST       = 9
    FORTRAN    = 10
    HASKELL    = 11
    JAVA       = 12
    GO         = 13
    TYPESCRIPT = 14
    CLISP      = 15
    RACKET     = 16
    CRYSTAL    = 17
    CLOJURE    = 18
    X86        = 19
    ZIG        = 20
    NIM        = 21
    DLANG      = 22
    CSHARP     = 23
    RSCRIPT    = 24
    DART       = 25
    VB         = 26
    FSHARP     = 27
    PHP        = 28
```
A mapping of language IDs to their respective names.

### Exceptions
- **RequestError** - Raised when an error occurs during the request
- **PayloadBuildError** - Raised when an error occurs while building the payload

## Contributing
Please read the [contributing guidelines](https://github.com/Whipcode-API/whipcode-py/blob/main/.github/CONTRIBUTING.md) before opening a pull request.

## License
This library is licensed under the [MIT License](https://github.com/Whipcode-API/whipcode-py/blob/main/LICENSE).
