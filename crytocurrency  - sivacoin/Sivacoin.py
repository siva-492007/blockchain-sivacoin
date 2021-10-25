# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 15:57:35 2021

@author: Vignesh Siva
@github: siva492007/blockchain
"""

# module 2 -  create a cryptocurrency (Sivacoin)

# install flask
# install postman
# requests package ( pip install requests )

# importing libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# part 1 - building a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, prev_hash = '0')
        self.nodes = set()
        
    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash,
                 'transactions': self.transactions}
        self.transactions = []
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
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver, 
                                  'amount': amount})
        prev_block = blockchain.get_prev_block()
        return prev_block['index'] + 1
    
    def add_nodes(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_len = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/blockchain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['blockchain']
                if length > max_len and self.validate_chain(chain):
                    max_len = length
                    longest_chain = chain
                    self.chain = longest_chain
                    return True
        return False
    
        # if longest_chain:
        #     self.chain = longest_chain
        #     return True
        # else: 
        #     return False
        
# part 2 - mining our blockchain
# creating a web app
app = Flask(__name__)

# creating an address for node on port 4927
node_address = str(uuid4()).replace('-', '')


# creating a blockchain
blockchain = Blockchain()

# mining a blockchain
@app.route('/mine', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.hash_function(prev_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Vignesh Siva', amount = 10)
    block = blockchain.create_block(proof, prev_hash)
    
    response = {'mesage': "Congratulation! You have mined a block!",
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash'],
                'transactions': block['transactions']}
    
    return jsonify(response), 200


# validating blockchain
@app.route('/validate', methods=['GET'])
def validate_blockchain():
    is_valid = blockchain.validate_chain(blockchain.chain)
    if is_valid:
        response = {'message': "Great Job! Blockchain is valid..."}
    else:
        response = {'message': "OMG! Blockchain in invalid..."}
    return jsonify(response), 200

# mining full blockchain
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    response = {'blockchain': blockchain.chain,
                'chain_length': len(blockchain.chain)}
    return jsonify(response), 200

# add new transaction to blockchain
@app.route('/add_transaxtion', methods=['POST'])
def add_new_transaction():
    json_file = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json_file for key in transaction_keys):
        return 'Inputs for transactions are invalid or missing!', 400
    index = blockchain.add_transaction(json_file['sender'], json_file['receiver'], json_file['amount'])
    response = {'message': f'This transaction will be added to Block - {index}'}
    return jsonify(response), 201

# Part 3 - Decentralizing our Blockchain
 
# connecting new nodes
@app.route('connect_node', methods=['POST'])
def connect_node():
    json_file = request.get_json()
    nodes = json_file.get('nodes')
    if nodes in None:
        return "No node address available", 400
    for node in nodes:
        blockchain.add_nodes(node)
    
    response = {'message': "New nodes are connected to the network. The nodes in Sivacoin Blockchain are: ",
               'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 200

# replacing chain by the longest chain
@app.route('/longest_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': "Our chain is replaced by the longest chain!",
                    'New_chain': blockchain.chain}
    else:
        response = {'message': "Good Going! Our chain is the longest chain!",
                    'Current_chain': blockchain.chain}
    return jsonify(response), 200

# Running Flask app
app.run(host = '0.0.0.0', port = 4927)
