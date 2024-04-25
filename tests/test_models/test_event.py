
import pytest
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event_details(event):
    logging.info(f"Event Title: {event.title}")
    logging.info(f"Event Start: {event.start_datetime}")
    logging.info(f"Event End: {event.end_datetime}")
    logging.info(f"Event Published: {event.published}")
    logging.info(f"Event Type: {event.event_type.name}")
    if event.creator:
        logging.info(f"Creator Nickname: {event.creator.nickname}")
        logging.info(f"Creator Email: {event.creator.email}")

@pytest.mark.asyncio
async def test_event_creation(async_client, company_tour_event):
    # Here you can implement tests to validate event creation, retrieval, etc.
    log_event_details(company_tour_event)
    assert company_tour_event.title == "Company Tour" 
    assert not company_tour_event.published