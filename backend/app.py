import base64
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

import json
import boto3

MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
system_prompt = '''
You are a specialised agent that is able to understand documents.
Answer any questions that are asked about the documents analysed.
'''
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/upload', methods=['POST'])
async def upload_file():
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
            fileName, fileExtension = file.filename.split('.')
          
           

            bedrock_runtime = boto3.client("bedrock-runtime",aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN)
            my_image = file.read()
            # print(my_image)
            user_prompt = "read entire file and List No of Incidents where supervisor is Jesse james"
            # user_prompt = "summarize top 5 nature of injury data and create a bar graph Python code snippet along with static data to save as image filename=ProjectChart.png. please return code only nothing else is required"
            messages = [
            {
                "role": "user",
                "content": [
                    {
                        "text": user_prompt
                    },
                    {
                        "document": {
                            "name":fileName,
                            "format": fileExtension, 
                            "source": {
                                "bytes": my_image
                            }
                        }
                    },
                ],
            }
            ] 
        
            response = bedrock_runtime.converse(
            system = [
                {
                "text": system_prompt
                }
            ],
            modelId = MODEL_ID,
            messages = messages
            )
            print(response)
            response_text = response["output"]["message"]["content"][0]["text"]
            # df = pd.read_excel(file)
            # exec(response_text.replace('python', '').replace('`', '').replace(file.filename,F'file').strip())
            # print("image generated")
            # image_path = os.path.join(os.getcwd(), 'ProjectChart.png')

            # Read the image file and encode it in base64
            # with open(image_path, "rb") as image_file:
            #     encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            # return jsonify({'image': encoded_image}), 200

            return jsonify({'message': response_text}), 200




            # content = await AWSCall(file)
            # return jsonify({'message': content}), 200
            # # Read and print file content (for small files)
            # file_content = file.read().decode('utf-8')
            # print(f"File content: {file_content}")

            # # Reset file pointer to the beginning
            # file.seek(0)

            # # Read the CSV file into a DataFrame
            # df = pd.read_csv(file, encoding='utf-8')
        # except UnicodeDecodeError:
        #     try:
        #         df = pd.read_csv(file, encoding='latin1')
        #     except Exception as e:
        #         return jsonify({'error': str(e)}), 500
        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500

        # Process the DataFrame as needed
        # message_content = (
        #     'Based on the incident list, here are all the Nature of Injuries along with their count:\n\n1. Sprain/Strain/Overexertion: 8\n2. Bruise/Contusion: 13\n3. Laceration or Cut: 8\n4. Soreness/Range of Motion Restricted: 8\n5. Eye injury/infection: 1\n6. Internal Injuries: 1\n7. Inflammation/Swelling: 3\n8. Not Determined: 2\n9. Crush Injury: 2\n10. Puncture: 2\n11. Abrasion, scrape: 3\n12. Compression: 1\n13. Animal/insect Bite or Attack: 1\n14. Burn, heat: 1\n15. Foreign Body: 1\n16. Allergic Reaction: 1\n17. Spasms: 2\n18. Tingling or numbness: 1\n\nNote: Many incidents had "N/A" listed for Nature of Injury and were not included in this count.'
        # )

        # return jsonify({'message': message_content}), 200


async def AWSCall(file):
    try:
        print(file)
        bedrock_runtime = boto3.client("bedrock-runtime")
        my_image = file.read()
        # print(my_image)
        user_prompt = " list down all Nature of injury along with count "
        messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": user_prompt
                },
                {
                    "document": {
                        "name":file.filename,
                        "format": "xlsx", 
                        "source": {
                            "bytes": my_image
                        }
                    }
                },
            ],
        }
        ] 
    
        response = await bedrock_runtime.converse(
           system = [
            {
            "text": system_prompt
            }
        ],
           modelId = MODEL_ID,
           messages = messages
          )
        print(response)
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text
    except Exception as e:
         return jsonify({'error': str(e)}), 500    

if __name__ == '__main__':
    app.run(debug=True)