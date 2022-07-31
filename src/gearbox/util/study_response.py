from gearbox.models.models import Study, StudyLink

def format_study_response(study_list):
    ret_val = []
    for study in study_list:
        study_dict = {}

        study_dict['id'] = study.id
        study_dict['title'] = study.name
        study_dict['code'] = study.code
        study_dict['description'] = study.description

        link_list = []
        for link in study.links:
            link_dict = {}
            link_dict['name'] = link.name
            link_dict['href'] = link.href

            link_list.append(link_dict)
        study_dict['links'] = link_list

        ret_val.append(study_dict)

        site_list = []        
        for site_has_study in study.sites:
            site_list.append(site_has_study.site.name)
        study_dict['locations'] = site_list

    return ret_val
