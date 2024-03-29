**Set Up**
   1. Check out the code into your local repo
   2. Pip install PyYAML, requests, pdoc3, unittest
   3. Set up servers for testing
      1. PySense tests must be run as admin
      2. Create configuration files in Test/resources
         1. Files to create
            1. TestConfig.yaml: All non version specific methods will be run against this file
            2. WindowsConfig.yaml: Create if you want to test Windows only end points
            3. LinuxConfig.yaml: Create if you want to test Linux only end points. 
         2. Note: 
            1. If your TestConfig is Linux, you can copy that config to LinuxConfig.yaml. Same with Windows. 
      3. Import PySense.smodel to all servers being tested against
         1. Attach the CSV file to Dim_Dates.csv
         2. Build the cube on both instances
      4. All other assets needed are created and destroyed by the test
   4. Run a test ensure all tests pass
      1. The linux build one and data import may fail due to API issues
      
**Repo walk through**
   1. Documentation
      1. This is the folder where the html documentation is stored
      2. Documentation is created from function comments (so comment your functions)
      3. Regenerate it with pdoc after before every release
      4. Html is viewed through link in readme
      5. Sample pdoc run:
    
    "venv/Scripts/pdoc3.exe" --html --output-dir Documentation PySense

   2. PySense Tutorial: Contains assets relating to PySense training series
   3. PySense: The actual code, which we will cover below
   4. Scripts: 
      1. Sample scripts for users to use
      2. When adding a new script
         1. Ensure comment at the top explaining script
         2. Separated block of configuration options that can be set
         3. Scripts should be runnable with no configuration beyond this
   5. Snippets: Example one liners on how to use functions
   6. Tests
      1. PySense tests tests all method called from py_client
      2. PySense{some object}Tests has all the tests for that object
      3. PySense{os}Tests has tests for platform specific methods
      4. All tests are added to the scale_test_suite
      5. In the main function we set up and tear down our test assets
      6. Test assets that should be reused are put in resources
      7. Test assets that are ephemeral are put in tmp
   7. Other
      1. Git attributes: Used so that git doesn’t count the documentation html as “code”
      2. Git ignore: For ignoring files we don’t want to commit to git
      3. Installing Python pptx: A walk through on installing python
      4. Licence: PySense uses the GPL-3.0 License 
      5. ReleaseNotesFull.md: 
         1. A running list of release notes for all versions
         2. When creating a new release append the new release notes to the top
      6. Readme.md: The current github readme
      7. Setup.py: A file to tell pypi about PySense
      
**The Code (PySense Folder)**

   1. PySense MixIns
      1. Contains functions that need to be accessible from py_client
      2. Done to prevent PySense.py from becoming too large
   2. PySense.py
      1. Set up all authentication methods
         1. Authentication methods all get forwarded to PySenseAuthentication class for processing
         2. Authentication methods return the py_client object
      2. We add all of our mixins to PySense
      3. init
         1. Creates a py_client that links us to server
         2. Param dict allows users to pass in their own config values
            1. There is a default dict which contains some default values
            2. Users can overwrite this by passing the value in a parameter
         3. Create the rest connector object
         4. Initializes role values
      4. Methods for modifying debug and parameter settings
   3. PySenseAuthentication.py: Authentication methods
   4. PySense{object}.py
      1. The python class for each PySense object
      2. Each object has
         1. A reference to py_client so it knows what server it belongs to
         2. An internal copy of it’s json
         3. Methods for manipulating that object
   5. PySenseRestConnector.py
      1. The rest wrapper around PySense
      2. Use rest_call to make a call to the api
         1. Action_type: post, put, get, patch, delete
         2. Url: the api url, ex: ‘api/v1/dashboards’
         3. Data: Data payload if needed
         4. Json_payload: Json_payload, more likely to be used
         5. Query_params
            1. A json dict of query params
            2. PySense will format them into a query string
            3. PySense will remove any keys with value ‘None’
         6. File: A file to upload (like an sdata file)
         7. Path: A place to download the response, like for exporting
   6. SisenseRole.py
      1. Enum which defines roles in PySense
      2. Done to reduce confusion around role names in PySense
      3. Can convert a string to a role enum with from_str()
   7. SisenseVersion.py: Enum for defining linux or windows