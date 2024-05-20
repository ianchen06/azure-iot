# Azure IoT

## Overview

This IoT reference app will have the following features

1. The edge device can send telemetry to the cloud IoT Hub (in this demo, the temperature)
1. A Azure function will read the telemetry from IoT Hub, and store the record in PostgreSQL
1. A Streamlit web app will read the data from PostgreSQL and display it.
1. The user can send commands to the device from the Streamlit web app

## Components

1. Device (ESP32, Raspberry Pi, etc)
2. Azure IoT Hub
3. Azure Function
4. Azure Flexible PostgreSQL
5. Azure App Services
6. Streamlit

## Architecture

![architecture](images/azure-architecture.png)

## Azure

| Service          | Free Quota                                                   | Purpose                           |
| ---------------- | ------------------------------------------------------------ | --------------------------------- |
| IoT Hub          | 8000 msgs/day                                                | Gateway between devices and cloud |
| App Service      | 10 web, mobile, or API apps with 1 GB storage 1 hour per day | Host Streamlit app                |
| Azure PostgreSQL | 12 month free                                                | Data storage                      |
| Azure Function   | 1M executions                                                | Insert data from IoT Hub to DB    |

## Getting Started

### Setup Database

You can use any PostgreSQL server (Azure, Supabase, local postgres, etc)

For this lesson, I will use Azure PostgreSQL

![create-pg1](./images/2024-05-20_09-53.png)
Create a PostgreSQL server by searching in the search bar and click "Azure Database for PostgreSQL Flexible server"

![pg2](./images/2024-05-20_10-12.png)
In the "Basics" tab. Make sure the configration matches the screenshot.

Save the credentials for the admin user. We will need this to connect to our server.

![pg2](./images/2024-05-20_10-03.png)
Make sure to enable firewall rules for the server. Here we allow connection from anywhere for development purposes.

![pg3](./images/2024-05-20_10-13.png)
Make changes in "Basics" and "Networking" tabs to match the configurations in the screenshot.

### Setup Azure IoT Hub

Next, we will create a Azure IoT Hub

![iot](./images/2024-05-20_10-08.png)

Follow the on screen directions to create a "Free" Tier IoT Hub. Make sure it is in the same Location as the PostgreSQL.

![](./images/2024-05-20_10-21.png)
Add a new device

![](./images/2024-05-20_10-22.png)
Make sure to select "Symmetric key" for the authentication

### Setup Azure Function

![](./images/2024-05-20_11-27.png)
Create a Azure Function App, select "Consumption" plan.

![](./images/2024-05-20_11-29.png)
Choose "Python" for the runtime, and make sure to select the same Region as the Postgres DB and IoT Hub.

![](./images/2024-05-20_11-29_1.png)
Make sure to enable "Basic Authentication", we will use this to deploy our function from GitHub Actions.

#### Clone example GitHub

Clone the following example GitHub repo for Azure Function
https://github.com/ianchen06/myiot-ingestor

Delete the `.git` folder and create a new git repo and upload to your own GitHub account.

Open `.github/workflows/azure-functions-app-python.yml` and change `AZURE_FUNCTIONAPP_NAME` configuration to the Azure Function name you created in the previous step.

![](./images/2024-05-20_11-37.png)
Go to your Azure Function App, select "Overview" tab, and click "Get publish profile". This will download the secrets we need to deploy the app.

![](./images/2024-05-20_11-39.png)
Create a new GitHun Actions secret, name it `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`,

![](./images/2024-05-20_11-42.png)
Open the profile you downloaded previously and copy/paste the secret into the "Secret" field. Click "Add Secret"

![](./images/2024-05-20_11-45.png)
Open the `.github/workflows/azure-functions-app-python.yml` file. Change the `AZURE_FUNCTIONAPP_NAME` to your Azure Function name. Commit the file.

Now the GitHub Action should run and deploy the function to your Azure Function App.

![](./images/2024-05-20_12-18.png)
Add the following environment variables

| Environment Variable          | Description                                                                | Example                                                |
| ----------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------ |
| DATABASE_URL                  | Connection string of the PostgreSQL server                                 | postgresql://user:pass@mypostgres.com/postgres         |
| EVENT_HUB_NAME                | Event Hub compatible name for your IoT Hub                                 | iothub-ehub-techin510-591-6d81                         |
| IOTHUB_CONNECTION_STRING_NAME | Name of the environment variable that stores the IoT Hub Connection String | IOTHUB_CONNECTION_STRING                               |
| IOTHUB_CONNECTION_STRING      | The actual connection string to the IoT Hub                                | Endpoint=sb://ihsuprodbyres002dednamespace.servicebus. |

![](./images/2024-05-20_12-24.png)
You can find the values for `EVENT_HUB_NAME` and `IOTHUB_CONNECTION_STRING` in the IoT Hub Hub Settings page

### Sending telemetry to IoT Hub

Open a terminal and run the following commands

```
cd device
pip install -r requirements.txt
cp .env.sample .env
```

Open `.env` and change the values to your IoT Hub settings. Then run the following commands.

```
python ./device.py
```

This will start a python program and act as a IoT device, and periodically send telemetry (in this example, a fake temperature value) to our IoT Hub.

![](./images/2024-05-20_12-33.png)
Go to your Function App, and click the function in the Overviews Tab. It should be a function triggered by "Event Hub"

![](./images/2024-05-20_12-37.png)
With the `device.py` running, you should see logs printed when there is a new message from the device to IoT Hub.

### Web Application and data visualization

Run the following command in a new terminal

```
cd webapp
pip install -r requirements.txt
cp .env.sample .env
```

Change the values in `.env` to your own settings, including PostgreSQL DATABASE_URL, and the IoT Hub and Device settings. Then run the following commands

```
streamlit run app.py
```

![](./images/2024-05-20_12-43.png)

You should see a web interface with the values sent from the IoT Device!

![](./images/2024-05-20_12-46.png)
You can click the `Send command` button and check the terminal of `device.py`, you should see that the device received a command from our web interface. You can use this to control or update settings of your device.
