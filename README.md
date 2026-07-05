# SchnitzelDonnerstag

An analysis of meals in several canteens in Stuttgart. The goal is to prove that the so-called "SchnitzelDonnerstag"
really exists.

## Background

While studying in Stuttgart we enjoyed going to the canteens on campus after our lectures. After a few semesters we
noticed that Schnitzel was part of the meal rotation, and that it was more likely to be served on Thursdays
than on any other day. This assumption was based solely on our personal experience, so we wanted to prove it with data.
On campus, the SchnitzelDonnerstag phenomenon has been discussed among students and professors, with some suggesting it
might actually be a Schnitzelmittwoch.

### Data aggregation

To prove our assumption we started collecting data from the canteens in Stuttgart. To get the data we used a custom
written Python script that uses the [openmensa API](https://github.com/openmensa/openmensa) to fetch data daily. The
script is being triggered through a cron job and run by GitHub Actions. The fetched data is being stored in a MongoDB
database hosted on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) solely for havin a generous free tier.

### Data analysis

The analysis will start once enough data has been collected. We plan to wait two to three semesters after the
start of data collection to gather a sufficient number of observations.

Before drawing conclusions, we will check that the sample size is large enough to give a hypothesis test reasonable
power to detect a real effect, rather than just an absence of evidence. Once that is confirmed, we will apply a
statistical hypothesis test to check whether Schnitzel is served on Thursdays significantly more often than would be
expected if it were served with equal probability on every weekday.

# Contributors

* [Alex Q](https://github.com/quadflal)
* [Anton F](https://github.com/anton-fischer)
* [Adrian E](https://github.com/Exotischer)
