-- add_initial_data.sql to add initial data to test_db
insert into students (id, first_name, last_name) values
   (1, 'Jane','Doe');
insert into students (id, first_name, last_name) values
   (2, 'John','Doe');
insert into students (id, first_name, last_name) values
   (3,'Bill','Gates');
insert into sections (id, course_alpha, credits) values
   (1, 'CSNT110', 3);
insert into sections (id, course_alpha, credits) values
   (2, 'CSNT132', 4);
insert into sections (id, course_alpha, credits) values
   (3, 'CSNT140', 4);
insert into sections (id, course_alpha, credits) values
   (4, 'CSNT280', 3);
insert into students_sections (student_id, section_id)
   values (1, 1);
insert into students_sections (student_id, section_id)
   values (1, 2);
insert into students_sections (student_id, section_id)
   values (2, 1);
insert into students_sections (student_id, section_id)
   values (2, 2);
insert into students_sections (student_id, section_id)
   values (3, 3);
insert into students_sections (student_id, section_id)
   values (3, 4);
