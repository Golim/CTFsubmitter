# How to Run

1. Install `mongodb` and run the daemon.

2. Change host from `mongo-dev` to `localhost` in files `config.py` and in `stat_service/database.py`

3. Create a virtual environment in the main directory

    `python3 -m venv ctf-submitter`

4. Install requirements

    `pip3 install -r requirements.txt`

5. Run `python submitter.py`

6. Run `python worker.py`

7. Move to `stat_service` directory and create a second virtual environment

    `python3 -m venv ctf-submitter`

8. Install stats requirements

    `pip3 install -r stats_requirements.txt`

9. Run `python stats.py`

10. Return to the main directory and run `python webservice.py`

11. Go to [http://localhost:8080/stats](http://localhost:8080/stats)
