import requests
from urllib.parse import urljoin
import json
import logging
logger = logging.getLogger(__name__)


class NetworkListManager(object):
    def __init__(self, session, baseurl):
        self.session = session
        self.baseurl = baseurl

    def http_caller(self, method: str, path: str, params=None, headers=None, payload=None) -> requests.Response:
        valid_methods = ['get', 'put', 'post', 'delete']
        try:
            if method not in valid_methods:
                raise ValueError(f'{method} is not a valid method')
        except (ValueError, IndexError) as err:
            raise err

        s = self.session
        try:
            r = s.request(method, urljoin(self.baseurl, path),
                          json=payload, params=params, headers=headers)
        except(requests.exceptions.RequestException, requests.exceptions.HTTPError) as err:
            logger.exception(err)
            raise
        else:
            if r.status_code in [200, 202, 204]:
                logger.debug(f'Successful {method.upper()} request made to {self.baseurl}{path}')
                return r
            else:
                if 'detail' in r.json():
                    detail = r.json().get('detail') or r.json().get('details')
                else:
                    detail = json.dumps(r.json(), indent=2)
                logger.error(f'Failed {method} request made to {self.baseurl}{path}, '
                             f'status_code={r.status_code}, details={detail}')
                raise requests.exceptions.HTTPError

    def get(self, path, params=None):
        r = self.http_caller('get', path, params)
        return r.json()

    def post(self, path, payload, headers, params=None):
        r = self.http_caller('post', path, params, headers, payload)
        return r.json()

    def put(self, path, params=None, headers=None, payload=None):
        r = self.http_caller('put', path, params, headers, payload)
        return r.json()

    def delete(self, path, params=None, headers=None, payload=None,):
        r = self.http_caller('delete', path, params, headers, payload)
        return r.json()

    def get_lists(self) -> list:
        path = '/network-list/v2/network-lists'
        json_results = self.get(path)
        return json_results

    def get_list(self, list_id: str) -> list:
        """
        Get details of specific network list
        :param list_id: ID of akamai's network list
        :return: dictionary with all the information about the list
        """
        path = f'/network-list/v2/network-lists/{list_id}'
        params = {'extended': 'true', 'includeElements': 'true'}
        json_results = self.get(path, params)
        return json_results

    def update_list(self, list_id: str, members: list) -> dict:
        """
        Updates a network list with the full new list of members
        :param list_id: ID of akamai's network list
        :param members: list of IP addresses
        :return: dictionary with all the information about the list
        """
        path = f'/network-list/v2/network-lists/{list_id}'
        network_list = self.get_list(list_id)
        headers = {'Content-Type': 'application/json'}
        params = {'extended': 'true', 'includeElements': 'true'}
        payload = {'name': network_list['name']}
        if 'type' in network_list:
            payload['type'] = network_list['type']
        if 'description' in network_list:
            payload['description'] = network_list['description']
        payload['syncPoint'] = network_list['syncPoint']
        payload['list'] = members
        json_results = self.put(path, params, headers, payload)
        return json_results

    def append_elements(self, list_id: str, elements: list) -> list:
        """

        :param list_id:
        :param elements:
        :return:
        """
        headers = {'Content-Type': 'application/json'}
        payload = {'list': elements}
        path = f'/network-list/v2/network-lists/{list_id}/append'
        json_results = self.post(path, payload, headers)
        return json_results

    def add_element(self, list_id: str, element: str) -> list:
        """

        :param list_id:
        :param element:
        :return:
        """
        path = f'/network-list/v2/network-lists/{list_id}/elements'
        headers = {'Content-Type': 'application/json'}
        params = {'element': element}
        json_results = self.put(path, params, headers)
        return json_results

    def remove_element(self, list_id: str, element: str) -> list:
        """

        :param list_id:
        :param element:
        :return:
        """
        path = f'/network-list/v2/network-lists/{list_id}/elements'
        headers = {'Content-Type': 'application/json'}
        params = {'element': element}
        json_results = self.delete(path, params, headers)
        return json_results

    def activate_list(self, list_id: str, environment: str, comments: str, recipients: list) -> list:
        """

        :param list_id:
        :param environment:
        :param comments:
        :param recipients:
        :return:
        """
        path = f'/network-list/v2/network-lists/{list_id}/environments/{environment}/activate'
        headers = {'Content-Type': 'application/json'}
        payload = {'comments': comments, 'notificationRecipients': recipients}
        json_results = self.post(path, payload, headers)
        return json_results

    def get_activation_status(self, list_id: str, environment: str) -> list:
        """

        :param list_id:
        :param environment:
        :return:
        """
        path = f'/network-list/v2/network-lists/{list_id}/environments/{environment}/status'
        json_results = self.get(path)
        return json_results



