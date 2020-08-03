# GEARBOx API design discussion

This is a summary of a discussion on GEARBOx API design on July 31, 2020.

Significantly updated on Auguest 3, 2020.

## Highlights:

- Eligibility Criteria will be extracted from studies as a separate abstraction
- Backend will provide four separate endpoints for:
  1. Match Form configuration
  2. Studies
  3. Eligibility Criteria
  4. Latest User Input for the Match Form
- Frontend will be responsible for matching/displaying matched Studies to User Input values for the Match Form
- Rough API design for response data
- "Maybe" criteria for each Study will be ignored and instead provided as extra info for that Study

## General workflow

Backend provides GET endpoints for 1) Match Form configuration, 2) Studies, 3) Eligibility Criteria, and 4) latest User Input for the Match Form. Backend must validate the data prior to serving them. Backend also provides a POST endpoint for latest User Input values--request body must provide User information.

Frontend requests to and fetches from Backend all data at successful authentication. Frontend then carries out the following tasks:

- Generate the Match Form input fields based on 1)
- Fetch saved input values for the user from Backend if availble to fill out the Match Form 4)
- Display Studies and mark the current match status of each Study based on 1), 2) and 3)
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
      "type": "", // one of the following: "checkbox", "radio", "number", "text", "select", "multiselect"

      // the rest is optional
      "label": "", // label text to display; avilable for all field types
      "options": [], // options to choose from; available for field types "radio", "select", "multiselect"
      "placeholder": "" // placeholder text to display; available for field types "number", "text", "select", "multiselect"

      // ... more attributes
    }
    // ...more fields
  ]
}
```

See [this demo app](https://poc-dynamic-form.netlify.app/) for an example.

### Studies

- Endpoint: GET `/studies`
- API:

```jsonc
// an array of Study objects
[
  {
    "id": 0, // unique id for the Trial
    "title": "",
    "group": "",
    "location": ""
    // ...more information on the Trial
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
    "fieldValue": , // IMPORTANT: see below for more details
    "studyIds": [0, 1]
  },
  // ...more Criteria
]
```

#### Possible `fieldValue` types

- Single boolean: `true`, `false`
- Single numeric value: number
- Single text value: string
- Range of numbers: array of two numbers or null
  - examples:
    - `[5, 10]`: between 5 and 10 (inclusive)
    - `[5, null]`: 5 or more
    - `[null, 10]`: 10 or less
- Set of text values: array of strings
  - match if the Match Form field value matches one of the strings

### Latest User Input

- Endpoints:
  - GET `/latest-user-input?userId=0`
  - POST `/latest-user-input`
- API:

```jsonc
{
  "userId": 0, // unique id for the user
  "fields": [
    {
      "id": 0,
      "value": // value type must conform to what the relevant input value allows
    }
    // ... more fields
  ]
}
```
