##### Configuring Omnata to Ingest Data from LinkedIn Ads into Snowflake

In this guide, we will go over the steps to configure Omnata to ingest data from LinkedIn Ads into Snowflake. This integration will allow you to easily transfer data from LinkedIn Ads into Snowflake, where you can analyze and transform it using Snowflake's powerful analytics tools.

---

###### Step 1: Connecting Omnata to LinkedIn Ads

1. Log in to your Omnata account.
2. Navigate to the "Connections" section.
3. Click on "Add Connection" and select "LinkedIn Ads" as the source.
4. Follow the on-screen instructions to authenticate your LinkedIn Ads account with Omnata.

---

###### Step 2: Setting Up the Destination in Snowflake

1. Log in to your Snowflake account.
2. Create a new database or schema to store the LinkedIn Ads data if you haven't already.
3. Note down your Snowflake account details (account name, username, password) as you will need them in the next step.

---

###### Step 3: Configuring the Data Pipeline in Omnata

1. In Omnata, navigate to the "Data Pipelines" section.
2. Click on "New Pipeline" and select "LinkedIn Ads" as the source and "Snowflake" as the destination.
3. Enter your Snowflake account details and select the database/schema where you want to store the data.
4. Choose the tables or data objects you want to replicate from LinkedIn Ads.
5. Configure any data transformation or filtering options as needed.
6. Save the pipeline configuration.

---

###### Step 4: Starting the Data Replication

1. Once the pipeline is configured, you can start the data replication process.
2. Monitor the replication progress in the Omnata dashboard to ensure it completes successfully.

---

###### Step 5: Verifying the Data in Snowflake

1. Log in to your Snowflake account and navigate to the database/schema where the data was loaded.
2. Run queries to verify that the data from LinkedIn Ads has been successfully replicated.

---
