# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 20:32:57 2021

@author: Vignesh Siva
@github: siva492007/blockchain
"""


# module 1 -  create a blockchain

# install flask
# install postman

# importing libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# part 1 - building a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, prev_hash = '0')
        
    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash}
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash_function(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    def validate_chain(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash_function(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index += 1
        return True
    
# part 2 - mining our blockchain
# creating a web app
app = Flask(__name__)
    
# creating a blockchain
blockchain = Blockchain()

# mining a blockchain
@app.route('/mine', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.hash_function(prev_block)
    block = blockchain.create_block(proof, prev_hash)
    
    response = {'mesage': "Congratulation! You have mined a block!",
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash']}
    
    return jsonify(response), 200


# validating blockchain
@app.route('/validate', methods=['GET'])
def validate_blockchain():
    is_valid = blockchain.validate_chain(blockchain.chain)
    if is_valid:
        response = {'message': "Great Job! Blockchain is valid..."}
    else:
        respnse = {'message': "OMG! Blockchain in invalid..."}
    return jsonify(response), 200

# mining full blockchain
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    response = {'blockchain': blockchain.chain,
                'chain_length': len(blockchain.chain)}
    return jsonify(response), 200


# Running Flask app
app.run(host = '0.0.0.0', port = 4927)
