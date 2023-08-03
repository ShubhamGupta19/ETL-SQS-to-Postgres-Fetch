import hashlib

def mask_pii_data(data):
    """
    Mask Personally Identifiable Information (PII) data in the input JSON records.

    Args:
        data (list of dict): A list of JSON records containing PII data.

    Returns:
        list of dict: A list of JSON records with masked PII data.

    Raises:
        Exception: If there is an error while masking PII data.
    """
    try:
        # Iterate through each record in the data
        for record in data:
            # Hash the 'device_id' and 'ip' fields for masking
            record['masked_device_id'] = hashlib.sha256(record['device_id'].encode()).hexdigest()
            record['masked_ip'] = hashlib.sha256(record['ip'].encode()).hexdigest()

            # Remove the original 'device_id' and 'ip' fields to hide them
            del record['device_id']
            del record['ip']

        return data

    except Exception as e:
        raise Exception(f"Error while masking PII data: {str(e)}") from e
