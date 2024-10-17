from flask import Blueprint, jsonify, request, Response, stream_with_context
from services.CharacterService import init_character_creation

# Blueprint for user-related routes
char_controller = Blueprint('char_controller', __name__)


@char_controller.route('/char/<session_id>', methods=['GET'])
def initCharacterCreation(session_id):
    def generate():
        for chunk in init_character_creation(session_id):
            yield chunk

    return Response(
        generate(),
        content_type='text/event-stream; charset=utf-8',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )

# @char_controller.route('/char/<session_id>', methods=['POST'])
# def createCharacter(session_id):
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Invalid data"}), 400
    
#     # Pass both session_id and data to create_user function
#     new_user = create_user(session_id, data)
#     # when creation inished we can return some specfic HTTP to inform fornt end that it cound start new session and proceed with new endpoint
#     return jsonify(new_user), 200