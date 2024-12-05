# Multiple Sequence Ali/Alpha Fold
## Streamlining the MSA building stages

## installation
### External dependencies
MSAF uses the following tools:
-  [mmseqs2](https://github.com/soedinglab/MMseqs2) for database search
-  [mafft](https://mafft.cbrc.jp/alignment/software/) for multiple sequence alignment
You will need those two sotware installed
### Python package
Just, `pip install msaf`

### Global setup 
MSAF requires a configuration file as first parameter.
This configuration file is under yaml format of the following shape
```yaml
databases : 
  - /path/to/databases/mmseqs
executables:
  mafft: /usr/local/bin/mafft
  mmseqs: /opt/homebrew/bin/mmseqs
settings:
  cache : /path/to/msaf/cache
cocktails:
    test:
        ingredients:
        - target: swissprot
            label: pif.sto
        - target: uniprot
            label: paf.a3m
```
Where,
* `databases` is a list of folder, where MSAF recursively looks for mmseqs database
* `executables` are key, value of paths to executable external dependencies
* `cache` points to a folder used to store MSAF mess, it MUST exist
* `cocktails` is dictionary of recipes

#### MSAF recipes
Recipes are declared in the configuration file. A recipe is caracterized by a name (eg:`test`) and `ingredients`. `ingredients` define database search and save schema as list of `target` and `label`. The `target` key defines the database to search and `label` defines the resulting msa file (and format).
Recipes feature an optional `PDQT` parameter, which if set to `TRUE` will wrap all a3m files in an [aligned.pdqt file](https://github.com/chaidiscovery/chai-lab)

In the above exemple, the `test` recipe will trigger a search in swissprot and uniprot for all supplied queries. 
- The result of swissprot search will be save under stockholm format in a file named `pif.sto`
- The result of the uniprot search will be save under a3m format in a file named `paf.a3m`


## Usage

### List available database
At startup, MSAF will recurively search inside all `databases` item found in configuration file for mmseqs database files (*<database_name>_h*, *<database_name>_.index*, *<database_name>.lookup*, *<database_name>.index*).

The registred <database_name> can be displayed with
`python -m msaf config.yaml --list`

### run a search
`python -m msaf config.yaml --query query1.fasta query2.fasta --bp test`
With `--bp` refering to one recipe defined in the config file and `--query` to absolute path(s) of query sequence file(s) (fasta format).
#### Multimer search
Results will be saved in the `--output` folder (msas, by default) with subfolders using sequential one letter chain identifier along the sequence of query files. If the same file is provided more than once as a query, only one folder will be created. Hence, results of an homodimer search will be stored under a single `A/` subfolder.


