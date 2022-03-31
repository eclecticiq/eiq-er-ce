# EclecticIQ Endpoint Response (ER) - Community Edition
EclecticIQ ER leverages the [Osquery](https://osquery.io/) tool, with [EclecticIQ Extension](https://github.com/EclecticIQ/osq-ext-bin) to provide endpoint visibility and monitoring at scale. To get the details of the architecture of the full platform, please read the [platform docs](https://github.com/EclecticIQ/eiq-er-docs). This repository provides the community release of the platform which focuses on the Osquery based agent management to provide visbility into endpoint activities, query configuration management, a live query interface and alerting capabilities based on security critical events.

## Prerequisites
- git client software
- Internet connectivity
- 5000 and 9000 ports should be available and accessible through firewall
- Docker(18.03.1-CE or above) and [docker-compose (1.21.1 or above)](https://docs.docker.com/compose/install/#install-compose)
- node and npm

## Build and deploy


### Fresh Installation

After you install Docker and Docker Compose, you can install the EclecticIQ
server. Please ensure that the following commands are executed from a root/administrator privileged terminal.

1.  Clone this repository.

    ```~/Downloads$ git clone https://github.com/EclecticIQ/eiq-er-ce.git```
     ```<snip>
    Cloning into 'plgx-esp'...
   
2.  Switch to the folder where the repository is cloned.

    ```~/Downloads\$ cd plgx-esp/```
3.  Enter the certificate-generate.sh script to generate certificates for
    osquery.  
    ```~/Downloads/plgx-esp$ sh ./certificate-generate.sh <IP address>```
    ```x.x.x.x
    Generating a 2048 bit RSA private key
    .........................................................................................+++
    .........................+++
    writing new private key to 'nginx/private.key'
    ``` 
            
    In the syntax, \<IP address\> is the IP address of the system on which on to host the EclecticIQ server. This will generate 
    the certificate for osquery (used for provisioning clients) and place the certificate in the nginx folder.

4.  Modify and save the .env file.

    1.  Edit the following configuration parameters in the file. In the syntax, replace the values in angle brackets with required values.
    ```
    ENROLL_SECRET=<secret value>
    POLYLOGYX_USER=<user login name> 
    POLYLOGYX_PASSWORD=<login password> 
    RSYSLOG_FORWARDING=true
    VT_API_KEY=<VirusTotal Api Key> 
    IBMxForceKey=<IBMxForce Key> 
    IBMxForcePass=<IBMxForce Pass>
    PURGE_DATA_DURATION=<number of days>  
    THREAT_INTEL_LOOKUP_FREQUENCY=<number of minutes>
     ```   
| Parameter | Description                                                                                                                                                                                  |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ENROLL_SECRET | Specifies the enrollment shared secret that is used for authentication.                                                                                                                              |
| POLYLOGYX_USER       | Refers to the user login name for the EclecticIQ server.                                                                                                         |
| POLYLOGYX_PASSWORD       | Indicates to the password for the EclecticIQ server user.                                                                                                              |
| RSYSLOG_FORWARDING       | Set to true to enable forwarding of osquery and EclecticIQ logs to the syslog receiver by using rsyslog. |                                                                         |  
| VT_API_KEY       | Represents the VirusTotal API key.                                                                            | 
| IBMxForceKey       | Represents the IBMxForce key.                                                                            | 
| IBMxForcePass       | Specifies the IBMxForce pass.                                                                            | 
| PURGE_DATA_DURATION       | Specifies the frequency (in number of days) for purging the data.                                                                            | 
| THREAT_INTEL_LOOKUP_FREQUENCY       | Specifies the frequency (in minutes) for fetching threat intelligence data.                                                                            |   
    2. Save the file.
    
5. Generating dist file using angular 8

    a. Installation of Node.js and Npm:

        Nodejs version required 10.3 and above
        npm version required 6.1 and above
  

        ==> Installing node on Ubuntu or debian based system

        Step 1: If curl is not installed on the system, run the following command to install it:
		       
		       sudo apt-get install curl
		       
        Step 2: Enabling nodesource repo:
		    
		        curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
		        
        Note: Here,  node.js version 10.x is being installed, if you want to install version 11, replace setup_10.x with setup_11.x.

        Step 3: To Install Node.js and NPM to your Ubuntu machine, use the command given below:
		      
		        sudo apt-get install -y nodejs
		       
        Step 4: Once installed, verify it by checking the installed version using the following command:
		      
		        node -v or node -version
		        npm -v or npm -version	
				
    b. Installing angular packages using npm
	```
        npm install -g @angular/cli@8.3.19 
    ```

    c. cd to the angular folder
    ```
        cd plgx-angular-ui
    ```

    d. Install project packages
    ```
       sudo npm install
    ```

    e. Installing gzipper to  generate the compressed files
    ```
        npm i gzipper@3.7.0 -g
    ```

    f. Creating dist folder using gzipper 
    ```
        ng build --prod --stats-json && sudo gzipper --verbose ../dist
    ```
    g. cd to the extracted folder
    ```
       cd ../
    ```
        
6.  Run the following command to start building containers using docker-compose.

    ```docker-compose -p 'plgx-esp' up -d```
    
    Typically, this takes approximately 10-15 minutes. The following lines appear on
    the screen when Docker starts:
    ````Starting plgx-esp_rabbit1_1  ... done
        Starting plgx-esp_postgres_1 ... done
        Starting plgx-esp_plgx-esp_1     ... done
        Attaching to plgx-esp_rabbit1_1, plgx-esp_postgres_1, plgx-esp_plgx-esp_1
        .
        .
        .
        Server is up and running```

### Upgrade from an existing Installation

After you install Docker and Docker Compose, you can install the EclecticIQ
server. Please ensure that the following commands are executed from a root/administrator privileged terminal.

1.  Clone this repository into a new directory.

    ```~/Downloads$ git clone https://github.com/EclecticIQ/eiq-er-ce.git```
     ```<snip>
    Cloning into 'plgx-esp'...
   
2.  Switch to the folder where the repository is cloned.

    ```~/Downloads\$ cd plgx-esp/```
3.  Execute the command to copy existing certs setting up the flags for osquery.

    sudo bash upgrade_script.sh --path < Path to the existing installation directory >

4.  Modify and save the .env file.

    1.  Edit the following configuration parameters in the file. In the syntax, replace the values in angle brackets with required values.
    ```
    ENROLL_SECRET=<secret value>
    POLYLOGYX_USER=<user login name> 
    POLYLOGYX_PASSWORD=<login password> 
    RSYSLOG_FORWARDING=true
    VT_API_KEY=<VirusTotal Api Key> 
    IBMxForceKey=<IBMxForce Key> 
    IBMxForcePass=<IBMxForce Pass>
    PURGE_DATA_DURATION=<number of days>  
    THREAT_INTEL_LOOKUP_FREQUENCY=<number of minutes>
     ```   
| Parameter | Description                                                                                                                                                                                  |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ENROLL_SECRET | Specifies the enrollment shared secret that is used for authentication.                                                                                                                              |
| POLYLOGYX_USER       | Refers to the user login name for the EclecticIQ server.                                                                                                         |
| POLYLOGYX_PASSWORD       | Indicates to the password for the EclecticIQ server user.                                                                                                              |
| RSYSLOG_FORWARDING       | Set to true to enable forwarding of osquery and EclecticIQ logs to the syslog receiver by using rsyslog. |                                                                         |  
| VT_API_KEY       | Represents the VirusTotal API key.                                                                            | 
| IBMxForceKey       | Represents the IBMxForce key.                                                                            | 
| IBMxForcePass       | Specifies the IBMxForce pass.                                                                            | 
| PURGE_DATA_DURATION       | Specifies the frequency (in number of days) for purging the data.                                                                            | 
| THREAT_INTEL_LOOKUP_FREQUENCY       | Specifies the frequency (in minutes) for fetching threat intelligence data.                                                                            |   
    2. Save the file.
    
5. Generating dist file using angular 8

    a. Installation of Node.js and Npm:

        Nodejs version required 10.3 and above
        npm version required 6.1 and above
  

        ==> Installing node on Ubuntu or debian based system

        Step 1: If curl is not installed on the system, run the following command to install it:
		       
		       sudo apt-get install curl
		       
        Step 2: Enabling nodesource repo:
		    
		        curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
		        
        Note: Here,  node.js version 10.x is being installed, if you want to install version 11, replace setup_10.x with setup_11.x.

        Step 3: To Install Node.js and NPM to your Ubuntu machine, use the command given below:
		      
		        sudo apt-get install -y nodejs
		       
        Step 4: Once installed, verify it by checking the installed version using the following command:
		      
		        node -v or node -version
		        npm -v or npm -version	
				
    b. Installing angular packages using npm
	```
        npm install -g @angular/cli@8.3.19 
    ```

    c. cd to the angular folder
    ```
        cd plgx-angular-ui
    ```

    d. Install project packages
    ```
       sudo npm install
    ```

    e. Installing gzipper to  generate the compressed files
    ```
        npm i gzipper@3.7.0 -g
    ```

    f. Creating dist folder using gzipper 
    ```
        ng build --prod --stats-json && sudo gzipper --verbose ../dist
    ```
    g. cd to the extracted folder
    ```
       cd ../
    ```

6.  Run the following command to start building containers using docker-compose.

    ```docker-compose -p 'plgx-esp' up --build -d```
    
    Typically, this takes approximately 10-15 minutes. The following lines appear on
    the screen when Docker starts:
    ````Starting plgx-esp_rabbit1_1  ... done
        Starting plgx-esp_postgres_1 ... done
        Starting plgx-esp_plgx-esp_1     ... done
        Attaching to plgx-esp_rabbit1_1, plgx-esp_postgres_1, plgx-esp_plgx-esp_1
        .
        .
        .
        Server is up and running```
        
7.  Log on to server using following URL using the latest version of Chrome or
    Firefox browser.
    
    ```https://<ip address>:5000/manage```

    In the syntax, `<IP address>` is the IP address of the system on which the
    EclecticIQ server is hosted. This is the IP address you specified in step 3.

8.  Ignore the SSL warning, if any.

9.  Log on to the server using the credentials provided above at step 5a.

10.  Provision the clients. For more information, see [Provisioning the EclecticIQ
    Client for Endpoints](https://github.com/EclecticIQ/eiq-er-docs/tree/master/03_Provisioning_Polylogyx_Client).


### Upgrading the agent

Download the latest CPT (v 3.0.0.0) and choose from the below upgrade options.

1. Shallow Upgrade : plgx_cpt.exe -g s ( Updates extension and binary and keeps the existing data).
2. Deep Upgrade : plgx_cpt.exe -g d ( Updates extension and binary and cleans the existing data)


## Uninstalling the Server 
------------------------

To uninstall the EclecticIQ server, run the following command to clean-up
existing Docker images and containers.

```~/Downloads\$ sh ./docker-cleanup.sh```

**Note:** This will clean **all** the images and containers.

## Uninstalling the Agent
-------------------------

Agent from the endpoints can be uninstalled following the [instructions here](https://github.com/EclecticIQ/eiq-er-docs/tree/master/03_Provisioning_Polylogyx_Client#uninstalling-the-client). If for any reasons these instructions do not work, then a brute force clean could be accomplished on the Windows sytems using _agent_cleanup.bat_ file provided as a part of this repository. The batch file can be downloaded on the target system and invoked from an administrator privileged command prompt.


## EclecticIQ ER Components
- plgx-esp - Manages requests coming from endpoint
- plgx-esp-ui - Mangement server for taking actions, modifying properties  of an endpoint.
- RabbitMQ
- nginx
- rSysLogF
- postgres

## Agent Configuration
EclecticIQ ER leverages osquery's TLS configuration, logger, and distributed read/write endpoints and provides a basic set of default configurations to simplify Osquery deployment. The platform also provides a Client Provisioning Tool (CPT) that wraps the agent installation via a thin installer. The CPT tool can be downloaded from the main page on the server UI which also gives the instruction on running the CPT at individual endpoint. For mass deployment, a centralized system like SCCM can be used.

## Supported Endpoints
Osquery is cross platform agent that supports 64 bit variants of Windows (7 and above), MacOS and all the popular Linux distributions (Ubuntu, Centos, RedHat etc). EclecticIQ ER's agent is built upon Osquery and therefore the supported endpoints are the ones as supported by Osquery.

## EclecticIQ ER API SDK
EclecticIQ ER can be programatically interacted with using the extensive  [REST API](https://github.com/EclecticIQ/eiq-er-docs/tree/master/13_Rest_API) interface. This allows for multiple use case like Incident Response, Threat Hunting, Compromise Assessment, Compliance checks etc to be easily served with the platform. This also provides an easy for integration with [SOAR platforms](https://youtu.be/XbpleymXpSg) 

## Integration with Big Data/Analytic systems
EclecticIQ ER is packaged with an rSysLog container. This container can be configured to stream the query results and other logs from the endpoint population to the back-end systems like Splunk, ELK, GrayLog etc for cross-product correlation, alert enrichments and other SIEM related use cases.

To configure rsyslog forwarding modify the [rsyslogd.conf](rSysLogF/rsyslogd.conf) and specify the destination address of the server accepting logs in syslog format. In the absense of any destination address, the container may not come up. It can be configured at a later point, although the container will have to be manually started.

## EclecticIQ ER - Community Edition License
Please read the [LICENSE](LICENSE) file for details on the license.

## EclecticIQ ER - Enterprise Edition
EclecticIQ ER comes with an enterprise flavor with advanced set of features and dedicated support. More about the enterprise edition of ER can be learned [here](https://github.com/EclecticIQ/eiq-er-docs)  or send an email to support@eclecticiq.com
