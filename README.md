# Python Google Cloud Task Queue sample for Google App Engine Standard Environment

This demonstrates how to create tasks and place them in push queues using [Google Cloud Task Queue](https://cloud.google.com/appengine/docs/standard/python/taskqueue/) on [Google App Engine Standard Environment](https://cloud.google.com/appengine).

## Running the sample locally

1. When running locally, you can use the [Google Cloud SDK](https://cloud.google.com/sdk) to provide authentication to use Google Cloud APIs:

    $ gcloud init

2. Download the [Google App Engine Python SDK](https://cloud.google.com/appengine/downloads) for your platform.

3. To run this app locally, specify both `.yaml` files to `dev_appserver.py`:

    $ dev_appserver.py -A your-app-id app.yaml worker.yaml

4. Visit `http://localhost:8080/stats/` to view your application.

## Deploying the sample

1. Download the [Google App Engine Python SDK](https://cloud.google.com/appengine/downloads) for your platform.

2. Deploy using gcloud:

    Deploy the worker:

        gcloud app deploy worker.yaml
        
    Deploy the web app, you will need to specify your Project ID and a version number:

         gcloud app deploy --project your-app-id -v your-version

4. Visit `https://your-app-id.appost.com/stats/` to view your application.

## How to test the API

   To make it simpler to try, I've already published the example so you can test it directly. Use your favorite client to make calls to the API, I leave as an example the calls using cURL.
    
        curl -X GET \
          https://pid-rmscm02500.appspot.com/stats/ \
          -H 'Cache-Control: no-cache'
          
        curl -X POST \
          https://pid-rmscm02500.appspot.com/mutant/ \
          -H 'cache-control: no-cache' \
          -H 'content-type: application/json' \
          -d '{"dna":["TTGCCA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]}'    


