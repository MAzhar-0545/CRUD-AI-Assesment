# app.py
from flask import Flask, request, jsonify
from api import BotAPI

app = Flask(__name__)
chatbot = BotAPI()

@app.route('/prompts', methods=['POST'])
def create_prompt():
    """Create a new prompt and return its index."""
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        index = chatbot.create_prompt(prompt)
        return jsonify({
            'status': 'success',
            'index': index,
            'message': 'Prompt created successfully'
        }), 201
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/prompts/<int:prompt_index>/response', methods=['GET'])
def get_response(prompt_index):
    """Get ChatGPT response for a stored prompt."""
    try:
        response = chatbot.get_response(prompt_index)
        return jsonify({
            'status': 'success',
            'response': response
        })
    except IndexError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404
    except RuntimeError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 503
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/prompts/<int:prompt_index>', methods=['PUT'])
def update_prompt(prompt_index):
    """Update an existing prompt."""
    try:
        data = request.get_json()
        new_prompt = data.get('prompt')
        chatbot.update_prompt(prompt_index, new_prompt)
        return jsonify({
            'status': 'success',
            'message': 'Prompt updated successfully'
        })
    except (IndexError, ValueError) as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/prompts/<int:prompt_index>', methods=['DELETE'])
def delete_prompt(prompt_index):
    """Delete a prompt (optional bonus implementation)."""
    try:
        if not chatbot._is_valid_index(prompt_index):
            raise IndexError("Invalid prompt index")
        chatbot.prompts.pop(prompt_index)
        return jsonify({
            'status': 'success',
            'message': 'Prompt deleted successfully'
        })
    except IndexError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)