deploy:
	git push heroku main

open:
	heroku open

test:
	python -m unittest test_main