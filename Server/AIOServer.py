import argparse
import json
import logging
from aiohttp import web


async def token(request):
    return web.Response(
        content_type=bytes,
        
    )
    # Send response status code
    self.send_response(200)
    # Send headers
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    # Send message back to client
    key = str(uuid.uuid4())
    # value is the expiry of the token
    value = current_time + TOKEN_EXPIRY
    # add the uuid and the current time into the token dictionary
    add_token_to_dict(value, key)
    # Write content as utf-8 data
    self.wfile.write(bytes(key, "utf8"))
    return

async def offer(request):
    params = await request.json()

    return web.Response(
        content_type='application/json',
        text=json.dumps({
            'sdp': pc.localDescription.sdp,
            'type': pc.localDescription.type
        }))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web Server')
    parser.add_argument('--port', type=int, default=8081, help='Port: 8081)')
    parser.add_argument('--verbose', '-v', action='count')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    app.router.add_post('/offer', offer)
    web.run_app(app, port=args.port)