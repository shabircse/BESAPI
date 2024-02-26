import requests
import xml.etree.ElementTree as ET
import time
import base64
import urllib3

# Disable SSL certificate verification warnings
urllib3.disable_warnings()

# Define the URL and payload
url = "https://Server:52311/api/clientquery"
payload = """<BESAPI>
<ClientQuery>
    <ApplicabilityRelevance>true</ApplicabilityRelevance>
    <QueryText>name of operating system</QueryText>
    <Target>
        <ComputerName>srvat0029</ComputerName>
    </Target>
</ClientQuery>
</BESAPI>"""

# Define username and password for basic authentication
username = "user"
password = "password"

# Concatenate username and password with a colon separator
credentials = f"{username}:{password}"

# Encode the credentials into Base64
credentials_base64 = base64.b64encode(credentials.encode()).decode()

# Create the headers dictionary
headers = {
    'Content-Type': 'text/plain',
    'Authorization': f"Basic {credentials_base64}"
}

try:
    # Make POST request
    response = requests.post(url, headers=headers, data=payload, verify=False)
    response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes

    print("POST Response:", response.text)

    # Parse XML response
    root = ET.fromstring(response.content)
    id_element = root.find(".//ID")
    if id_element is not None:
        id_value = id_element.text
        print("ID:", id_value)
        try:
            id_value_int = int(id_value)
            print("ID (Integer):", id_value_int)
            time.sleep(6)

            # Make GET request to retrieve the result
            url_result = f"https://Server:52311/api/clientqueryresults/{id_value_int}"
            response_get = requests.get(url_result, headers=headers, verify=False)
            response_get.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
            print("GET Response:", response_get.text)
            
            # Parse the XML response
            root_get = ET.fromstring(response_get.content)
            
            # Extract the <Result> tag
            result_element = root_get.find(".//Result")
            
            if result_element is not None:
                result = result_element.text
                print("Result:", result)
            else:
                print("No results found.")
                
        except ValueError:
            print("ID is not an integer")
    else:
        print("ID not found in response.")

except requests.exceptions.RequestException as e:
    print("Error:", e)
