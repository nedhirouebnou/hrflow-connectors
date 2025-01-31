
# Pull jobs
`Ceridian Jobs` :arrow_right: `HrFlow.ai Jobs`

Retrieve all jobs via the ***Ceridian*** API and send them to an ***Hrflow.ai Board***.



## Action Parameters

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| `logics`  | `typing.List[typing.Callable[[typing.Dict], typing.Optional[typing.Dict]]]` | [] | List of logic functions |
| `format`  | `typing.Callable[[typing.Dict], typing.Dict]` | [`format_job`](../connector.py#L15) | Formatting function |
| `read_mode`  | `str` | ReadMode.sync | If 'incremental' then `read_from` of the last run is given to Origin Warehouse during read. **The actual behavior depends on implementation of read**. In 'sync' mode `read_from` is neither fetched nor given to Origin Warehouse during read. |

## Source Parameters

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| `subdomain` :red_circle: | `str` | None | Subdomain used to access Ceridian API |
| `client_name_space` :red_circle: | `str` | None | Client name space used to access Ceridian API |
| `companyName`  | `str` | None | Company name. Example: XYZ Co. |
| `parentCompanyName`  | `str` | None | Parent Company name. Example: Ceridian |
| `lastUpdateTimeFrom`  | `str` | None | A starting timestamp of job posting date. Example: 2017-01-01T13:24:56 |
| `htmlDescription`  | `bool` | None | A flag to feed the jobs over with html formatting or plain text description |

## Destination Parameters

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| `api_secret` :red_circle: | `str` | None | X-API-KEY used to access HrFlow.ai API |
| `api_user` :red_circle: | `str` | None | X-USER-EMAIL used to access HrFlow.ai API |
| `board_key` :red_circle: | `str` | None | HrFlow.ai board key |
| `sync`  | `bool` | True | When enabled only pushed jobs will remain in the board |
| `update_content`  | `bool` | False | When enabled jobs already present in the board are updated |
| `enrich_with_parsing`  | `bool` | False | When enabled jobs are enriched with HrFlow.ai parsing |

:red_circle: : *required*

## Example

```python
import logging
from hrflow_connectors import Ceridian
from hrflow_connectors.core import ReadMode


logging.basicConfig(level=logging.INFO)


Ceridian.pull_jobs(
    workflow_id="some_string_identifier",
    action_parameters=dict(
        logics=[],
        format=lambda *args, **kwargs: None # Put your code logic here,
        read_mode=ReadMode.sync,
    ),
    origin_parameters=dict(
        subdomain="your_subdomain",
        client_name_space="your_client_name_space",
        companyName="your_companyName",
        parentCompanyName="your_parentCompanyName",
        lastUpdateTimeFrom="your_lastUpdateTimeFrom",
        htmlDescription=False,
    ),
    target_parameters=dict(
        api_secret="your_api_secret",
        api_user="your_api_user",
        board_key="your_board_key",
        sync=True,
        update_content=False,
        enrich_with_parsing=False,
    )
)
```