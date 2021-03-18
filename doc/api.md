# GEARBOx API design discussion

This is a summary of a discussion on GEARBOx API design on July 31, 2020.

> _Updates_:
>
> - Auguest 3, 2020:
>   - renamed endpoints
>   - added a separate endpoint and API for Eligibility Criteria
>   - added details on latest user to Highlights and General Workflow
> - August 5, 2020:
>   - added a block for document updates
>   - added a separate endpoint and API for Matching Conditions
> - Auguet 7, 2020:
>   - modified Latest User Input endpoint and API (remove unnecessary userId)
> - February 8, 2021:
>   - modified Eligibility Criteria API (add `operator` field)
> - February 22, 2021:
>   - updated Match Form configuration API based on feedback to
>     - handle sophisticated `showIf` conditions
>     - add a new `age` input type
>     - modify `options` value into an object with "value", "label", and "descrtiption" attributes
> - March 1, 2021
>   - updated Match Form configuration API `options` value type
> - March 18, 2012
>   - updated Studies API based on feedback

## Highlights:

- Eligibility Criteria will be extracted from studies as a separate abstraction
- Backend will provide four separate endpoints for:
  1. Match Form configuration
  2. Studies
  3. Eligibility Criteria
  4. Match Conditions
  5. Latest User Input for the Match Form
- Frontend will be responsible for matching/displaying matched Studies to User Input values for the Match Form
- Rough API design for response data
- "Maybe" criteria for each Study will be ignored and instead provided as extra info for that Study

## General workflow

Backend provides GET endpoints for 1) Match Form configuration, 2) Studies, 3) Eligibility Criteria, 4) Match Conditions, and 5) latest User Input for the Match Form. Backend must validate the data prior to serving them. Backend also provides a POST endpoint for latest User Input values--request body must provide User information.

Frontend requests to and fetches from Backend all data at successful authentication. Frontend then carries out the following tasks:

- Generate the Match Form input fields based on 1)
- Fetch saved input values for the user from Backend if availble to fill out the Match Form using 5)
- Display Studies and mark the current match status of each Study based on 1), 2), 3), and 4)
- At each registered change in Match Form input field values:
  - Update the match status
  - Disable input fields not needed in the remaining Eligibility Criteria
  - Send the current Match Form input values to Backend

## Endpoints and APIs

Please note that the following information on each endpoint and API is not stable and subject to change. Consider this section more as a proposal/working definition.

### Match Form configuration

- Endpoint: GET `/match-form`
- API:

```jsonc
// an object with two props: "groups" and "fields"
{
  // an array of group objects to organize generated form input fields
  // each "group" will get a heading unless its value is empty string ""
  "groups": [
    {
      "id": 0, // unique id for the group
      "name": ""
    },
    {
      "id": 1,
      "name": "first group"
    }
    // ...more groups
  ],

  // an array of field objects with relevant props/attributes
  "fields": [
    {
      "id": 0, // unique id for the field
      "groupId": 0, // one of the IDs in "groups" above

      // name, type, group are required all all fields
      "name": "", // field name
      "type": "", // one of the following: "checkbox", "radio", "number", "text", "select", "multiselect", "age"

      // the rest is optional
      "label": "", // label text to display; avilable for all field types
      "showIf": { // for conditional display; available for all field types
        "operator": "AND", // possible values: AND, OR
        "criteria": [
          {
            "id": 1, // id for another field
            "operator": "eq", // one of the following: "eq", "gt", "gte", "lt", "lte", "ne"
            "value": // value for another field; boolean, string, or number
          }
        ]
      },
      "options": [ // options to choose from; available for field types "radio", "select", "multiselect"
        {
          "value": 0, // integer; based on id in database
          "label": "",
          "description": "" // optional; available for "select" only
        }
      ],
      "placeholder": "" // placeholder text to display; available for field types "number", "text", "select", "multiselect"

      // ... more attributes
    }
    // ...more fields
  ]
}
```

See [this demo app](https://poc-dynamic-form.netlify.app/) for an example.

#### Conditional rendering with `showIf`

Fields with `showIf` property are conditionally rendered based on the values of other fields. The `showIf` value shape is based on those of Eligibility Criteria and Match Conditions (see below).

#### Field type `"age"`

This is a special input type with a dedicated input component consisting of year, month, and day input fields. The actual `age` value will be in days, and the values for year and month fields will be converted to days using the following formula:

* 1 year is 365 days
* 1 month is 30 days

### Studies

- Endpoint: GET `/studies`
- API:

```jsonc
// an array of Study objects
[
  {
    "id": 0, // unique id for the Trial
    "title": "",
    "description": "",
    "locations": [""],
    "links": [
      {
        "name": "",
        "href": "" // URL
      }
    ]
  }
  // ...more Studies
]
```

### Eligibility Criteria

- Endpoint: GET `/eligibility-criteria`
- API:

```jsonc
// an array of Eligibility Criteria objects
[
  {
    "id": 0, // unique id for the Criterion
    "fieldId": 0,
    "fieldValue":, // boolean | string | number; see below for more details
    "operator": // "eq" | "gt" | "gte" | "lt" | "lte" | "ne"; see below for more details
  },
  // ...more Criteria
]
```

#### Possible `fieldValue` types

- Single boolean: `true`, `false`
- Single numeric value: number
- Single text value: string

#### Possible `operator` values

- `"eq"`: equal to (`==`)
- `"gt"`: greater than (`>`)
- `"gte"`: greater than/equal to (`>=`)
- `"lt"`: less than (`<`)
- `"lte"`: less than/equal to (`<=`)
- `"ne"`: not equal to (`!=`)


### Match Conditions

- Endpoint: GET `/match-conditions`
- API:

```jsonc
// an array of Match Condition objects
[
  {
    "studyId": 0, // Study id for the given Match Condition
    "algorithm": {
      "operator": "AND", // possible values: AND, OR
      // array of Eligibility Criterion ids or algorithm objs
      "criteria": [
        1,
        {
          "operator": "OR",
          "criteria": [2, 3]
        },
        4
      ]
    }
  }
  // more Match Conditions
]
```

### Latest User Input

- Endpoint: GET, POST `/latest-user-input`
- API:

```jsonc
// an array of field id-value pair
[
  {
    "id": 0,
    "value": // value type must conform to what the relevant input value allows
  }
  // ... more fields
]
```
