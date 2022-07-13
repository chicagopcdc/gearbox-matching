# GEARBOx study criteria transformation for the creation of match conditions

This document describes the transformation of study criteria from information extracted from 
<href> clinicaltrials.gov </href> to their representation in the GEARBOx backend database. 

<details>
  <summary>
    <em>Updates:</em>
  </summary>
  
> - July 12, 2022
>   - Initial revision
</details>

## General workflow and logic

For the purposes of this document, it is assumed that the study criteria are represented by boolean expressions as below:

> > "( \
> > ((diagnosis == 'Acute myeloid leukemia (AML)') and (ever_refractory == 'Yes' and current_refractory == 'Yes' and current_refractory_num_cycles >= 2)) \
> > or \
> > ((diagnosis == 'Ambiguous lineage acute leukemia (ALAL)') and (ever_refractory == 'Yes' and current_refractory == 'Yes' and current_refractory_num_cycles >= 2)) \
> > or \
> > ((diagnosis == 'Acute myeloid leukemia (AML)') and (ever_relapse == 'Yes' and current_relapse == 'Yes')) \
> > or \
> > ((diagnosis == 'Ambiguous lineage acute leukemia (ALAL)') and (ever_relapse == 'Yes' and current_relapse == 'Yes')) \
> > )" \

Example default:

path
>> 80.81.82.83.84 \
>> 80.85.82.83.84 \
>> 80.81.86.87 \
>> 80.85.86.87 

match condition endpoint output json
```jsonc
        {       
                "operator": "AND",
                "criteria": [
                    "80", // (age <= 24 years)
                    {   
                        "operator": "OR",
                        "criteria": [ 
                            {   
                                "operator": "AND", 
                                "criteria": [ 
                                    "81", // (AML)
                                    {   
                                        "operator": "OR", 
                                        "criteria": [
                                            {    
                                                "operator": "AND", 
                                                "criteria": [
                                                    "82", // (refractory disease = "yes") 
                                                    "83", // (currently refractory = "yes")
                                                    "84" // (refractory cycles >= 2) 
                                                ] 
                                            },
                                            {   
                                                "operator": "AND",
                                                "criteria": [
                                                    "86", // (relapase = "yes")
                                                    "87" // (currently in relapse = "yes")
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {   
                                "operator": "AND",
                                "criteria": [
                                    "85", (
                                    {    
                                        "operator": "OR",
                                        "criteria": [ 
                                            {   
                                                "operator": "AND",
                                                "criteria": [
                                                    "82", // (refractory disease = "yes")
                                                    "83", // (currently refractory = "yes")
                                                    "84" // (refractory cycles >= 2) 
                                                ]
                                            },
                                            {   
                                                "operator": "AND",
                                                "criteria": [ 
                                                    "86", // (relapase = "yes")
                                                    "87" // (currently in relapse = "yes")
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                }
            ]
        }
```

Example explicit operator:

> (ecog == ECOG 0 or ecog == ECOG 1 or ecog == ECOG 2)

path
>> 80.102-OR-G2.103-OR-G2.467-OR-G2

match condition endpoint output json

```jsonc
{
    "operator": "OR",
    "criteria": [
        "102", // (ECOG 0 (Lansky/Karnofsky 90-100)
        "103", // (ECOG 1 (Lansky/Karnofsky 70-80))
        "467" // (ECOG 2 (Lansky/Karnofsky 50-60)
    ]
},
```

Example explicit operator:

>> ((norm_cardiac = 'yes') or
>> (norm_cardiac = 'no' and norm_lv = 'yes') or
>> (norm_cardiac = 'no' and norm_lv = 'no' and (meas_ef >= 40 or meas_sf >= 25)))

path

>> 80.502-OR-G4.503.110-OR-G5.111-OR-G5 \
>> 80.502-OR-G4.478 \
>> 80.477-OR-G4 \

```jsonc
{
    "operator": "OR",
    "criteria": [
        {
            "operator": "AND",
            "criteria": [
                "502", // (normal: cardiac function test results = "false")
                {
                    "operator": "OR",
                    "criteria": [
                        "503",  // (normal: left ventricular function = "false")
                        {
                            "operator": "OR",
                            "criteria": [
                                "110",
                                 "111"
                            ]
                        },
                        "478"
                    ]
                }
            ]
        },
        "477"
    ]
}
```
