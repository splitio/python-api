_CACHE_CONTROL = 'Cache-Control'
_CACHE_CONTROL_NO_CACHE = 'no-cache'

class FetchOptions(object):
    """Fetch Options object."""

    def __init__(self, cache_control_headers=False, change_number=None):
        """
        Class constructor.

        :param cache_control_headers: Flag for Cache-Control header
        :type cache_control_headers: bool

        :param change_number: ChangeNumber to use for bypassing CDN in request.
        :type change_number: int

        :param sets: list of flag sets
        :type sets: list
        """
        self._cache_control_headers = cache_control_headers
        self._change_number = change_number

    @property
    def cache_control_headers(self):
        """Return cache control headers."""
        return self._cache_control_headers

    @property
    def change_number(self):
        """Return change number."""
        return self._change_number

def build_fetch(change_number, fetch_options, metadata):
    """
    Build fetch with new flags if that is the case.

    :param change_number: Last known timestamp of definition.
    :type change_number: int

    :param fetch_options: Fetch options for getting definitions.
    :type fetch_options: splitio.api.commons.FetchOptions

    :param metadata: Metadata Headers.
    :type metadata: dict

    :param rbs_change_number: Last known timestamp of a rule based segment modification.
    :type rbs_change_number: int

    :return: Objects for fetch
    :rtype: dict, dict
    """
    query = {}
    query['since'] = change_number
    extra_headers = metadata
    if fetch_options is None:
        return query, extra_headers

    if fetch_options.cache_control_headers:
        extra_headers[_CACHE_CONTROL] = _CACHE_CONTROL_NO_CACHE
    if fetch_options.change_number is not None:
        query['till'] = fetch_options.change_number
    return query, extra_headers

class Backoff(object):
    """Backoff duration calculator."""

    MAX_ALLOWED_WAIT = 30 * 60  # half an hour

    def __init__(self, base=1, max_allowed=MAX_ALLOWED_WAIT):
        """
        Class constructor.

        :param base: basic unit to be multiplied on each iteration (seconds)
        :param base: float

        :param max_allowed: max seconds to wait
        :param max_allowed: int
        """
        self._base = base
        self._max_allowed = max_allowed
        self._attempt = 0

    def get(self):
        """
        Return the current time to wait and pre-calculate the next one.

        :returns: time to wait until next retry.
        :rtype: float
        """
        to_return = min(self._base * (2 ** self._attempt), self._max_allowed)
        self._attempt += 1
        return to_return

    def reset(self):
        """Reset the attempt count."""
        self._attempt = 0
