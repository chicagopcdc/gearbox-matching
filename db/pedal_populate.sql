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
insert into `study` (`id`, `name`, `code`) values (10, 'study', 'study10');
insert into `study` (`id`, `name`, `code`) values (11, 'study', 'study11');
insert into `study` (`id`, `name`, `code`) values (12, 'study', 'study12');

insert into `site` (`id`, `name`, `code`) values (1, 'site 1', 'site1');
insert into `site` (`id`, `name`, `code`) values (2, 'site 2', 'site2');
insert into `site` (`id`, `name`, `code`) values (3, 'site 3', 'site3');
insert into `site` (`id`, `name`, `code`) values (4, 'site 4', 'site4');

insert into `study_version` (`id`, `study_id`) values (1, 1);
insert into `study_version` (`id`, `study_id`) values (2, 2);
insert into `study_version` (`id`, `study_id`) values (3, 3);
insert into `study_version` (`id`, `study_id`) values (4, 4);
insert into `study_version` (`id`, `study_id`) values (5, 5);
insert into `study_version` (`id`, `study_id`) values (6, 6);
insert into `study_version` (`id`, `study_id`) values (7, 7);
insert into `study_version` (`id`, `study_id`) values (8, 8);
insert into `study_version` (`id`, `study_id`) values (9, 9);

insert into `note` (`id`, `value`) values (1, 'value1');
insert into `note` (`id`, `value`) values (2, 'value2');
insert into `note` (`id`, `value`) values (3, 'value3');

insert into `tag` (`id`, `code`) values (1, 'code1');
insert into `tag` (`id`, `code`) values (2, 'code2');

insert into `criterion` (`id`, `code`) values (1, 'code1');
insert into `criterion` (`id`, `code`) values (2, 'code2');
insert into `criterion` (`id`, `code`) values (3, 'code3');
insert into `criterion` (`id`, `code`) values (4, 'code4');
insert into `criterion` (`id`, `code`) values (5, 'code5');

insert into `eligibility_criteria` (`id`, `study_version_id`) values (1, 1);
insert into `eligibility_criteria` (`id`, `study_version_id`) values (2, 2);
insert into `eligibility_criteria` (`id`, `study_version_id`) values (3, 3);
insert into `eligibility_criteria` (`id`, `study_version_id`) values (4, 4);
insert into `eligibility_criteria` (`id`, `study_version_id`) values (5, 5);

insert into `value` (`id`, `code`, `description`, `type`, `value_string`, `unit`, `operator`, `active`) values (1, 'lt_22_yr', 'lower than 22 years', 'Integer', '22', 'years', 'lt', 1);
insert into `value` (`id`, `code`, `description`, `type`, `value_string`, `operator`, `active`) values (2, 'Yes', 'is true', 'Boolean', 'Yes', 'eq', 1);
insert into `value` (`id`, `code`, `description`, `type`, `value_string`, `unit`, `operator`, `active`) values (3, 'gte_5_p', 'greater than or equal to 5%', 'Float', '5', '%', 'gte', 1);
insert into `value` (`id`, `code`, `description`, `type`, `value_string`, `unit`, `operator`, `active`) values (4, 'gte_1_p', 'greater than or equal to 1%', 'Float', '1', '%', 'gte', 1);
insert into `value` (`id`, `code`, `description`, `type`, `value_string`, `unit`, `operator`, `active`) values (5, 'gte_0_1_p', 'greater than or equal to 0.1%', 'Float', '0.1', '%', 'gte', 1);

insert into `el_criteria_has_criterion` (`id`, `criterion_id`, `eligibility_criteria_id`, `value_id`) values (1, 1, 1, 1);
insert into `el_criteria_has_criterion` (`id`, `criterion_id`, `eligibility_criteria_id`, `value_id`) values (2, 2, 2, 2);
insert into `el_criteria_has_criterion` (`id`, `criterion_id`, `eligibility_criteria_id`, `value_id`) values (3, 3, 3, 3);
insert into `el_criteria_has_criterion` (`id`, `criterion_id`, `eligibility_criteria_id`, `value_id`) values (4, 4, 4, 4);
insert into `el_criteria_has_criterion` (`id`, `criterion_id`, `eligibility_criteria_id`, `value_id`) values (5, 5, 5, 5);

insert into `algorithm_engine` (`id`, `el_criteria_has_criterion_id`, `parent_id`, `parent_path`) values (1, 1, 1, 'parent_path1');
insert into `algorithm_engine` (`id`, `el_criteria_has_criterion_id`, `parent_id`, `parent_path`) values (2, 2, 1, 'parent_path2');

insert into `study_algorithm_engine` (`study_version_id`, `algorithm_engine_id`) values (1, 1);

insert into `display_rules` (`id`, `criterion_id`, `priority`) values (1, 1, 1);
insert into `display_rules` (`id`, `criterion_id`, `priority`) values (2, 2, 2);

insert into `input_type` (`id`, `data_type`, `render_type`) values (1, 'data_type_1', 'render_1');
insert into `input_type` (`id`, `data_type`, `render_type`) values (2, 'data_type_2', 'render_2');
insert into `input_type` (`id`, `data_type`, `render_type`) values (3, 'data_type_3', 'render_3');
