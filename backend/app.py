from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Request received...")

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # Print file details
            print(f"File name: {file.filename}")
            print(f"File content type: {file.content_type}")

            # Read and print file content (for small files)
            file_content = file.read().decode('utf-8')
            print(f"File content: {file_content}")

            # Reset file pointer to the beginning
            file.seek(0)

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file, encoding='latin1')
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        # Process the DataFrame as needed
        return jsonify({'message': 'File successfully processed'}), 200

if __name__ == '__main__':
    app.run(debug=True)