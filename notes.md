# How to Run

1. Install `mongodb` and run the daemon.

2. Change host from `mongo-dev` to `localhost` in files `config.py` and in `stat_service/database.py`

3. Create a virtual environment in the main directory

    `python3 -m venv main-venv`

4. Activate the virtual environment
	
	`source main-venv/bin/activate`

5. Install requirements

    `pip3 install -r requirements.txt`

6. Run `python submitter.py`

7. Run `python worker.py`

8. Move to `stat_service` directory, create a second virtual environment and activate it

    `cd stat_service
    python3 -m venv stats-venv
    source stats-venv/bin/activate`

9. Install stats requirements

    `pip3 install -r stats_requirements.txt`

10. Run `python stats.py`

11. Return to the main directory and run `python webservice.py`

12. Go to [http://localhost:8080/stats](http://localhost:8080/stats)
