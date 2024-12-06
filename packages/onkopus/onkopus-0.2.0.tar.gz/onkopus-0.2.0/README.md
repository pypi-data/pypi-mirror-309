
![Onkopus](https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus/-/raw/main/assets/onkopus_logo_v0.1.4.2_150.png?inline=false)

# Onkopus: A modular variant interpretation framework

[![pipeline](https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus/badges/main/pipeline.svg)](https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus) |
[![commits](https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus/-/jobs/artifacts/main/raw/commits.svg?job=build_badges)](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes)
[![license](https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus/-/jobs/artifacts/main/raw/license.svg?job=build_badges)](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes)
[![coverage](https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus/badges/main/coverage.svg)](https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus)
[![python_version](https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus/-/jobs/artifacts/main/raw/python_version.svg?job=build_badges)](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes)
[![release](https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus/-/badges/release.svg)](https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus)

## What is Onkopus?

Onkopus is an easy-to-use cancer variant interpretation framework to annotate, interpret 
and prioritize genetic alterations in cancer. 
Onkopus provides annotation for different mutation types including a wide range of features, including 
genomic, transcriptomic and protein information, biochemical features, pathogenicty prediction, 
functional effect prediction, biochemical features, and clinical significance of treatments on 
molecular targets. 

## Installation

Install the main Onkopus package:
```bash
python -m pip install onkopus
```

## Usage

### Use Onkopus from the command line

Onkopus provides a command line tool to directly annotate variant files. 
Run the ```onkopus``` tool by specifying an input file (`-i`) and the genome version (`-g`). 
Optionally pass an output file (`-o`) and specific modules (`-m`):  
```bash
onkopus run -i somatic_mutations.vcf -g hg38

onkopus run -i somatic_mutations.vcf -g hg38 -m alphamissense
onkopus run -i somatic_mutations.vcf -g hg38 -m revel,primateai
```

### Use Onkopus from Python

Use Onkopus from Python by running the full annotation pipeline or instantiate 
custom Onkopus clients and calling `process_data`:

#### Annotate variants with all modules

For a complete variant annotation, including functional and clinical annotation, run

```python
import onkopus as op

bframe = op.read_file('./somatic_mutations.vcf', genome_version="hg38", input_format="vcf")
bframe = op.annotate(bframe)
```



#### Annotate with specific modules

```python
import onkopus as op

genome_version="hg38"
bframe = op.read_file('./somatic_mutations.vcf', input_format='vcf')

# Annotate with ClinVar
client = op.ClinVarClient(genome_version=genome_version)
bframe.data = client.process_data(bframe.data)

# Annotate with REVEL
client = op.REVELClient(genome_version=genome_version)
bframe.data = client.process_data(bframe.data)

op.write_file('./somatic_mutations.annotated.vcf', bframe)
```



## License

GPLv3

## Documentation

The official documentation on how to use the Onkopus Python package is hosted on the public [Onkopus website](https://mtb.bioinf.med.uni-goettingne.de/onkopus). 

## Public version

A public instance of Onkopus Web is available at [https://mtb.bioinf.med.uni-goettingen.de/onkopus](https://mtb.bioinf.med.uni-goettingen.de/onkopus). 
