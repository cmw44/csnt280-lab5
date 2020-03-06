-- init.sql for the test_db database
drop table if exists students cascade;
drop table if exists sections cascade;
drop table if exists students_sections cascade;

create table students(
   id serial,
   first_name text,
   last_name text,
   primary key (id)
);
create table sections(
   id serial,
   course_alpha text,
   credits integer,
   primary key (id)
);
create table students_sections(
   id serial,
   student_id integer references students(id),
   section_id integer references sections(id),
   primary key (id)
);
create view students_view as
   select students.id as st_id, students.first_name,
   students.last_name, sections.id as sec_id,
   sections.course_alpha, sections.credits
   from students join students_sections
   on students.id=students_sections.student_id
   join sections on
   students_sections.section_id=sections.id;
