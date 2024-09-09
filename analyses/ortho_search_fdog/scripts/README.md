# Scripts

## Parsing python scripts

The 3 scripts `mod_id_profile.py`, `mod_id_fasta.py` and `mod_id_domains.py` are used to map the seed protein IDs with their enzyme family. Usage:
```
python mod_id_profile.py -i <original_fdog_output.phyloprofile> -m <data/id_mapping.txt>
```
The mapping file `id_mapping.txt` can be found in the *data* folder.

## How to run fDOG

Check `run_fdog.sh` for an example of a slurm script to run fDOG.

**NOTE 1:** please modify the slurm settings according to your needs!

**NOTE 2:** please check the manual of fDOG (using the command `fdog.run -h`) to understand the used parameters

**NOTE 3:** after the run, you can merge the outputs for individual seed proteins into one single output using `fdog.mergeOutput` function
