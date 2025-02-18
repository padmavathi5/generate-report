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
        message_content = (
            'Based on the incident list, here are all the Nature of Injuries along with their count:\n\n1. Sprain/Strain/Overexertion: 8\n2. Bruise/Contusion: 13\n3. Laceration or Cut: 8\n4. Soreness/Range of Motion Restricted: 8\n5. Eye injury/infection: 1\n6. Internal Injuries: 1\n7. Inflammation/Swelling: 3\n8. Not Determined: 2\n9. Crush Injury: 2\n10. Puncture: 2\n11. Abrasion, scrape: 3\n12. Compression: 1\n13. Animal/insect Bite or Attack: 1\n14. Burn, heat: 1\n15. Foreign Body: 1\n16. Allergic Reaction: 1\n17. Spasms: 2\n18. Tingling or numbness: 1\n\nNote: Many incidents had "N/A" listed for Nature of Injury and were not included in this count.'
        )

        return jsonify({'message': message_content}), 200

if __name__ == '__main__':
    app.run(debug=True)