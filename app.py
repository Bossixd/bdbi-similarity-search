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
        o = subprocess.run(f"./fasta36 -d 0 fasta_buffer/{_uuid}.fasta c_elegans_tflink.fasta", shell=True)
        output = o.stdout.decode()
        error = o.stderr
    except Exception as e:
        print("Error:", e)
        print("Other: ", error)
    
    os.remove(f'fasta_buffer/{_uuid}.txt')
    
    result = parse_fasta(output)
    
    return jsonify({'result': result}), 200

#parses output of fasta36 and returns score
def parse_fasta(output):
    print(output)
    srch = re.search("[0-9]+ residues in +[0-9]+ sequences", output)
    n_sequence = int(output[srch.start() : srch.end()].split(' ')[-2])

    srch = re.search("The best scores are:", output)
    buffer = output[srch.start():].split("\n")[1].split(' ')

    return {
        buffer[0]: float(buffer[-1])
    }

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )