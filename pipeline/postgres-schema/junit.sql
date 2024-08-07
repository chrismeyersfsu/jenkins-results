CREATE TABLE junit_data_b (
	"Time" TIMESTAMP WITHOUT TIME ZONE, 
	build_number DECIMAL NOT NULL, 
	instance VARCHAR NOT NULL, 
	pipeline_step VARCHAR NOT NULL, 
	pipeline_step_1 VARCHAR NOT NULL, 
	project_name VARCHAR NOT NULL, 
	project_name_1 VARCHAR NOT NULL, 
	project_namespace VARCHAR NOT NULL, 
	project_path VARCHAR NOT NULL, 
	project_path_1 VARCHAR NOT NULL, 
	suite_name VARCHAR NOT NULL, 
	suite_name_1 VARCHAR NOT NULL, 
	test_class_full_name VARCHAR NOT NULL, 
	test_class_full_name_1 VARCHAR NOT NULL, 
	test_count BOOLEAN NOT NULL, 
	test_duration DECIMAL NOT NULL, 
	test_name VARCHAR NOT NULL, 
	test_name_1 VARCHAR NOT NULL, 
	test_status VARCHAR NOT NULL, 
	test_status_1 VARCHAR NOT NULL, 
	test_status_ordinal DECIMAL NOT NULL
);
