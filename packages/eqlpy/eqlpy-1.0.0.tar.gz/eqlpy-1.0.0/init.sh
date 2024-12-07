curl -L https://github.com/cipherstash/encrypt-query-language/releases/download/eql-0.4.3/cipherstash-encrypt.sql | psql -h localhost -p 5432 -U postgres eqlpy_example
psql -h localhost -p 5432 -U postgres eqlpy_example < application_types.sql
psql -h localhost -p 5432 -U postgres eqlpy_example < create_examples_table.sql
