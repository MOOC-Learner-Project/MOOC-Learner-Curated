FROM curated:base
RUN mkdir app
ADD . /app/MOOC-Learner-Curated
WORKDIR /app/MOOC-Learner-Curated
RUN ["chmod", "+x", "wait_for_it.sh"]
CMD ["./wait_for_it.sh", "db", "python", "-u", "autorun.py", "-c", "../config/config.yml"]
