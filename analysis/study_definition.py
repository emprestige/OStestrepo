from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA


study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.registered_with_one_practice_between( #I'm interested in all patients who have never changed practice, between these two dates
        "2019-02-01", "2020-02-01"
    ),

    age=patients.age_as_of( #give me a column of data corresponding to the ageg of each patient on the given date 
        "2019-09-01",  #given date
        return_expectations={ #I expect every patient to have a value, and the distribution of agess to match that of the real UK population
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
)
