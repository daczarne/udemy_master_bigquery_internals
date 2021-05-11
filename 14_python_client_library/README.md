# Python client library

We need to set up a service account key to access BigQuery via APIs. Head on to *IAM & Admin > Service Accounts > + CREATE SERVICE ACCOUNT*. Now provide a name for it and click *CREATE*. You can set up privileges in the authentication key (for example, project editor). Then click *CONTINUE*. If needed, grant users access to the service account, then click *DONE*.

The Google UI will display the list of service accounts. Go to *Actions* and *Create key*. Recommended key type is JSON. Click create and a JSON file will be downloaded onto your computer. This JSON file will be embedded on the project. **DO NOT SHARE THE KEY!!**
