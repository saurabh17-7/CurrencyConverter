import json
import urllib.request

def lambda_handler(event, context):
    try:
        amount = float(event['queryStringParameters']['amount'])
        from_currency = event['queryStringParameters']['from']
        to_currency = event['queryStringParameters']['to']

        # ✅ Your FreeCurrencyAPI key
        api_key = "fca_live_NABV8rKpHwcKPHLIYcBpSWiicu11OzI0QwC66akj"
        url = f"https://api.freecurrencyapi.com/v1/latest?apikey={api_key}&base_currency={from_currency}"

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            rates = data.get("data", {})

        if to_currency not in rates:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"message": "Invalid target currency"})
            }

        converted_amount = round(amount * rates[to_currency], 2)

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"result": converted_amount})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": str(e)})
        }
