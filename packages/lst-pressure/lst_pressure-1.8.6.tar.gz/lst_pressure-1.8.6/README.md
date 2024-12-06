# lst-pressure

Python module for calculating LST pressure based on scheduled observations

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Motivation](#motivation)
  - [Design](#design)
  - [Normalizing intervals](#normalizing-intervals)
  - [Customising interval calculations](#customising-interval-calculations)
- [Usage and installation](#usage-and-installation)
  - [Command line interface (CLI)](#command-line-interface-cli)
    - [CLI Examples](#cli-examples)
  - [Direct API usage](#direct-api-usage)
- [Local development](#local-development)
  - [PyEnv](#pyenv)
  - [csvkit](#csvkit)
  - [Testing](#testing)
  - [Publishing](#publishing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Motivation

Observation blocks encompass various time-related constraints, notably the Local Sidereal Time (LST) window of a source rise/fall, and some constraints related to UTC. As LST and UTC time can diverge over a year, it can be hard to quickly identify candidate UTC times based on LST ranges in conjunction with constraints related to sun/UTC.

This library should facilitate easily comparing intervals defined in LST with intervals defined in UTC. Essentially this library is an opinionated wrapper over a Python implementation of an [interval tree](https://en.wikipedia.org/wiki/Interval_tree) called [intervaltree](https://pypi.org/project/intervaltree/).

## Design

Each UTC day includes intervals in which an observation can be scheduled. These intervals are called:

- `ALL_DAY`
- `DAY`
- `SUNRISE_SUNSET`
- `SUNSET_SUNRISE`
- `NIGHT`

To identify the UTC intervals that satisfy scheduling constraints of observations, generate a list of LST intervals over `N` days, that are labelled with UTC information. For example:

```
[ lst_t0 : lst_t1 ]: { type: <SUNRISE_SUNSET>, utc_0, utc_1 }
[ lst_t0 : lst_t1 ]: { type, utc_0, utc_1 }
[ lst_t0 : lst_t1 ]: { type, utc_0, utc_1 }
[ lst_t0 : lst_t1 ]: { type, utc_0, utc_1 }
[ lst_t0 : lst_t1 ]: { type, utc_0, utc_1 }
... etc
```

Then, for an observation with an LST window defined, query that list for all intervals that overlap the observation LST window. The resultant list can then be filtered by UTC-related information such as sunset/sunrise and other constraints (i.e. observation duration). **Noted that the LST window in the context of this package defines possible _start_ times of observations. It's up to the user to ensure that the start time of an observation takes into account the required observation duration.**

The result is a list of UTC calendar days that a particular observation can be scheduled along with UTC start/end times for applicable observations. Done for many observations, it's easy to create a UTC calendar with potential observation events that can serve as the basis for more complicated scheduling logic (for example, picking the best observation to schedule on a particular day).

## Normalizing intervals

Intervals should strictly have `t1 > t0`, which means that in some cases intervals defined by two LST times must be normalized. For example, an LST range that begins on day0 and ends on day1 will have a start time that is higher than the end time. In this case, add a full LST day to the end time at both indexing time and at query time. Likewise, when an interval - for example `NIGHT` - begins on the preceding day, the portion of the interval that falls on the current day is indexed.

For any given day, intervals are created starting at 00:00, and spilling over into the next day. This means that there are overlapping intervals when considering multiple days. For example, since for day = N there are two night intervals, these intervals are actually the same period of time:

- date N: N.dusk -> N.dusk -> (N + 1).dawn (captured as `21 -> 34`)
- Date (N + 1): 00:00 -> (N + 1).dawn (captured as `0 -> 7`)

Without the additional early interval, it would be impossible to match early LST observation windows (for example `02:00 -> 03:30`) since early morning, calculated from the night before, is `> 24`.

## Customising interval calculations

By default this tool will calculate intervals that correspond to sunset/sunset times as available on the OPT tool, with the "NIGHT" interval equal to the "SUNSET_SUNRISE" interval (there is no concept of a NIGHT interval when calculating intervals using the default MeerKAT provider). For more general interval calculations, you can configure the tool to calculate sun statistics and intervals using the popular [Astral](https://github.com/sffjunkie/astral) package either via a CLI flag or specifying configuration within Python:

**_Python_**

```python
from lstpressure import LocationProviderType, LSTConf
LSTConf().LOC_PROVIDER = LocationProviderType.ASTRAL

# ... See below for usage examples
```

**_CLI_**

```sh
cat opt-csv.csv | lstpressure --loc-provider ASTRAL observables # See below for more examples
```

# Usage and installation

The lst-pressure package currently supports **_Python version 3.12_**

## Command line interface (CLI)

The CLI wraps the `LST` module, allowing for running the `lstpressure` application with OPT CSV download as input. Use the lstpressure CLI outside of Python environments (requires Docker, as the distribution is as a Docker image). The CLI also allows for specifying the provider for calculation sun statistics per location. By default all sun information is relative to the MeerKAT telescope. Via the CLI you can specify arbitrary lat/long locations for calculating UTC intervals.

To use, ensure that [Docker Engine](https://docs.docker.com/engine/) is installed (or Docker Desktop for non-Linux users). It's also necessary to login to the GitHub Container Registry (ghcr.io):

```sh
# Navigate to https://github.com/settings/tokens and generate a 'classic' token with the "read:packages" scope selected (copy the value)
docker login ghcr.io
# Username: Your GitHub username
# Password: <token value>

# Install the lstpressure CLI
docker pull ghcr.io/ska-sa/lst-pressure_dist:latest \
  && docker \
    run \
      --rm \
      ghcr.io/ska-sa/lst-pressure_dist:latest install \
        | bash

# (or uninstall the lstpressure CLI)
docker pull ghcr.io/ska-sa/lst-pressure_dist:latest \
  && docker \
    run \
      --rm \
      ghcr.io/ska-sa/lst-pressure_dist:latest uninstall \
        | bash

# To update, pull the latest docker image (or a specific tag)
docker pull ghcr.io/ska-sa/lst-pressure_dist:latest

# Run the CLI
lstpressure --help
```

### CLI Examples
Download the observations in CSV form from [apps.sarao.ac.za/opt/observations](https://apps.sarao.ac.za/opt/observations), and rename the file to `observations.csv` to work with these examples.

```sh
# Print instructions
lstpressure
lstpressure <cmd> -h

# Get a list of today's schedulable observations
cat observations.csv | lstpressure obs

# ... And format the result nicely using csvlook. It's hard to imaging using this tool without --pretty. To use csvlook with custom args, just omit the --pretty flag
cat observations.csv | lstpressure obs --pretty

# ... By default --pretty will truncate long values. If you want the full output specify --no-trunc
cat observations.csv | lstpressure obs --pretty --no-trunc

# Get a list of schedulable observations over the next 3 months (including this month)
cat observations.csv | lstpressure obs --end="+2M" --pretty

# Get a list of schedulable NIGHT observations over the next 3 months
cat observations.csv | lstpressure obs --end="+2M" --filter night --pretty

# Get a list of schedulable NIGHT observations over the next 3 months, aggregated by opportunities per month
cat observations.csv | lstpressure obs --end="+2m" --filter night --aggregate observables-by-month.duckdb --pretty

# Get a list of schedulable NIGHT observations over the next 7 days, aggregated by opportunities per day
cat observations.csv | lstpressure obs --end="+7d" --filter night --aggregate observables-by-day.duckdb --pretty

# Or split the above steps for bespoke SQL aggregation
cat observations.csv | lstpressure obs --end="+2m" --filter night > night_obs_next_3m.csv --pretty
cat night_obs_next_3m.csv | lstpressure agg --query observables-by-month.duckdb --pretty

# Use the DuckDB query engine by specifying a query that includes "duckdb", or including "duckdb" in a comment in a query
cat night_obs_next_3m.csv | lstpressure agg --query observables-by-month.duckdb --pretty
# or..
cat night_obs_next_3m.csv | lstpressure agg --query "select * from stdin -- duckdb" --pretty

# Write bespoke aggregations (SQLite syntax, in the case of multiple statements, the last is returned)
cat night_obs_next_3m.csv | lstpressure agg --query "select * from stdin;" --pretty

# Interrogate what the "observables-by-month.duckdb" query looks like
lstpressure agg --query observables-by-month.duckdb --echo

# .. Write your own SQL in a file
# Using the CLI via the Docker image requires filepaths to be specified as absolute paths, i.e. --query $(pwd)/my-report.sql
echo "select * from stdin;" > my-report.sql
cat night_obs_next_3m.csv | lstpressure agg --query $(pwd)/my-report.sql # or ...
cat observations.csv | lstpressure obs --end="+2m" --filter night --aggregate $(pwd)/my-report.sql
```

The aggregation tool just wraps the [csvkit (csvsql)](https://csvkit.readthedocs.io/en/latest/scripts/csvsql.html) program. Other tools can easily be integrated into this CLI in the future. Two SQL engines are currently supported - [DuckDB](https://duckdb.org/) and [SQLite](https://www.sqlite.org/index.html). `DuckDB` is more versatile as an aggregation framework for it's support of [dynamic pivoting](https://duckdb.org/docs/archive/0.9.2/sql/statements/pivot).

## Direct API usage

Install from [PyPi](https://pypi.org/project/lst-pressure/):

```sh
pip install lst-pressure
```

Then use the `lst` module ([API Docs](https://ska-sa.github.io/lst-pressure/) are available)

```py
import lstpressure as lst
import pandas as pd

# Specify the provider for calculating sun stats (defaults to bespoke logic for MeerKAT, to match the OPT tool times)
lst.LSTConf().LOC_PROVIDER = lst.LocationProviderType.MEERKAT

START = "20231108"
END = "20231208"


# Filter for specific rows in the CSV
def observation_filter(observation: lst.Observation):
    if lst.LSTIntervalType.NIGHT in observation.utc_constraints:
        return True
    return False


# Specifying a filter on observations requires
# processing the entire CSV file (and doing sun calculations
# on each row). If it's slow, a lot less work is done if
# you filter on input
def input_filter(row: pd.Series):
    night_only: str = row.iloc[15]
    if night_only.strip().lower() == "yes":
        return True
    return False


lst.LST(
    input="./observations.csv",
    calendar_start=START,
    calendar_end=END,
    # input_filter=input_filter,
    observation_filter=observation_filter,
).to_csv_file(f"lst-pressure-{START}-{END}.csv")

# ... Or provide input as a pandas.DataFrame instance
# ... Or provide input as a list[list[Any]]

```

It's also possible to work with the underlying `Observation`, `LSTCalendar`, `LSTInterval` types directly. For the most part this should not be required, however it does allow for using the `lstpressure.is_observable` function. In terms of implementation, we don't use the OPT observations download directly but instead use instances of the `lstpressure.Observation` class so as to decouple the application logic from the CSV structure.

```python
import lstpressure

# Define an observation
observation = lstpressure.Observation(
  id="some-id",
  lst_window_start=2,
  lst_window_end=12,
  utc_constraints=[lstpressure.lstindex.LSTIntervalType.NIGHT],
  duration=2
)

# Test if it can be scheduled on a date
is_valid = lstpressure.is_observable(observation, "20231031")

# ... or within a date range
is_valid = lstpressure.is_observable(observation, "20231031", "20231105")

# ... or test multiple observations against a calendar
calendar = lstpressure.LSTCalendar('20231001', '20231001')
is_obs1_valid = lstpressure.is_observable(Observation(...), calendar)
is_obs2_valid = lstpressure.is_observable(Observation(...), calendar)
is_obs3_valid = lstpressure.is_observable(Observation(...), calendar)

# ... or get a list of dates that an observation can be scheduled on
observables = [
    o # use o.to_tuple() for CSV values, or access the interval/observation via the observable instance
    for o in lstpressure.LSTCalendar(
        "20231001", "20231010", observations=[Observation(...), ...]
    ).observables()
]

# ... or specify the ASTRAL provider for calculations
lstpressure.LSTConf().LOC_PROVIDER = lstpressure.LocationProviderType.ASTRAL
```

# Local development

Ensure that your Python context is `3.12.x`, and run `source env.sh`. this will install project dependencies and add `./bin/lst` to your path.

## PyEnv

So long as your current Python version is 3.12, things should 'just work'. One tool for quickly switching between various Python versions is `pyenv` - to install:

```sh
# PyEnv builds Python versions from source, therefore build dependencies are required
brew install openssl readline sqlite3 xz zlib

# Install pyenv using the pyenv-installer (don't forget to add 'pyenv' to the load path!)
curl https://pyenv.run | bash

# Install python v3.12 using pyenv
pyenv install -v 3.12 # Not mac
arch -x86_64 pyenv install 3.12 # Mac

# Create a pyenv virtual environment
pyenv virtualenv 3.12 py3.12

# Activate your pyenv environment
pyenv activate py3.12
```

... And now your current Python context should be `3.12.x`

## [csvkit](https://csvkit.readthedocs.io/en/latest/)

The current output of lstpressure is quite raw, and some aggregating needs to be done on it. csvsql is a command-line tool provided by the csvkit Python library for performing SQL operations on CSV files. To install csvkit and, consequently, csvsql on your Mac, you can follow these steps:

```sh
# Install csvkit using pip
pip install csvkit

# Verify the installation
csvsql --version
```

This should display the version number of csvsql if the installation was successful.

Now you should be able to use csvsql on your Mac.

## Testing

To test the codebase, run `pytest` in the terminal. For live testing, use the [`chomp`](https://github.com/guybedford/chomp#install) task runner. Install either via Cargo (Rust), or via NPM (Node.js)

```sh
source env.sh
chomp --watch
```

## Publishing

The publish workflow is described in [.github/workflows/publish.yml](.github/workflows/publish.yml), and is triggered on tags pushed to the `main` branch. The published package is available on [PyPI](https://pypi.org/project/lst-pressure/).
