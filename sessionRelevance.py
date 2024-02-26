import besapi
 
def run_client_relevance(server_url, username, password, relevance_query):
    # Initialize the BESAPI client
    client = besapi.besapi.BESConnection('user', 'passs', 'https://Server:52311')
 
    # Connect to the BigFix server
    client.connect()
 
    try:
        # Run the client relevance query
        results = client.eval_relevance(relevance_query)
 
        # Print the results
        for result in results:
            print(f"Computer: {result['computer']}, Result: {result['result']}")
 
    except besapi.BESConnection.Error as e:
        print(f"Error: {e}")
 
    finally:
        # Disconnect from the BigFix server
        client.disconnect()
 
if __name__ == "__main__":
    # Replace these values with your actual BigFix server details
    server_url = "https://Server:52311"
    username = "bigfix_admin"
    password = "User@098!"
    # Replace this with the client relevance query you want to execute
    relevance_query = 'name of operating system'
 
    run_client_relevance(server_url, username, password, relevance_query)
