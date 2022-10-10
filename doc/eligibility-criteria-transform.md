# GEARBOx match condition transformation and database representation

This document describes the method of representing match condition criteria in the GEARBOx backend database and how those criteria are represented in the match condition json that is returned to the front end application by the match-condition endpoint.

<details>
  <summary>
    <em>Updates:</em>
  </summary>
  
> - July 12, 2022
>   - Initial revision
</details>

For the purposes of this document, it is assumed that study criteria have already been tranformed from the descriptions in <href> clinicaltrials.gov </href>  into boolean expressions as below. These expressions are stored as dot separated (EL_CRITERIA_HAS_CRITERION.path) path values in the ALGORITHM_ENGINE table. Tree traversal in the paths is depth first left (AND) before right (OR) except in cases where an explicit operator and group number are indicated in the path. 

Explicit operators are used when the default tree traversal is not sufficient to logically represent a match condition, or when it may be a more concise representation. Every explicit operator in a path includes the operator type ('AND','OR') along with a unique group number to indicate the scope to which the explicit operator applies. See examples below for illustration. 

## Example default with no explicit operators:
> ( \
> ((diagnosis == 'Acute myeloid leukemia (AML)') and (ever_refractory == 'Yes' and current_refractory == 'Yes' and current_refractory_num_cycles >= 2)) \
> or \
> ((diagnosis == 'Ambiguous lineage acute leukemia (ALAL)') and (ever_refractory == 'Yes' and current_refractory == 'Yes' and current_refractory_num_cycles >= 2)) \
> or \
> ((diagnosis == 'Acute myeloid leukemia (AML)') and (ever_relapse == 'Yes' and current_relapse == 'Yes')) \
> or \
> ((diagnosis == 'Ambiguous lineage acute leukemia (ALAL)') and (ever_relapse == 'Yes' and current_relapse == 'Yes')) \
> ) \

ALGORITHM_ENGINE.path (EL_CRITERIA_HAS_CRITERION.id) tree representation
> 80.81.82.83.84 \
> 80.85.82.83.84 \
> 80.81.86.87 \
> 80.85.86.87 

This series of paths is read as: \
( \
    (80 and 81 and 82 and 83 and 84) OR \
    (80 and 85 and 82 and 83 and 84) OR \
    (80 and 81 and 86 and 87)  OR \
    (80 and 85 and 86 and 87) \
)

And should be transformed into the following json:
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

## Example explicit operator and group:
This example illustrates one way an explicit operator might be used to represent 3 criteria grouped together by an 'OR':

> (ecog == ECOG 0 OR ecog == ECOG 1 OR ecog == ECOG 2)

Here the node is represented in the form: criteria-explicit operator-group number where the group number is a marker for all nodes for which the explicit operator applies. In the simple example below, nodes 102, 103, and 467 all belong to the same logical group in the expression, and all are indicated with 'G2'

ALGORITHM_ENGINE.path (EL_CRITERIA_HAS_CRITERION.id) tree representation
> 102-OR-G2.103-OR-G2.467-OR-G2

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

## Example explicit operator:
Here is an example of explicit operators in nested groups:

> ( \
>   (norm_cardiac = 'no' and norm_lv = 'no' and (meas_ef >= 40 or meas_sf >= 25)) \
>   (norm_cardiac = 'no' and norm_lv = 'yes') or \
>   (norm_cardiac = 'yes') or \
> )

ALGORITHM_ENGINE.path (EL_CRITERIA_HAS_CRITERION.id) tree representation
> 502-OR-G4.503.110-OR-G5.111-OR-G5 \
> 502-OR-G4.478 \
> 477-OR-G4 

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
                                "110", //(most recent Ejection Fraction (EF) (in %) >= 40)
                                 "111" // (Shortening Fraction (SF) (in %) >= 25)
                            ]
                        },
                        "478" // (normal left ventricular function = "true")
                    ]
                }
            ]
        },
        "477" // (normal cardiac function test result = "true")
    ]
}
```
