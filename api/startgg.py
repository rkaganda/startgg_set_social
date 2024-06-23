import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import config
from typing import Any, Dict

# Configure logging
logger = logging.getLogger(__name__)

# Set the logging level for the gql.transport.requests module to WARNING
logging.getLogger('gql.transport.requests').setLevel(logging.WARNING)


# Define custom exception for missing API key
class NoApiKey(Exception):
    pass


url = "https://api.start.gg/gql/alpha"


def get_set(set_id: int) -> Dict[str, Any]:
    # Retrieve the API key from the config
    api_key = config.current_config.get('startgg_token')

    if not api_key:
        logger.error("API key is not set in the configuration.")
        raise NoApiKey("API key is not set in the configuration.")

    # Set up the transport with your API key in the headers
    transport = RequestsHTTPTransport(
        url=url,
        headers={'Authorization': f'Bearer {api_key}'},
        use_json=True,
    )

    # Create a GraphQL client
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query GetSetDetails($setId: ID!) {
      set(id: $setId) {
        id
        event {
            slug
            name
            videogame {
                name
            }
            tournament {
                name
            }
        }
        stream {
            streamName,
            streamSource
        }
        slots(includeByes: false) {
          entrant {
            id
            name
            participants {
              id
              gamerTag
              user {
                authorizations {
                    type
                    externalUsername
                }
              }
            }
          }
          standing {
            stats {
              score {
                value
              }
            }
          }
        }
      }
    }
    """)

    variables = {
        "setId": set_id
    }

    # Log the request details
    logger.info(f"Query: {query}")
    logger.info(f"Variables: {variables}")

    # Execute the query
    try:
        result = client.execute(query, variable_values=variables)
        logger.info(f"Query result: {result}")
        return result
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
