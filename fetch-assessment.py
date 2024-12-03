from flask import Flask, request, jsonify
import uuid
import math
from datetime import datetime
app = Flask(__name__)

# In-memory storage
stored_data = []

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.json

    data['id'] = str(uuid.uuid4())

    stored_data.append(data)
    print('{ id: ' + data['id'] + ' }')
    return jsonify({'message': 'ok', 'id': data['id']}), 200

@app.route('/receipts/<string:id>/points', methods=['GET'])
def process_receipt_by_id(id):
    for data in stored_data:
        if data['id'] == id:
            points = 0

            """ 1 point for every alphanumeric character in the retailers name """
            for char in data['retailer']:
                if char.isalnum():
                    points += 1

            """ 50 points if the total is a round dollar amount with no cents """
            total = float(data['total'])
            if total % 1 == 0.0:
                points += 50

            """ 25 points if the total is a multiple of .25 """
            if total % .25 == 0.0:
                print('is multiple of .25')
                points += 25

            # 5 points for every two items on the reciept
            points += (int(len(data['items'])) // 2) * 5

            """
            If the trimmed length of the item description is a multiple of 3, 
            multiply the price by 0.2 and round up to the nearest integer. 
            The result is the number of points earned.
            """
            for item in data['items']:
                stripped_item = item['shortDescription'].strip()
                if int(len(stripped_item)) % 3 == 0:
                    print(str(len(stripped_item)) + ' is divisible by 3')
                    points += math.ceil(float(item['price']) * 0.2)

            """ 6 points if the day in the purchase date is odd """

            # Store date and time in a datetime object
            date_time = datetime.strptime(data['purchaseDate'] + " " + data['purchaseTime'], '%Y-%m-%d %H:%M')

            if (date_time.day % 2) != 0:
                points += 6

            """ 10 points if the time of the purchase is after 2:00pm and before 4:00pm """
            if date_time.hour >= 14 and date_time.hour < 16:
                points += 10


            return jsonify({'message': 'ok', 'points': points}), 200
        else:
            continue


@app.route('/receipts/all', methods=['GET'])
def getAll() :
    print('return')
    return jsonify({'message': 'ok', 'data': stored_data}), 200


if __name__ == '__main__':



    
    app.run(debug=True)