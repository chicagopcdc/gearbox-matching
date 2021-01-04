use pedal_dev_v_0;

insert into `study` (`id`, `name`, `code`) values (1, 'study', 'study1');
insert into `study` (`id`, `name`, `code`) values (2, 'study', 'study2');

insert into `site` (`id`, `name`, `code`) values (1, 'site 1', 'site1');

insert into `site_has_study` (`site_id`, `study_id`) values (1, 1);

insert into `study_version` (`id`, `study_id`) values (1, 1);
insert into `study_version` (`id`, `study_id`) values (2, 1);
insert into `study_version` (`id`, `study_id`) values (3, 2);

insert into `algorithm_engine` (`id`, `name`, `type`) values (1, 'algo1', 'sum');
insert into `algorithm_engine` (`id`, `name`, `type`) values (2, 'algo2', 'sum');

insert into `study_algorithm_engine` (`study_version_id`, `study_id`, `algorithm_engine_id`) values (1, 1, 1);

insert into `logins` (`sub_id`, `refresh_token`, `iat`, `exp`) values (1, 'alphaNum0123', '2020-01-01T00:00:00.000', '2021-01-01T00:00:00.000');

insert into `criterion` (`id`, `code`) values (1, 'code1');
insert into `criterion` (`id`, `code`) values (2, 'code2');

insert into `tag` (`id`, `code`) values (1, 'code1');
insert into `tag` (`id`, `code`) values (2, 'code2');

insert into `eligibility_criteria` (`id`, `study_version_id`) values (1, 1);
insert into `eligibility_criteria` (`id`, `study_version_id`) values (2, 2);
