"""Small HTTP/SSE JSON-RPC client for Unity MCP; Python standard library only."""
import argparse
import json
import sys
import urllib.request
from pathlib import Path


def decode_response(raw, request_id=1):
    if raw.lstrip().startswith('{'):
        response = json.loads(raw)
        if response.get('id') != request_id:
            raise ValueError('Mismatched JSON-RPC response ID')
        return response
    data = []
    for line in (raw + '\n\n').splitlines():
        if line.startswith('data:'):
            data.append(line[5:].lstrip())
        elif not line and data:
            payload = '\n'.join(data)
            data.clear()
            if payload == '[DONE]':
                continue
            response = json.loads(payload)
            if response.get('id') == request_id:
                return response
    raise ValueError('No matching JSON-RPC response in SSE stream')


def rpc(url, method, params, timeout=90):
    body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode('utf-8')
    request = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return decode_response(response.read().decode('utf-8-sig'))


def unwrap(response):
    if 'error' in response:
        return response['error'], True
    result = response.get('result', {})
    failed = bool(result.get('isError')) if isinstance(result, dict) else False
    if isinstance(result, dict):
        content = result.get('content', [])
        parsed = []
        for block in content:
            if block.get('type') != 'text':
                continue
            try:
                value = json.loads(block['text'])
            except (ValueError, KeyError):
                value = block.get('text', '')
            if isinstance(value, dict) and value.get('success') is False:
                failed = True
            parsed.append(value)
        if parsed:
            return parsed[0] if len(parsed) == 1 else parsed, failed
    return result, failed


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tool', nargs='?', help='MCP tool name; check --list-tools before guessing schemas')
    parser.add_argument('arguments', nargs='?', default='{}', help='JSON object arguments')
    parser.add_argument('--url', default='http://127.0.0.1:27841/')
    parser.add_argument('--list-tools', action='store_true')
    parser.add_argument('--code-file', type=Path, help='Trusted C# file for execute_code; refresh must be done first')
    parser.add_argument('--save', type=Path, help='Save raw envelope outside Unity, without bypassing MCP checks')
    args = parser.parse_args()
    try:
        if args.list_tools:
            if args.tool or args.code_file:
                parser.error('--list-tools cannot be combined with a tool or --code-file')
            response = rpc(args.url, 'tools/list', {})
        else:
            arguments = json.loads(args.arguments)
            if not isinstance(arguments, dict):
                parser.error('arguments must be a JSON object')
            if args.code_file:
                if args.tool not in (None, 'execute_code'):
                    parser.error('--code-file requires execute_code')
                arguments['code'] = args.code_file.read_text(encoding='utf-8-sig')
                arguments.setdefault('skip_refresh', True)
            tool = 'execute_code' if args.code_file else args.tool
            if not tool:
                parser.error('provide a tool name, --list-tools or --code-file')
            response = rpc(args.url, 'tools/call', {'name': tool, 'arguments': arguments})
        value, failed = unwrap(response)
        if args.save:
            args.save.write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(value, ensure_ascii=False, indent=2))
        return 1 if failed else 0
    except (OSError, ValueError) as error:
        print(f'{type(error).__name__}: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
