### Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/payment-monitoring-system.git
```

### Navigate Into Project

```bash
cd payment-monitoring-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask API server:

```bash
python main.py
```

The API will run locally at:

```text
http://127.0.0.1:5000
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t payment-monitoring-system .
```

### Run Docker Container

```bash
docker run -p 5000:5000 payment-monitoring-system
```

## Automated Testing

Run all automated tests using:

```bash
pytest
```

Test coverage includes:

- Fraud detection validation
- API endpoint testing
- Error handling validation
- Monitoring metrics testing