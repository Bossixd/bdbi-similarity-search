import pandas as pd

sequences_df = pd.read_csv('c_elegans_tflink.csv')

tfs = ["TFLinkLS00543756;Q93560;blmp-1;ce10;chrX:5716076-5716086"]

sequence = sequences_df[sequences_df['id'] == tfs[0].split(';')[0]].iloc[0]['sequence']
print(sequence)
