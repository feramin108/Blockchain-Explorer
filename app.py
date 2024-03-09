from flask import Flask, render_template, request
from blockchain import Blockchain
from datetime import datetime

app = Flask(__name__)
blockchain = Blockchain()

def format_timestamps(chain):
    for block in chain:
        # Check if the timestamp is a string in the expected format
        if isinstance(block['timestamp'], (float, int)):
            block['timestamp'] = datetime.fromtimestamp(block['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(block['timestamp'], str):
            try:
                # Convert the timestamp to the desired format
                block['timestamp'] = datetime.strptime(block['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                # If the timestamp is not in the expected format, leave it unchanged
                pass

@app.route('/')
def index():
    # Preprocess timestamps to a human-readable format
    format_timestamps(blockchain.chain)
    return render_template('index.html', chain=blockchain.chain)

@app.route('/mine')
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Reward for mining
    blockchain.new_transaction(sender="0", recipient="your_username", amount=1)

    # Create a new block
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    # Preprocess timestamps to a human-readable format
    format_timestamps([block])

    return render_template('mine.html', block=block)

@app.route('/transactions/new', methods=['GET', 'POST'])
def new_transaction():
    if request.method == 'POST':
        values = request.form
        required = ['sender', 'recipient', 'amount']

        if not all(k in values for k in required):
            return 'Missing values', 400

        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        return f'Transaction will be added to block {index}'

    return render_template('new_transaction.html')

if __name__ == '__main__':
    app.run(debug=True)
