import struct,base58,base64
from .logManager import *
def parse_data(program_data,all_js={}):
    # Step 1: Base64 decode the input program data
    decoded_data = base64.b64decode(program_data)
    
    offset = 8  # Adjusted offset to skip the first 8 bytes
    parsed = all_js
    
    try:
        # 32-byte publicKey (mint)
        mint = decoded_data[offset:offset + 32]
        parsed['mint'] = base58.b58encode(mint).decode('utf-8')
        offset += 32
        
        # 8-byte u64 (solAmount)
        parsed['solAmount'], = struct.unpack_from('<Q', decoded_data, offset)
        offset += 8
        
        # 8-byte u64 (tokenAmount)
        parsed['tokenAmount'], = struct.unpack_from('<Q', decoded_data, offset)
        offset += 8
        
        # 1-byte bool (isBuy)
        parsed['isBuy'], = struct.unpack_from('<?', decoded_data, offset)
        offset += 1
        
        # 32-byte publicKey (user)
        user = decoded_data[offset:offset + 32]
        parsed['user_address'] = base58.b58encode(user).decode('utf-8')
        offset += 32
        
        # 8-byte i64 (timestamp)
        parsed['timestamp'], = struct.unpack_from('<q', decoded_data, offset)
        offset += 8
        
        # 8-byte u64 (virtualSolReserves)
        parsed['virtualSolReserves'], = struct.unpack_from('<Q', decoded_data, offset)
        offset += 8
        
        # 8-byte u64 (virtualTokenReserves)
        parsed['virtualTokenReserves'], = struct.unpack_from('<Q', decoded_data, offset)
        
    except struct.error as e:
        print(f"Struct error: {e}")
        return None
    return parsed
def get_program_data(response, all_js={}):
    """
    Extract and parse program data from logs.
    """
    try:
        logs = get_logs(response)
        for log in logs:
            if log.startswith('Program data: '):
                base64_data = log[len('Program data: '):]
                all_js = parse_data(base64_data, all_js)
    except Exception as e:
        logger.error(f"Error parsing program data: {e}")
    return all_js
