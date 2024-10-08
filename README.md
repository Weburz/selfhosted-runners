# Self-Hosting GitHub Action Runners

This repository contains some scripts (and some Terraform IaC to provision the
resources) to setup
[self-hosted GitHub Action runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners).
The resources available in this repository are used internally at Weburz and is
publicly accessible for anyone interested in using them for their self-hosting
needs (or as a source of reference).

## Disclaimer Before Using the Script

1. You are **REQUESTED** to audit the script and identify any potential issues that
   might affect the system's performance or functionality, on which the script ought to
   be run on. Neither the authors of the script, nor Weburz will be liable to any damage
   caused to your system when running this script.

2. The script requires a working installation of Python (ideally, Python v3.12
   and above) and will **ONLY** download the runners for Linux machines. So, if
   you want the script to run on Windows/MacOS machines, please open a PR with a
   brief description of the changes you want introduced to the script(s).

3. The script also downloads the runners for systems running on x64 machines. A
   future update will _probably_ support a more robust way to automatically
   fetch the appropriate runners to install. Feel free to submit pull requests if you'd
   like to expedite the addition of this functionality.

4. Please note that, in its current form, the script will configure and install _n_
   runners if invoked _n_ times. A future update _may_ change this behavior, so feel
   free to share any suggestions if you have better ideas for managing this process.

## Usage Guidelines

The [`scripts`](./scripts) directory contains some Python files (named
`install.py` and `remove.py`) which are responsible for installing the runners
and removing them from the host VM intelligently. The purpose of the scripts are
to provide its users an efficient way to spin up an arbitrary number of runners
on a single VM in a reproducible manner.

### Provisioning a VM to Host the Runners

The repository contains the necessary Terraform IaC to provision a Virtual
Machine on Azure. We use Azure internally at Weburz hence we provided the IaC in
the `infra` directory with this repository for our particular needs. If you do
not use Azure for infrastructure provisioning, you can skip this section of the
documentation to the next without any hesitation.

Before you can provision a VM, you will have to provide certain variables to
Terraform to add as metadata for the infrastructure. You can do so by creating a
`terraform.tfvars` file and adding all the **REQUIRED** variables in it. For
reference purpose and understanding which variables are required, check out the
[`variables.tf`](./infra/variables.tf) file.

To provision a VM for hosting the runners, run the following command:

```console
terraform init
terraform plan --out="main.tfplan"
terraform apply "main.tfplan"
```

**NOTE**: The `terraform plan` command will automatically detect and pick up the
`terraform.tfvars` file as long as it's named exactly as such and nothing else
(for example, `terraform.example.tfvars` won't work). If you have a differently
named `.tfvars` file, you will have to pass it to the `terraform plan` command
explicitly (see
[the docs](https://developer.hashicorp.com/terraform/cli/commands/plan#var-file-filename)).

With the Virtual Machine provisioned, you will have to access it remotely using
SSH before the runners can be provisioned on them. The following will help in
exactly that regard:

```console
ssh $(terraform output --raw "admin_username")@$(terraform output --raw "public_ip_address")
```

If you could successfully login to the VM, then you are good to go and install
the runners on it.

### Managing up the Runners

To spin up say 4 runners in a VM, run the following command:

```console
curl -fsSL "https://raw.githubusercontent.com/Weburz/selfhosted-runners/main/scripts/install.py" \
    | python - --number=4 --url=<GITHUB-ORGANISATION-URL> --pat=<PERSONAL-ACCESS-TOKEN>
```

**NOTE**: The script by default will spin up a single runner if the optional
positional argument `--number` is missing. Replace `<GITHUB_ORGANISATION-URL>`
with the URL to your GitHub organisation (for example,
`https://github.com/Weburz`) and `<PERSONAL-ACCESS-TOKEN>` with a PAT configured
with `admin` access privileges (see
[ the official docs ](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
for more instructions). The script accepts additional positional arguments which
you can check by invoking the above command as `... | python - --help`

To remove a single runner, run the following command:

```console
curl -fsSL "https://raw.githubusercontent.com/Weburz/selfhosted-runners/main/scripts/remove.py" \
    | python - --runner=<RUNNER-ID>
```

To remove all existing runners from the host VM, run the following command:

```console
curl -fsSL "https://raw.githubusercontent.com/Weburz/selfhosted-runners/main/scripts/remove.py" \
    | python - --all
```

## Development Guidelines

If you find a bug or simply want to recommend some improvements to the source
code in this repository, please be sure to follow the instructions laid down in
this section of the documentations.

1. Open an issue thread with details of the bug/improvement (also specify a fix
   if you are aware of it).
2. If you are contributing a PR or two, please ensure the code is well
   formatted. We use `ruff` and `terraform fmt` to format the source code into a
   standardised community accepted format.
3. If your contribution requires any changes to the documentation or if you
   find some aspects of the project missing from the documentation, please do
   not hesitate to open a PR to update it.

## Usage and Distribution Rights

The source code made available in this repository are subject to the terms and
conditions (T&Cs) of the MIT License. You will find all the necessary licensing
details in the [LICENSE](./LICENSE) document.
