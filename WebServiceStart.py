from flask import Flask, request, jsonify

from chrome.chatGPT import PromptVariableFile, ChatGPTBrowser

# Create a Flask app instance
app = Flask(__name__)

# Define a route for the exposed file

@app.route("/")
def helloworld():
    return "Hello World"

@app.route("/LLM", methods=["GET"])
def get_LLM_response():
    print("Started")
    # Get the input string from the request body
    input_string = request.args.get("input")
    print ("LLM Browser request :" , input_string)
    # Check if input is provided
    if input_string is None:
        return jsonify({"error": "Missing request"}), 400

    # Process the input string (replace this with your logic)
    # Example: convert to uppercase
    full_command  = PromptVariableFile.AIOPS_PROMPT.replace("@@EXCEPTION_DETAIL@@", input_string )

    ChatGPTBrowser.inputRequest(full_command)
    response  = ChatGPTBrowser.getResponse()

    #Less contextual memory than ChatGPT and slowly logical performance degraded
    #BardBrowser.inputRequest(full_command)
    #response  = BardBrowser.getResponse()
    #extract json
    start_index = response.find("{") + 1
    end_index = response.rfind("}")
    extracted_string = response[start_index:end_index]
    print(f"Extracted Json response : {extracted_string}")
    processed_string = "{ " + extracted_string + " }"

    # Return the processed string
    return (processed_string)

if __name__ == "__main__":
    app.run()