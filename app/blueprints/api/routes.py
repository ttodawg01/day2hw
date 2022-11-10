from flask import jsonify, request
from . import api
from app.models import Address

@api.route('/')
def index():
    return 'hello this is the API'


@api.route('/address')
def get_address():
    addresses = Address.query.all()
    return jsonify([a.to_dict() for a in addresses])

# @api.route('/addresses/<address_id>')
# def get_address(address_id):
#     address = Address.query.get_or_404(address_id)
#     return jsonify(address.to_dict())

@api.route('/address', methods=['POST'])
def create_address():
        # Check to see that the request sent a request body that is JSON
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get the data from the request body
    data = request.json
    # Validate the incoming data
    for field in ['address', 'date_created', 'user_id']:
        if field not in data:
            # If the field is not in the request body, throw an error saying they are missing a field
            return jsonify({"error": f"'{field}' must be in request body"}), 400
            
    # make new request data
    address = data.get('address')
    date_created = data.get('date_created')
    user_id = data.get('user_id')
    new_address = Address(address=address, date_created=date_created, user_id=user_id)
    return jsonify(new_address.to_dict()), 201