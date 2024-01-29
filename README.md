# Konveyor AI (kai)

Konveyor AI (kai) is Konveyor's approach to easing modernization of application source code to a new target by leveraging LLMs with guidance from static code analysis.

Pronounciation of 'kai': https://www.howtopronounce.com/kai

### Approach

Our approach is to use static code analysis to find the areas in source code that need to be transformed. 'kai' will iterate through analysis information and work with LLMs to generate code changes to resolve incidents identified from analysis.

This approach does _not_ require fine-tuning of LLMs, we augment a LLMs knowledge via the prompt, similar to approaches with [RAG](https://arxiv.org/abs/2005.11401) by leveraging external data from inside of Konveyor and from Analysis Rules to aid the LLM in constructing better results.

For example, [analyzer-lsp Rules](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md) such as these ([Java EE to Quarkus rulesets](https://github.com/konveyor/rulesets/tree/main/default/generated/quarkus)) are leveraged to aid guiding a LLM to update a legacy Java EE application to Quarkus.

## Getting Started

### Setup

1. `python3 -m venv env`
2. `source env/bin/activate`
3. `pip install -r ./requirements.txt`

### Run an analysis of a sample app (example for MacOS)

1. Install [podman](https://podman.io/) so you can run [Kantra](https://github.com/konveyor/kantra) for static code analysis
1. `cd samples`
1. `./fetch_sample_apps.sh` # this will git clone example source code apps
1. `cd macos`
1. `./restart_podman_machine.sh` # setups the podman VM on MacOS so it will mount the host filesystem into the VM
1. `./get_latest_kantra_cli.sh` # fetches 'kantra' our analyzer tool and stores it in ../bin
1. `cd ..`
1. `./analyze_coolstore.sh` # Analyzes 'eap-coolstore-monolith' directory and writes an analysis output to [analysis_reports/eap-coolstore-monolith/output.yaml](/samples/analysis_reports/eap-coolstore-monolith/output.yaml)
   - There are a few other scripts in this directory to analyze other samples

We plan to keep latest versions of static code analyis committed to this repo in [samples/analysis_reports](samples/analysis_reports)

## Contributing

### Linting

1. Install trunk via: https://docs.trunk.io/check#install-the-cli
1. Run the linters: `trunk check`
1. Format code: `trunk fmt`

### Testing

#### How to run regression tests

1. Install the prereqs in Setup and activate the python virtual environment
2. Ensure you've checked out the source code for sample applications: Run: [./samples/fetch_sample_apps.sh](./samples/fetch_sample_apps.sh)
3. Run: [./run_tests.sh](./run_tests.sh)

## Prototype

This repository represents a prototype implementation as the team explores the solution space. The intent is for this work to remain in the konveyor-ecosystem as the team builds knowledge in the domain and experiments with solutions. As the approach matures we will integrate this properly into Konveyor and seek to promote to github.com/konveyor organization.

## Code of Conduct

Refer to Konveyor's Code of Conduct [here](https://github.com/konveyor/community/blob/main/CODE_OF_CONDUCT.md).
