# `tap-pulumi-cloud`

Singer tap for Pulumi Cloud.

Built with the [Meltano Singer SDK](https://sdk.meltano.com).

## Capabilities

* `catalog`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`

> **Note**
> Incremental replication is not supported by any streams, so the `state` capability is not supported by this tap.

## Settings

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| token               | True     | None    | API Token for Pulumi Cloud |
| organizations       | True     | None    | List of organizations to sync |
| start_date          | False    | None    | Earliest datetime to get data from |
| requests_cache      | False    | None    | Cache configuration for HTTP requests |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |

A full list of supported settings and capabilities is available by running: `tap-pulumi-cloud --about`

### Source Authentication and Authorization

See https://www.pulumi.com/docs/reference/cloud-rest-api/#authentication.

## Usage

You can easily run `tap-pulumi-cloud` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-pulumi-cloud --version
tap-pulumi-cloud --help
tap-pulumi-cloud --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and then run:

```bash
poetry run pytest
```

You can also test the `tap-pulumi-cloud` CLI interface directly using `poetry run`:

```bash
poetry run tap-pulumi-cloud --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-pulumi-cloud
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-pulumi-cloud --version

# OR run a pipeline:
meltano run tap-pulumi-cloud target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
