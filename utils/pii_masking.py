import hashlib

def mask_pii_data(data):
    try:
        for record in data:
            # Hash the device_id and ip fields for masking
            record['masked_device_id'] = hashlib.sha256(record['device_id'].encode()).hexdigest()
            record['masked_ip'] = hashlib.sha256(record['ip'].encode()).hexdigest()

            # Remove the original device_id and ip fields
            del record['device_id']
            del record['ip']

        return data

    except Exception as e:
        raise Exception(f"Error while masking PII data: {str(e)}")