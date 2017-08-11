## Python V3 Invoice Sample App
### Sample App in Python that implements OAuth1, Invoice CRUD and Webhooks

This sample app is meant to provide working example of how to make API calls to QuickBooks. Specifically, this sample application demonstrates the following:

1. Implementing OAuth1 to connect an application to a customer's QuickBooks Online company.
2. Invoicing which supports create, read, update, delete and query operations using:
    1. Invoice object
    2. Dictionary
3. Webhooks

Please note that while these examples work, features not called out above are not intended to be taken and used in production business applications. In other words, this is not a seed project to be taken cart blanche and deployed to your production environment.

For example, certain concerns are not addressed at all in our samples (e.g. security, privacy, scalability). In our sample apps, we strive to strike a balance between clarity, maintainability, and performance where we can. However, clarity is ultimately the most important quality in a sample app.

Therefore there are certain instances where we might forgo a more complicated implementation (e.g. caching a frequently used value, robust error handling, more generic domain model structure) in favor of code that is easier to read. In that light, we welcome any feedback that makes our samples apps easier to learn from.

Note: This app has been developed and tested for MacOS Sierra 10.12

### Table of Contents

* [Getting Started](#getting-started)
* [Project Structure](#project-structure)
* [OAuth1 Implementation](#oauth1-implementation)
* [Invoice CRUD Using Object](#invoice-crud-using-object)
* [Invoice CRUD Using Dictionary](#invoice-crud-using-dictionary)
* [Webhooks](#webhooks)


### Getting Started

Clone the repository:
```
git clone https://github.com/IntuitDeveloper/PythonV3InvoiceSampleApp.git
```

Install Python 3.5:
```
https://www.python.org/
```

Use requirements.txt file:
```
cd PythonV3InvoiceSampleApp/
pip install -r requirements.txt 
```

Launch your app:
```
cd PythonV3InvoiceSampleApp/
python manage.py runserver
```

### Project Structure
This project is divided into 4 apps. They're mostly independent of each other (except for OAuth1 apps) so that developers can pick and choose the app they want to use. The apps are as follows:
1. SampleAppOAuth
2. SampleInvoiceCRUD
3. SampleInvoiceCRUDUsingDict
4. SampleWebhooks

All app settings can be found at [settings.py](mysite/settings.py) and apps use common utility modules found in [context.py](mysite/utils/context.py) and [httpRequests.py](mysite/utils/httpRequests.py).

Please go to each app to see how to configure and run it. 

### OAuth1 Implementation
This app shows how to use you app's consumer token and consumer secret and get OAuth access token, access secret and realm id.

To implement OAuth2, please refer to [OAuth2PythonSampleApp](https://github.com/IntuitDeveloper/OAuth2PythonSampleApp)

#### Configure this app
Please enter your app's consumer token and consumer secret in [settings.py](mysite/settings.py). Then follow the steps given above to launch the app and go to url `http://localhost:8000/oauth`

### Invoice CRUD Using Object
This app shows how to create, read, update, delete and query Invoice using objects. 

#### Configure this app
For OAuth2 apps, please go to [OAuth2 playgorund](https://developer.intuit.com/v2/ui#/playground) and follow the OAuth2 flow and then paste the access token and associated realm id in [settings.py](mysite/settings.py). 

This app by default uses OAuth2 tokens, if your have OAuth1 app and would like to run this app, please go to [settings.py](mysite/settings.py) and change `oauth_flag` to 1, follow steps from OAuth1 implementation to run it and save access tokens and realm id to session.

Then follow the steps given above to launch the app and go to url `http://localhost:8000/invoice`

### Invoice CRUD Using Dictionary
This app shows how to create, read, update, delete and query Invoice using dictionary. 

#### Configure this app
For OAuth1 and OAuth2 token configuration see the steps given in Invoice CRUD Using Object.

Then follow the steps given above to launch the app and go to url `http://localhost:8000/invoiceUsingDict`

### Webhooks
This app shows how to receive webhooks for authorized sandbox company for subscribed entities.

#### Configure this app
1. Install ngrok and launch ngrok with command `ngrok http 8000`
2. Copy the https url you get from the ngrok server after it launche, paste it in app's Webhooks tab to field `Endpoint URL`, select entities and click Save.
3. Copy the webhooks verifier after clicking Save and paste it in [settings.py](mysite/settings.py)
Note: For now, `webhooks_subscribed_entities` is saved for Customer and Term. It will need to be updated for other subscribed entities.

After the subscribed entities are edited from the customer's point of view in sandbox company, you should see the post from Intuit's servers on the terminal.
