import re

example = """FASTA searches a protein or DNA sequence data bank
 version 36.3.8i May, 2023
Please cite:
 W.R. Pearson & D.J. Lipman PNAS (1988) 85:2444-2448

Query: sequence
  1>>>sequence1 - 111 nt
Library: c_elegans_tflink.fasta
  1096531 residues in  9905 sequences

Statistics: MLE_cen statistics: Lambda= 0.1314;  K=0.05254 (cen=876)
 statistics sampled from 4412 (4415) to 4412 sequences
Algorithm: FASTA (3.8 Nov 2011) [optimized]
Parameters: +5/-4 matrix (5:-4), open/ext: -12/-4
 ktup: 6, E-join: 0.25 (0.656), E-opt: 0.05 (0.252), width:  16
 Scan time:  0.100

The best scores are:                                      opt bits E(9905)
TFLinkLS00543757;Q93560;blmp-1;ce10;chrII:1307 ( 111) [f]  555 111.5 3.4e-26
TFLinkLS00546532;Q93560;blmp-1;ce10;chrV:13892 ( 111) [f]  119 28.8    0.26
TFLinkLS07120251;P34707;skn-1;ce10;chrV:138928 ( 115) [f]  118 28.6     0.3
TFLinkLS00545947;Q93560;blmp-1;ce10;chrI:37237 ( 111) [f]  106 26.3     1.4

111 residues in 1 query   sequences
1096531 residues in 9905 library sequences
 Tcomplib [36.3.8i May, 2023] (2 proc in memory [0G])
 start: Sat Mar  1 23:36:42 2025 done: Sat Mar  1 23:36:42 2025
 Total Scan time:  0.100 Total Display time:  0.000

Function used was FASTA [36.3.8i May, 2023]"""

def parse_fasta(output):
    start = re.search("The best scores are:", output)
    end = re.search("[0-9]+ residues in +[0-9]+ query", output)
    
    buffer = output[start.end():end.start() - 2]
    buffer = buffer.split('\n')[1:]
    
    tfs = [x.split(' ')[0] for x in buffer]
    scores = [float(x.split(' ')[-1]) for x in buffer]
    
    return_list = []
    for i in range(len(tfs)):
        return_list.append({
            "tf": tfs[i],
            "score": scores[i]
        })
    return return_list
    
print(parse_fasta(example))