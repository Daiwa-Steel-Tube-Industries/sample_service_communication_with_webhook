# Webhook Publisher-Subscriber Example

This project demonstrates a simple webhook pattern using two separate FastAPI services: a **Publisher** and a **Subscriber**.

-   The **Publisher** service is responsible for managing webhook subscriptions and sending out notifications when a specific event occurs.
-   The **Subscriber** service exposes an endpoint to receive these notifications.

This example simulates a scenario where an "order\_change" event in the publisher system triggers a notification to all subscribed systems.

---

## Core Concepts

### Publisher (`publisher.py`)

-   Maintains a list of registered webhooks.
-   Provides an endpoint to register a new webhook.
-   Provides an endpoint to simulate an event (`order_change`).
-   When the event is triggered, it iterates through all registered hooks for that event and sends an HTTP GET request to the hook's `url` with a data payload.

### Subscriber (`subscriber.py`)

-   A simple web server with a single endpoint (e.g., `/webhook`).
-   This endpoint is designed to listen for incoming GET requests from the publisher.
-   When it receives a notification, it prints the payload to the console to confirm receipt.

---

## Hook Data Structure

Webhooks are registered in the publisher using the following data structure:

-   **`id`** (integer): A unique identifier for the hook.
-   **`name`** (string): A descriptive name for the hook (e.g., "My web hook").
-   **`event`** (string): The name of the event to subscribe to. In this example, it is always `"order_change"`.
-   **`url`** (string): The URL of the subscriber that will be called when the event occurs.

---

## Setup and Installation

1.  **Prerequisites**: Make sure you have Python 3.7+ installed.

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## How to Run

You will need two separate terminal windows to run both services concurrently.

1.  **Terminal 1: Start the Subscriber**
    This service will listen for incoming webhook notifications.
    ```bash
    uvicorn subscriber:app --host 0.0.0.0 --port 8001
    ```
    The subscriber is now running and listening on `http://0.0.0.0:8001`.

2.  **Terminal 2: Start the Publisher**
    This service manages hooks and sends events.
    ```bash
    uvicorn publisher:app --host 0.0.0.0 --port 8000
    ```
    The publisher is now running on `http://0.0.0.0:8000`.

---

## How to Use: Step-by-Step

### Step 1: Register Webhooks with the Publisher

Use a tool like `curl` to register three webhooks. Two will point to a valid subscriber running on port `8001`, and one will point to a non-existent service on port `8002` to demonstrate a failure case.

**Hook 1:**
```bash
curl -X 'POST' \
  'http://localhost:8000/hooks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "name": "Hello Service",
  "event": "order_change",
  "url": "http://localhost:8001/hello"
}'
```

**Hook 2:**
```bash
curl -X 'POST' \
  'http://localhost:8000/hooks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 2,
  "name": "World Service",
  "event": "order_change",
  "url": "http://localhost:8001/world"
}'
```

**Hook 3:**
```bash
curl -X 'POST' \
  'http://localhost:8000/hooks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 3,
  "name": "Non-existent Service",
  "event": "order_change",
  "url": "http://localhost:8002/error"
}'
```

### Step 2: Trigger the Event on the Publisher

Now, simulate an `order_change` event by sending a `POST` request to the publisher's `/trigger-event` endpoint. The publisher will attempt to send a notification to all three registered hooks.

```bash
curl "http://localhost:8000/fake-event/order_change"
```

### Step 3: Check the log

Immediately after triggering the event, look at the terminal where the *subscriber* is running. You will see output confirming that it received the two valid webhook notifications from the publisher. The third hook will fail silently on the publisher side (or log an error, depending on implementation), but the subscriber will never receive it.

---

## Further information

You can access to the route `/docs` from both services for interactive docs.
