# GEARBOx API design discussion

This is a summary of a discussion on GEARBOx API design on July 31, 2020.

## Highlights:

- Eligibility criteria will be extracted from studies as a separate abstraction
- Backend will provide three separate endpoints for:
  1. Input fields configuration
  3. Studies and eligibility criteria
  2. save and get input form data 
  
- Frontend will be responsible for matching
- Rough API design for response data
- "Maybe" criteria for each study will be ignored and instead provided as extra info for that study

## General workflow

Backend provides GET endpoints for 1) Input Fields configuration, 2) Studies and eligibility Criteria, and 3) Save and get input form data. Backend must validate the data prior to serving them. Backend also provides a POST endpoint for saved input values--request body must provide user information.

Frontend requests to and fetches from backend all data at successful authentication. Frontend then carries out the following tasks:

- generate the match form input fields based on 1)
- fetch saved input values for the user from backend if availble to fill out the match form 3)
- display Studies and mark the current match status of each Study based on 2)
- at each registered change in input values:
  - update the match status
  - disable input fields not needed in the remaining criteria
  - send the current set of input values to backend

## Endpoints

Please note that the following information on endpoint and API are not stable and subject to change. Consider this section more as a proposal/working definition.

### Input Fields

- Endpoint: GET `/input-fields?study_ids=1,2,3...`
- API:

```jsonc
// an object with two props: "groups" and "inputs"
{
  // an array of group names to organize generated input fields
  // each "group" will get a heading unless its value is empty string ""
  "groups": [
    {id: 0, name: ""},
    {id:1, name: "first group"},
    {id:2, name: "second group"}
    // ...more groups
  ],

  // an array of input object with relevant props
  "inputs": [
    {
      // name, type, group are required all all inputs
      "name": "", // variable name
      "type": "", // one of the following: "checkbox", "radio", "number", "text", "select", "multiselect"
      "group_ids": [], // one of the values in "groups" above
      "eligibility_criteria_ids": [],
      
      // the rest is optional
      "label": "", // label text to display
      "options": [], // used for input types "radio", "select", "multiselect"
      "placeholder": "" // used for input types "number", "text", "select", "multiselect"

      // ... more attributes
    },
    {
      "name": "",
      "type": "",
      "group": ""
      // ...
    }
  ]
}
```

See [this demo app](https://poc-dynamic-form.netlify.app/) for an example.

### Studies

- Endpoint: GET `/studies`
- API:

```jsonc
// an array of study objects
[
  {
    "id": "", // unique id for the given study
    "title": "",
    "group": "",
    "location": "",
    "eligibility_criteria":   // an array of eligibility criteria objects
    [                        // each elegibility criteria is an object with a range of permissible values
      {
        "input": {
          "name": "", // variable name
          "type": "",
          "value": []   // values to match; see below for possible value types
          // ... other props
        },  
      },
      {
        "input": {
          // ...
        }
      },
  }
]
 
```

#### Possible input value types

- Single boolean: `true`, `false`
- Single numeric value: number
- Single text value: string
- Range of numbers: array of two numbers or null
  - examples:
    - `[5, 10]`: between 5 and 10 (inclusive)
    - `[5, null]`: 5 or more
    - `[null, 10]`: 10 or less
- Set of text values: array of strings
  - match if the input form value matches one of the strings
  
  
### Studies

- Endpoint: GET/POST `/form`
- API:

```jsonc
// an array of inputs
[
  {
      // name, type, group are required all all inputs
      "name": "", // variable name
      "type": "", // one of the following: "checkbox", "radio", "number", "text", "select", "multiselect"
      "group_ids": [], // one of the values in "groups" above
      "eligibility_criteria_id": [],
      "value": ""       //The value inserted/typed by the user
      
      // the rest is optional
      "label": "", // label text to display
      "options": [], // used for input types "radio", "select", "multiselect"
      "placeholder": "" // used for input types "number", "text", "select", "multiselect"

      // ... more attributes
    },
]
 
```
