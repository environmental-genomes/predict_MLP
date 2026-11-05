# External Validation of MLP model

## 1. The 20 Input Genomes

| No. | Genome / NCBI                                                                   | Species                             | Strain            | Reference group |
| --- | ------------------------------------------------------------------------------- | ----------------------------------- | ----------------- | --------------- |
| 1   | [GCF_000005845.2](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000005845.2/) | Escherichia coli                    | K-12 MG1655       | NPA             |
| 2   | [GCF_000006765.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000006765.1/) | Pseudomonas aeruginosa              | PAO1              | NPA             |
| 3   | [GCF_000008405.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000008405.1/) | Mesomycoplasma hyopneumoniae        | 232               | NPA             |
| 4   | [GCF_000008565.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000008565.1/) | Deinococcus radiodurans             | R1                | NPA             |
| 5   | [GCF_000009045.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000009045.1/) | Bacillus subtilis subsp. subtilis   | 168               | NPA             |
| 6   | [GCF_000009425.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000009425.1/) | Lactococcus cremoris                | MG1363            | NPA             |
| 7   | [GCF_000013425.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000013425.1/) | Staphylococcus aureus subsp. aureus | NCTC 8325         | NPA             |
| 8   | [GCF_000015005.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000015005.1/) | Mycolicibacterium smegmatis         | mc²155 (MC2 155) | NPA             |
| 9   | [GCF_000091545.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000091545.1/) | Thermus thermophilus                | HB8               | NPA             |
| 10  | [GCF_000203835.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000203835.1/) | Streptomyces coelicolor             | A3(2)             | NPA             |
| 11  | [GCA_048284325.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_048284325.1/) | Flavobacterium esculini             | LB1P62            | PAc             |
| 12  | [GCA_048284335.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_048284335.1/) | Flavobacterium amylolyticum         | LB2P44            | PAc             |
| 13  | [GCA_048284345.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_048284345.1/) | Flavobacterium glucosi              | LB2P6             | PAc             |
| 14  | [GCA_048286515.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_048286515.1/) | Flavobacterium rhamnosi             | XS2P39            | PAc             |
| 15  | [GCA_048286555.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_048286555.1/) | Flavobacterium cryophilum           | GT2P42            | PAc             |
| 16  | [GCA_048286615.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_048286615.1/) | Flavobacterium pasteuri             | LS1P3             | PAc             |
| 17  | [GCA_048286715.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_048286715.1/) | Flavobacterium kochi                | ZS1P14            | PAc             |
| 18  | [GCA_048286755.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_048286755.1/) | Flavobacterium labens               | LB3P6             | PAc             |
| 19  | [GCA_048286775.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_048286775.1/) | Flavobacterium glycogeni            | ZB4P13            | PAc             |
| 20  | [GCA_048286795.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_048286795.1/) | Flavobacterium frigidum             | XS1P32            | PAc             |

## 2. Environment, Origin, and Temperature Information

### 2.1 NPA: 10 Reference Genomes

| Genome          | Species                        | Strain      | Environment              | Source           | Topt (°C) | NCBI link                                             | fasta_name                         |
| --------------- | ------------------------------ | ----------- | ------------------------ | ---------------- | ---------- | ----------------------------------------------------- | ---------------------------------- |
| GCF_000005845.2 | Escherichia coli               | K-12 MG1655 | Host-associated          | human faces      | 37         | https://www.ncbi.nlm.nih.gov/assembly/GCF_000005845.2 | GCF_000005845.2_ASM584v2_protein   |
| GCF_000006765.1 | Pseudomonas aeruginosa         | PAO1        | Environmental / pathogen | Human wound      | 30–37     | https://www.ncbi.nlm.nih.gov/assembly/GCF_000006765.1 | GCF_000006765.1_ASM676v1_protein   |
| GCF_000008405.1 | Thermotoga maritima            | MSB8        | Hydrothermal vent        | Marine sediment  | 80         | https://www.ncbi.nlm.nih.gov/assembly/GCF_000008405.1 | GCF_000008405.1_ASM840v1_protein   |
| GCF_000008565.1 | Methanocaldococcus jannaschii  | DSM 2661    | Hydrothermal vent        | Deep-sea vent    | 85         | https://www.ncbi.nlm.nih.gov/assembly/GCF_000008565.1 | GCF_000008565.1_ASM856v1_protein   |
| GCF_000009045.1 | Bacillus subtilis              | 168         | Soil                     | Soil             | 30–37     | https://www.ncbi.nlm.nih.gov/assembly/GCF_000009045.1 | GCF_000009045.1_ASM904v1_protein   |
| GCF_000009425.1 | Geobacillus stearothermophilus | ATCC 7953   | Thermophilic soil        | Compost / soil   | 60–65     | https://www.ncbi.nlm.nih.gov/assembly/GCF_000009425.1 | GCF_000009425.1_ASM942v1_protein   |
| GCF_000013425.1 | Staphylococcus aureus          | NCTC 8325   | Host-associated          | Clinical isolate | 37         | https://www.ncbi.nlm.nih.gov/assembly/GCF_000013425.1 | GCF_000013425.1_ASM1342v1_protein  |
| GCF_000015005.1 | Mycobacterium smegmatis        | MC2 155     | Soil                     | Soil             | 37         | https://www.ncbi.nlm.nih.gov/assembly/GCF_000015005.1 | GCF_000015005.1_ASM1500v1_protein  |
| GCF_000091545.1 | Thermus thermophilus           | HB8         | Hot spring               | Hot spring       | 70         | https://www.ncbi.nlm.nih.gov/assembly/GCF_000091545.1 | GCF_000091545.1_ASM9154v1_protein  |
| GCF_000203835.1 | Streptomyces coelicolor        | A3(2)       | Soil                     | Soil             | 28–30     | https://www.ncbi.nlm.nih.gov/assembly/GCF_000203835.1 | GCF_000203835.1_ASM20383v1_protein |

### 2.2 PAc: 10 Type Strains from Glaciers

| Strain | Glacier (all on the Tibetan Plateau, China) | Sample type | Culture collection numbers | Topt (°C) |
| ------ | ------------------------------------------- | ----------- | -------------------------- | ---------- |
| LB1P62 | Laigu Glacier                               | Ice         | CGMCC 1.11346; NBRC 114817 | 14–20     |
| LB2P44 | Laigu Glacier                               | Ice         | CGMCC 1.11256; NBRC 114815 | 14–20     |
| LB2P6  | Laigu Glacier                               | Ice         | CGMCC 1.11263; NBRC 114816 | 14–20     |
| XS2P39 | Zhuxi Glacier                               | Meltwater   | CGMCC 1.23204; NBRC 115054 | 14–20     |
| GT2P42 | Gawalong Glacier                            | Cryoconite  | CGMCC 1.24821; NBRC 114831 | 14         |
| LS1P3  | Laigu Glacier                               | Meltwater   | CGMCC 1.11474; NBRC 114821 | 14–20     |
| ZS1P14 | Zepu Glacier                                | Meltwater   | CGMCC 1.24093; NBRC 114828 | 14–20     |
| LB3P6  | Laigu Glacier                               | Ice         | CGMCC 1.11428; NBRC 114818 | 14–20     |
| ZB4P13 | Zepu Glacier                                | Ice         | CGMCC 1.24050; NBRC 115056 | 14–20     |
| XS1P32 | Zhuxi Glacier                               | Meltwater   | CGMCC 1.23370; NBRC 115055 | 14–20     |

## 3. Validation Workflow

The server workflow is as follows:

**Protein FAA → gapseq pathway results → an aligned matrix of 3,156 binary features → preprocessing for the deployed model → MLP three-class prediction.**

[final_predictions.csv](final_predictions.csv) contains the final prediction results. Its column headers are defined below:

| Field               | Meaning                                        |
| ------------------- | ---------------------------------------------- |
| `sample`          | Sample ID corresponding to the input file      |
| `predicted_class` | Class predicted by the model: NPA, PAc, or PAd |
| `max_probability` | Maximum of the three class probabilities       |
| `probability_NPA` | Probability of class NPA                       |
| `probability_PAc` | Probability of class PAc                       |
| `probability_PAd` | Probability of class PAd                       |

## 4. Validation Results for the 20 Samples

| Reference class | Number of samples | Correct predictions | Recall          |
| --------------- | ----------------- | ------------------- | --------------- |
| NPA             | 10                | 8                   | 80.00%          |
| PAc             | 10                | 10                  | 100.00%         |
| PAd             | 0                 | —                  | Not estimable   |
| Total           | 20                | 18                  | 90.00% accuracy |

Rows of the confusion matrix represent reference groups, and columns represent predicted classes:

| Reference / Predicted | NPA | PAc | PAd |
| --------------------- | --- | --- | --- |
| NPA                   | 8   | 0   | 2   |
| PAc                   | 0   | 10  | 0   |
| PAd                   | 0   | 0   | 0   |

Results for individual genomes are shown below:

| Genome          | Reference group | Predicted class | Maximum class probability | Result    |
| --------------- | --------------- | --------------- | ------------------------- | --------- |
| GCF_000005845.2 | NPA             | NPA             | 0.993681                  | Correct   |
| GCF_000006765.1 | NPA             | NPA             | 0.998113                  | Correct   |
| GCF_000008405.1 | NPA             | NPA             | 0.846651                  | Correct   |
| GCF_000008565.1 | NPA             | NPA             | 0.532886                  | Correct   |
| GCF_000009045.1 | NPA             | PAd             | 0.799587                  | Incorrect |
| GCF_000009425.1 | NPA             | NPA             | 0.491979                  | Correct   |
| GCF_000013425.1 | NPA             | NPA             | 0.812197                  | Correct   |
| GCF_000015005.1 | NPA             | PAd             | 0.574619                  | Incorrect |
| GCF_000091545.1 | NPA             | NPA             | 0.409268                  | Correct   |
| GCF_000203835.1 | NPA             | NPA             | 0.889537                  | Correct   |
| GCA_048284325.1 | PAc             | PAc             | 0.918528                  | Correct   |
| GCA_048284335.1 | PAc             | PAc             | 0.994068                  | Correct   |
| GCA_048284345.1 | PAc             | PAc             | 0.984830                  | Correct   |
| GCA_048286515.1 | PAc             | PAc             | 0.783703                  | Correct   |
| GCA_048286555.1 | PAc             | PAc             | 0.986466                  | Correct   |
| GCA_048286615.1 | PAc             | PAc             | 0.976790                  | Correct   |
| GCA_048286715.1 | PAc             | PAc             | 0.911464                  | Correct   |
| GCA_048286755.1 | PAc             | PAc             | 0.993558                  | Correct   |
| GCA_048286775.1 | PAc             | PAc             | 0.951716                  | Correct   |
| GCA_048286795.1 | PAc             | PAc             | 0.980966                  | Correct   |

The reference group for `GCF_000009045.1_ASM904v1_protein` and `GCF_000015005.1_ASM1500v1_protein` is NPA, and both are predicted as PAd.

Since this model was trained strictly on a three-class dataset of 8075 genomes, its predictions also comprise three classes: NPA, PAd, and PAc. The [github.com/ZhuGuoLiang-gi/CryoClass](https://github.com/ZhuGuoLiang-gi/CryoClass) model focuses more on whether an input microbial genome belongs to the PAc class, so its predictions are binary: PAc and non-PAc.
