from flask import Flask, request
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

@app.route( '/' , methods = [ 'POST' ] )
'''
    cURL Request sample:
    --------------------

    curl -X POST \
    http://localhost:5000 \
    -H 'Content-Type: text/plain' \
    -H 'Host: localhost:5000' \
    -d '<div class="jsoneditor-treepath" tabindex="0"><span class="jsoneditor-treepath-element">object</span><span class="jsoneditor-treepath-seperator">►</span><span class="jsoneditor-treepath-element">object</span><span class="jsoneditor-treepath-seperator">►</span><span class="jsoneditor-treepath-element">a</span></div>'
'''
def index():
    '''
        Built to parse the JSON tree HTML in https://jsoneditoronline.org/
        Inspect and copy the HTML elements in <div class="jsoneditor-treepath" tabindex="0">
        or using inspect tool hover and select JSON tree in navigation bar
    '''
    try:
        test_str = request.get_data(cache=True, as_text=True, parse_form_data=False)
        
        test_str = test_str.strip()

        remove1 = '<div class="jsoneditor-treepath" tabindex="0">'
        remove2 = '<span class="jsoneditor-treepath-seperator">►</span>'
        remove3 = '<span class="jsoneditor-treepath-show-all-btn" title="show all path">...</span>'
        remove4 = '</div>'
        subst = ""

        test_str = re.sub(remove1, subst, test_str, 0, re.MULTILINE)
        test_str = re.sub(remove2, subst, test_str, 0, re.MULTILINE)
        test_str = re.sub(remove3, subst, test_str, 0, re.MULTILINE)
        test_str = re.sub(remove4, subst, test_str, 0, re.MULTILINE)

        regex = r"</span>"
        subst = r"</span>\n"
        test_str = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        remove5 = '<span class="jsoneditor-treepath-element">'
        remove6 = '</span>'
        subst = ""

        test_str = re.sub(remove5, subst, test_str, 0, re.MULTILINE)
        test_str = re.sub(remove6, subst, test_str, 0, re.MULTILINE)

        regex = r"\n0"
        subst = "[0]"
        test_str = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        regex = r"\n"
        subst = "."
        test_str = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        regex = r"\.(.+?:.+?)\."
        subst = "['\\1']."
        test_str = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        regex = r"\.(.+?:.+?)(\.|\[0\])"
        subst = "['\\1']\\2"
        test_str = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        regex = r"^object"
        subst = ""
        test_str = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        regex = r"\.(\n)?$"
        test_str = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        return test_str.strip()
    except Exception as e:
        return str(e)

app.run( debug = False , host = '0.0.0.0' , threaded = True )
