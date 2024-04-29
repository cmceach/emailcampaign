#!/usr/bin/env python
from email_campaign.crew import EmailCampaignCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'customer_id': input('Enter the customer id here: '),
    }
    EmailCampaignCrew().crew().kickoff(inputs=inputs)