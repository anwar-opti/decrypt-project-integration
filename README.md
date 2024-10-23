# Decrypt Project Integration settings field in datastore

The settings field in datastore for ProjectIntegration is decrypted.
Normally, its encrypted in two ways as follows
1. base64encrypted
2. aws encrypted and then base64encrypted

To see the value of settings field encrypted in 2nd way, this repo is created.
All you need to do is - 

1. Clone this repo and install the requirements (`pip install -r requirements.txt`)
2. Update the constants with appropriate values (depending on the environment e.g. `prod` or `develrc`), you should get the value from `configsecrets` in `AWS S3 bucket` with PCI account. See the fields in `aws.customer_secrets` field of `configsecrets` file 
3. Provide the `value_to_decode` (some examples are listed), which is the result of base64decrypt of the settings field
4. Run the main function

Many thanks [Istiak Bin Mahmod](https://github.com/istiakbinmahmod) for helping me with the code.