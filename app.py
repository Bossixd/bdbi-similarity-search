from flask import Flask, request, jsonify
import subprocess
import os
import shlex
import uuid
import re

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_executable():
    try:
        print(request.get_json())
        sequence = request.get_json()['sequence']
    except:
        return jsonify({'error': 'Invalid JSON'}), 400

    _uuid = str(uuid.uuid4())
    
    with open(f'fasta_buffer/{_uuid}.fasta', 'w') as fasta_file:
        fasta_file.write(f">input_sequence\n{sequence}\n")
    
    try:
        o = subprocess.run(f"./fasta36 -d 0 fasta_buffer/{_uuid}.fasta c_elegans_tflink.fasta", capture_output=True, shell=True)
        output = o.stdout.decode()
        error = o.stderr
    except Exception as e:
        print("Error:", e)
        print("Other: ", error)
    
    os.remove(f'fasta_buffer/{_uuid}.fasta')
    
    result = parse_fasta(output)
    
    return jsonify({'result': result}), 200

#parses output of fasta36 and returns score
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

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )