from flask import Flask, request, jsonify
import subprocess
import os
import shlex
import uuid

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
        o = subprocess.run(f"./fasta36 c_elegans_tflink.fasta fasta_buffer/{_uuid}.fasta", shell=True)
        output = o.stdout
        error = o.stderr
    except Exception as e:
        print("Error:", e)
        print("Other: ", error)
    
    # os.remove(f'fasta_buffer/{_uuid}.txt')
    
    return jsonify({'uuid': _uuid, 'result': output}), 200
    
    # data = request.get_json()
    # user_input = data.get('input', '')

    # # Sanitize input to prevent command injection
    # args = ['fasta36'] + shlex.split(user_input)

    # try:
    #     result = subprocess.run(
    #         args,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #         timeout=30  # Adjust timeout as needed
    #     )
    #     output = result.stdout.decode()
    #     error = result.stderr.decode()
    #     return jsonify({
    #         'output': output,
    #         'error': error,
    #         'exit_code': result.returncode
    #     }), 200
    # except subprocess.TimeoutExpired:
    #     return jsonify({'error': 'Timeout occurred'}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )