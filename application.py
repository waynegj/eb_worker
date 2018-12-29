from flask import Flask, request
app = Flask(__name__)
@app.route('/', methods=['POST'])
def parse_request():
    r_body = request.get_json()
    print(r_body)
    return 'Received !' # response to your request.

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
