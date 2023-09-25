# How to setup the Bremerhaven grid
1. Download the zipped data from the link in the download_link.txt.
2. Unpack the data in your designated simulation environment. A VM running Linux is highly recommended.
    2a. If the remote Linux-VM is chosen: create an ssh connection to the VM and tunnel the two ports 11193 and 11194.
        A possible command could like this:
        ```ssh -L 11193:localhost:11193 -L 11194:localhost:11194  <user_name@vm_ip>```
3. Navigate to /pgasc/pg-agent-systems-competition and run ```sudo docker-compose -f docker-compose-dev.yml -p pg-asc up -d```
4. The scheduler GUI should now be reachable via localhost:11193 in your local browser.
5. Create an account and follow the how-to on the website.
6. Using the example Experiment Run Documents (ERDs) in the folder 'Example ERDs', you can create your own experiment by copying the contents of the ERDs into
   the Experiment Run Document field when creating a new experiment.
7. Have fun experimenting. 
