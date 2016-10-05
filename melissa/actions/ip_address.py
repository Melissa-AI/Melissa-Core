import re

from netifaces import interfaces, ifaddresses, AF_INET

# Melissa
from melissa.tts import tts

WORDS = {
    'ip_address': {
        'groups': [
            'ip', ['ip', 'address'], ['network', 'address']
        ]
    }
}


def ip_address(text):
    tts("Here are my available I.P. addresses.")
    for ifaceName in interfaces():
        addresses = [
            i['addr'] for i in
            ifaddresses(ifaceName).setdefault(
                AF_INET, [{'addr': None}])]
        if None in addresses:
            addresses.remove(None)
        if addresses and ifaceName != "lo":
            updated_addresses = [re.sub(r"\.", r" dot ", address)
                                 for address in addresses]
            tts('%s: %s' % ("interface: " + ifaceName +
                            ", I.P. Address ", ', '.join(updated_addresses)))

    tts("Those are all my I.P. addresses.")
