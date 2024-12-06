# T1-CICD

## High-Level Design

![High-Level Design](./images/system_diagram_week6.png)

## Sequence Diagram

### Pipeline Run

![High-Level Design](./images/sequence_diagram_pipeline_run.png)

## Components

### CLI

#### cicd

- Usage: cicd [OPTIONS] COMMAND [ARGS]...

    This command is the entry point to the CLI. It can be used to check the
    config file, perform a dry run, or run a pipeline.

  - Options:
    - -c, --check              Check config file.
    - -dr, --dryrun            Dry run.
    - -cf, --config-file TEXT  Path to config file.
    - -h, --help               Show help message and exit
  - Commands:
    - report  Show a report of a pipeline.
    - run     Run a specific pipeline or override the config file in a repository.
    - stop    Stop a specific pipeline in a repository.

##### cicd report

- Usage: cicd report [OPTIONS]

 	 Show a report of a pipeline.
 	
 	 If no options are specified, show a report of all pipelines.
 	
 	 If --pipeline is specified, show a report of the pipeline.
 	
 	 If --run is specified, show a report of the run.
 	
 	If --stage is specified, show a report of the stage.
 	
 	If --job is specified, show a report of the job.

- Options:
  - -r, --repo TEXT      Repository path.  [required]
  - -l, --local          Run locally.
  - -p, --pipeline TEXT  Pipeline name.
  - -rn, --run TEXT      Run number.
  - -s, --stage TEXT     Stage name.
  - -j, --job TEXT       Job name.
  - -h, --help           Show help message and exit.

##### cicd run

- Usage: cicd run [OPTIONS]

  Run a specific pipeline or override the config file in a repository.
  
    If --override is specified, override the config file with the new config.
  
    if either --pipeline or --file is specified, run the specific pipeline.
  
    Otherwise, run all pipelines in the repository.
  
- Options:

  - -r, --repo TEXT      Repository path.  [default: (current local directory)]
  - -l, --local          Run locally.
  - -b, --branch TEXT    Branch name.  [default: (main branch)]
  - -c, --commit TEXT    Commit hash.  [default: (the latest commit)]
  - -p, --pipeline TEXT  Pipeline name.
  - -f, --file TEXT      Path to config file.
  - -o, --override TEXT  Override config file.
  - -h, --help           Show this message and exit.


##### cicd stop

- Usage: cicd stop [OPTIONS]

  	Stop a specific pipeline in a repository.
    if either --pipeline or --file is specified, stop the specific pipeline.
    Otherwise, stop all pipelines in the repository.

- Options:
  - -r, --repo TEXT    Repository path.  [default: (current local directory)]
  - -l, --local        Run locally.
  - -b, --branch TEXT  Branch name.  [default: (main branch)]
  - -c, --commit TEXT  Commit hash.  [default: (the latest commit)]
  - -p, --pipeline TEXT  Pipeline name.
  - -f, --file TEXT      Path to config file.
  - -h, --help         Show help message and exit.

### Rest API

![1729643497158](./images/1729643497158.jpg)

## Getting Started

#### Build the project

```bash
$ poetry install
```

#### Run server

```bash
$ poetry run server # It will be packaged and added to system env.
```

#### Run CLI

```bash
$ poetry run cicd # It will be packaged and added to system env. 
```

#### Run tests

```bash
$ poetry run pytest
```

#### Run test coverage

```bash
$ poetry run coverage report
```

#### Run static analysis

```bash
$ poetry run pylint src
```

#### Generate documents

```bash
$ poetry run pdoc src
```

