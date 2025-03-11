import pandas as pd

# with open('c_elegans_tflink.fasta', 'r') as f:
#     # while file is not over
#     arr = []
#     sequence = ""
#     name = ""
#     while True:
#         line = f.readline()
#         if not line:
#             break
#         if line.startswith('>'):
#             arr.append([id, sequence])
#             sequence = ""
#             id = line.split(';')[0][1:]
#         else:
#             sequence += line.strip()
#     pd.DataFrame(arr[1:]).to_csv('c_elegans_tflink.csv', index=False)

sequences_df = pd.read_csv('c_elegans_tflink.csv')
