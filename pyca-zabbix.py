import sys
import socket
from optparse import OptionParser
import requests
from requests import RequestException
from requests.auth import HTTPBasicAuth


# Rest endpoint to get the pyca services
PYCA_SERVICES = "/api/services"


def get_agentstate(options):
    response = get_pyca_services(options)
    if response:
        print(response['meta']['services']['agentstate'])
    else:
        print("ERROR")


def get_capture(options):
    response = get_pyca_services(options)
    if response:
        print(response['meta']['services']['capture'])
    else:
        print("ERROR")


def get_ingest(options):
    response = get_pyca_services(options)
    if response:
        print(response['meta']['services']['ingest'])
    else:
        print("ERROR")


def get_schedule(options):
    response = get_pyca_services(options)
    if response:
        print(response['meta']['services']['schedule'])
    else:
        print("ERROR")

# Actions dict
services = { "agentstate": get_agentstate,
            "capture": get_capture,
            "ingest": get_ingest,
            "schedule": get_schedule
           }


def get_pyca_services(options):

    url = "http://" + options.host + ":" + options.port
    try:
        r = requests.get(url + PYCA_SERVICES, auth=HTTPBasicAuth(options.user, options.password), timeout=2)
    except RequestException:
        print("ERROR")
        sys.exit(1)

    if r.status_code != requests.codes.ok:
        r.raise_for_status()
        sys.exit(1)
    response = r.json()
    return response


def warning(options):
    print("Please check %prog --help for the correct syntax")


def process_service(parser, options):
    services.get(options.service)(options)


def main():

    parser = OptionParser(usage="%prog [-s]", version="%prog 0.1")
    parser.add_option("-s", "--service", dest="service", nargs=1, type="choice",
                        choices=["agentstate", "capture", "ingest", "schedule"],
                        help="Options: agentstate, capture, ingest and schedule.")
    parser.add_option("--host", dest="host", default="localhost",
                      help="Ip address for the pyca agent, default is localhost")
    parser.add_option("-p", "--port", dest="port", default="80",
                      help="Port for the pyca rest interface, default is 80")
    parser.add_option("-u", "--user", dest="user", default="admin",
                      help="User to use for authentication")
    parser.add_option("-p", "--password", dest="password", default="opencast",
                      help="Password to use for authentication")

    (options, args) = parser.parse_args()

    if not(options.service):
        parser.error("Incorrect number of arguments, please provide a service.")

    process_service(parser, options)


if __name__ == "__main__":
    main()
