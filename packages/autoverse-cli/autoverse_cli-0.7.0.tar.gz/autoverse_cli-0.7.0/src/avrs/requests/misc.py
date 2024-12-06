from avrs.requests.request import AvrsApiRequest

class AvrsGetSimVersionRequest(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'GetVersion', 0)
        psr = parser.add_parser('get-sim-version', help='get the version of the currently running simulator')
        psr.set_defaults(func=self.send_request)
    
    def get_request_body(self, args):
        return {
        }