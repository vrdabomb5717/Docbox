CREATE TABLE userpass ( id INTEGER PRIMARY KEY,
						username TEXT NOT NULL COLLATE NOCASE,
						password TEXT NOT NULL,
						email TEXT NOT NULL COLLATE NOCASE,
						firstname TEXT,
						middlename TEXT,
						lastname TEXT,
						UNIQUE (username) );
	