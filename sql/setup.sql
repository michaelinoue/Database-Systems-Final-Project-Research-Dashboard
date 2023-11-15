USE academicworld;

ALTER TABLE keyword
ADD COLUMN ( # add additional fields
	rating INTEGER,
    rating_date DATETIME),
ADD CHECK (rating >=0 AND rating <= 5) ; # add constraint for ratings field