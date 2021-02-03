use pedal_dev_v_0;

insert into `logins` (`sub_id`, `refresh_token`, `iat`, `exp`) values (1, 'alphaNum0123', '2020-01-01T00:00:00.000', '2021-01-01T00:00:00.000');

insert into `study` (`id`, `name`, `code`) values (1, 'study', 'study1');
insert into `study` (`id`, `name`, `code`) values (2, 'study', 'study2');
insert into `study` (`id`, `name`, `code`) values (3, 'study', 'study3');
insert into `study` (`id`, `name`, `code`) values (4, 'study', 'study4');
insert into `study` (`id`, `name`, `code`) values (5, 'study', 'study5');
insert into `study` (`id`, `name`, `code`) values (6, 'study', 'study6');
insert into `study` (`id`, `name`, `code`) values (7, 'study', 'study7');
insert into `study` (`id`, `name`, `code`) values (8, 'study', 'study8');
insert into `study` (`id`, `name`, `code`) values (9, 'study', 'study9');

insert into `site` (`id`, `name`, `code`) values (1, 'site 1', 'site1');

insert into `site_has_study` (`site_id`, `study_id`) values (1, 1);

insert into `study_version` (`id`, `study_id`) values (1, 1);
insert into `study_version` (`id`, `study_id`) values (2, 2);
insert into `study_version` (`id`, `study_id`) values (3, 3);
insert into `study_version` (`id`, `study_id`) values (4, 4);
insert into `study_version` (`id`, `study_id`) values (5, 5);
insert into `study_version` (`id`, `study_id`) values (6, 6);

insert into `note` (`id`, `value`) values (1, 'value1');
insert into `note` (`id`, `value`) values (2, 'value2');
insert into `note` (`id`, `value`) values (3, 'value3');

insert into `tag` (`id`, `code`) values (1, 'code1');
insert into `tag` (`id`, `code`) values (2, 'code2');

insert into `criterion` (`id`, `code`) values (1, 'code1');
insert into `criterion` (`id`, `code`) values (2, 'code2');
insert into `criterion` (`id`, `code`) values (3, 'code3');

insert into `eligibility_criteria` (`id`, `study_version_id`) values (1, 1);
insert into `eligibility_criteria` (`id`, `study_version_id`) values (2, 2);
insert into `eligibility_criteria` (`id`, `study_version_id`) values (3, 3);

insert into `el_criteria_has_criterion` (`id`, `criterion_id`, `eligibility_criteria_id`) values (1, 1, 1);
insert into `el_criteria_has_criterion` (`id`, `criterion_id`, `eligibility_criteria_id`) values (2, 2, 2);
insert into `el_criteria_has_criterion` (`id`, `criterion_id`, `eligibility_criteria_id`) values (3, 3, 3);

insert into `algorithm_engine` (`id`, `el_criteria_has_criterion_id`, `parent_path`) values (1, 1, 'parent_path1');
insert into `algorithm_engine` (`id`, `el_criteria_has_criterion_id`, `parent_path`) values (2, 2, 'parent_path2');

insert into `study_algorithm_engine` (`study_version_id`, `algorithm_engine_id`) values (1, 1);
