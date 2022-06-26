import urllib.request
import json
import os
import ssl

url = os.environ.get('ENDPOINT_URL')
api_key = os.environ.get('ENDPOINT_KEY') # Replace this with the API key for the web service

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

def get_review_sentiment(review: str) -> str:
    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    data =  {
    "Inputs": {
        "WebServiceInput0": [{"review_full": review}]
    },
    "GlobalParameters": {}
    }

    body = str.encode(json.dumps(data))

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        print(result)
        sample_dict: dict[dict] = eval(result)
        return sample_dict.get('Results').get('WebServiceOutput0')[0].get('Scored Labels')
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))


if __name__=='__main__':
    review = "Used to visit here a lot. Since refurbishment standards have dropped. Sandwiches are sparse (5 finger slices for 3 people) dried up bread. Scones are dry you need a lot of cream to revive them. As for cakes a couple of brightly coloured things on the top tier. Were told initially we would also get a cake from centre table however it was cleared up & where told all finished!!! For the money you get more value from a Happy Meal! Staff very nice but slow. However if you are any nationality other than English you will be treated like Royalty, sadly if you have an English accent you won't! We will not be going back anytime soon. Advise anyone reading this who wants high end afternoon tea to go to Ritz, Savoy or Claridges!"

    print(get_review_sentiment(review))