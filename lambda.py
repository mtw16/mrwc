import boto3
import json

def lambda_handler(event, context):
    # Configure Amazon SES
    aws_region = 'us-east-1'
    sender_email = 'dave@skisharkusa.com'
    ses = boto3.client('ses', region_name=aws_region)

    # Configure DynamoDB
    dynamodb = boto3.client('dynamodb')
    table_name = 'mwrc-email-list'
    response = dynamodb.scan(TableName=table_name)
    
    email_addresses = [item['emailaddress']['S'] for item in response['Items']]
    
    # Assuming the form data is in JSON format
    form_data = event['body']
    # Parse the JSON string into a dictionary
    parsed_data = json.loads(form_data)
    print(parsed_data)
    print(parsed_data['title'])
    print(parsed_data['message'])
    
    # HTML email template
    html_template = """
    <html>
    <head></head>
    <body>
        <h1>Header here</h1>
        <p>""" + parsed_data['message'] + """</p>
        <!-- Image in the footer -->
        <p>This email notification system is sponsored The Merrimack Co. </p>
        <img src="https://merrimackco.com/cdn/shop/files/tmc-logo-with-tagline-full-color-rgb-10in_300ppi.png?v=1644245461&width=250" alt="The Merrimack Co. logo" style="max-width: 100%;">
    </body>
    </html>
    """


    
    # Send email to each recipient
    for email in email_addresses:
        print(email)
        try:
            response = ses.send_email(
                Source=sender_email,
                Destination={
                    'ToAddresses': [email]
                },
                Message={
                    'Subject': {
                        'Data': parsed_data['title']
                    },
                    'Body': {
                        'Html': {
                            'Data': html_template
                        }
                    }
                }
            )
            
            print(f"Email sent to {email}: Message ID {response['MessageId']}")
        except Exception as e:
            # Log error if email is unverified
            print(f"Unable to send email to {email}. Error: {e}")

    return {
        'statusCode': 200,
        'body': 'Emails sent successfully'
    }
